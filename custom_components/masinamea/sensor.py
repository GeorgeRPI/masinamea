"""Senzori pentru integrarea Mașina Mea."""
from datetime import datetime, date
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN

from .const import (
    DOMAIN,
    CONF_NUME_AUTO,
    CONF_NR_INMATRICULARE,
    CONF_MARCA,
    CONF_MODEL,
    CONF_CAPACITATE_CILINDRICA,
    CONF_KM_CURENTI,
    CONF_DATA_ITP,
    CONF_ITP_EXPIRA,
    CONF_DATA_ROVINIETA,
    CONF_ROVINIETA_EXPIRA,
    CONF_DATA_REVIZIE,
    CONF_KM_REVIZIE,
    CONF_SCHIMB_ULEI,
    CONF_SCHIMB_FILTRU_ULEI,
    CONF_SCHIMB_FILTRU_AER,
    CONF_SCHIMB_FILTRU_COMBUSTIBIL,
    STATE_ACTIV,
    STATE_EXPIRAT,
    STATE_APROAPE_EXPIRARE,
    ITP_PRAG_AVERTISMENT,
    ROVINIETA_PRAG_AVERTISMENT,
    PRAG_URGENT
)

def parse_date(date_str):
    """Convertește data din format DD.MM.YYYY în obiect date."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except:
        return None

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configurează senzorii."""
    data = config_entry.data
    sensors = []
    
    # Senzor informații mașină
    sensors.append(CarInfoSensor(data))
    sensors.append(PlateNumberSensor(data))
    sensors.append(CurrentKmSensor(data))
    sensors.append(EngineCapacitySensor(data))
    
    # Senzori ITP
    sensors.append(ItpStatusSensor(data))
    sensors.append(ItpExpirySensor(data))
    sensors.append(ItpUrgencySensor(data))
    
    # Senzori Rovinietă
    sensors.append(RovinietaStatusSensor(data))
    sensors.append(RovinietaExpirySensor(data))
    sensors.append(RovinietaUrgencySensor(data))
    
    # Senzori Revizie
    sensors.append(ServiceInfoSensor(data))
    sensors.append(ServiceKmSensor(data))
    sensors.append(ServiceDaysSensor(data))
    sensors.append(ServiceRecommendationSensor(data))
    
    async_add_entities(sensors, True)


class CarInfoSensor(SensorEntity):
    """Senzor informații generale mașină."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Informații"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_info"
        self._attr_icon = "mdi:car-info"

    @property
    def state(self):
        return self._data.get(CONF_MARCA, "Necunoscut")

    @property
    def extra_state_attributes(self):
        return {
            "marca": self._data.get(CONF_MARCA),
            "model": self._data.get(CONF_MODEL),
            "capacitate_cilindrica": self._data.get(CONF_CAPACITATE_CILINDRICA),
            "nume": self._data.get(CONF_NUME_AUTO),
            "nr_inmatriculare": self._data.get(CONF_NR_INMATRICULARE),
        }


class PlateNumberSensor(SensorEntity):
    """Senzor număr înmatriculare."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Număr înmatriculare"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_plate"
        self._attr_icon = "mdi:car-license-plate"

    @property
    def state(self):
        plate = self._data.get(CONF_NR_INMATRICULARE)
        return plate if plate else "Necunoscut"


class CurrentKmSensor(SensorEntity):
    """Senzor kilometraj curent."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Kilometraj"
        self._attr_unit_of_measurement = "km"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_km"
        self._attr_icon = "mdi:counter"

    @property
    def state(self):
        return self._data.get(CONF_KM_CURENTI, 0)


class EngineCapacitySensor(SensorEntity):
    """Senzor capacitate cilindrică."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Capacitate cilindrică"
        self._attr_unit_of_measurement = "cm³"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_capacity"
        self._attr_icon = "mdi:engine"

    @property
    def state(self):
        return self._data.get(CONF_CAPACITATE_CILINDRICA, "N/A")


class ItpStatusSensor(SensorEntity):
    """Senzor status ITP."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} ITP Status"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_itp_status"
        self._attr_icon = "mdi:car-wrench"

    def _get_days_left(self):
        """Calculează zilele rămase până la expirare."""
        expiry_date_str = self._data.get(CONF_ITP_EXPIRA)
        if not expiry_date_str:
            return None
        
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            return None
        
        today = date.today()
        return (expiry_date - today).days

    def _calculate_status(self):
        """Calculează statusul ITP."""
        days_left = self._get_days_left()
        
        if days_left is None:
            return "nedefinit"
        
        if days_left < 0:
            return STATE_EXPIRAT
        elif days_left <= PRAG_URGENT:
            return "urgent"
        elif days_left <= ITP_PRAG_AVERTISMENT:
            return STATE_APROAPE_EXPIRARE
        else:
            return STATE_ACTIV

    @property
    def state(self):
        return self._calculate_status()

    @property
    def icon(self):
        """Returnează iconița în funcție de status."""
        if self.state == STATE_EXPIRAT:
            return "mdi:alert-circle"
        elif self.state == "urgent":
            return "mdi:clock-alert"
        elif self.state == STATE_APROAPE_EXPIRARE:
            return "mdi:clock-alert-outline"
        else:
            return "mdi:check-circle"

    @property
    def extra_state_attributes(self):
        days_left = self._get_days_left()
        return {
            "data_efectuare": self._data.get(CONF_DATA_ITP),
            "data_expirare": self._data.get(CONF_ITP_EXPIRA),
            "zile_ramase": days_left if days_left is not None else "N/A",
        }


class ItpExpirySensor(SensorEntity):
    """Senzor zile până la expirare ITP."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} ITP Expira în"
        self._attr_unit_of_measurement = "zile"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_itp_days"
        self._attr_icon = "mdi:calendar-clock"

    @property
    def state(self):
        expiry_date_str = self._data.get(CONF_ITP_EXPIRA)
        if not expiry_date_str:
            return None
        
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            return None
        
        today = date.today()
        days_left = (expiry_date - today).days
        return max(0, days_left)


class ItpUrgencySensor(SensorEntity):
    """Senzor nivel urgență ITP."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} ITP Urgență"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_itp_urgency"
        self._attr_icon = "mdi:alert"

    @property
    def state(self):
        expiry_date_str = self._data.get(CONF_ITP_EXPIRA)
        if not expiry_date_str:
            return "nedefinit"
        
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            return "eroare"
        
        today = date.today()
        days_left = (expiry_date - today).days
        
        if days_left < 0:
            return "critic"
        elif days_left <= PRAG_URGENT:
            return "urgent"
        elif days_left <= ITP_PRAG_AVERTISMENT:
            return "averizare"
        else:
            return "ok"


class RovinietaStatusSensor(SensorEntity):
    """Senzor status Rovinietă."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Rovinietă Status"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_rovinieta_status"
        self._attr_icon = "mdi:road-variant"

    def _get_days_left(self):
        """Calculează zilele rămase până la expirare."""
        expiry_date_str = self._data.get(CONF_ROVINIETA_EXPIRA)
        if not expiry_date_str:
            return None
        
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            return None
        
        today = date.today()
        return (expiry_date - today).days

    def _calculate_status(self):
        """Calculează statusul Rovinietei."""
        days_left = self._get_days_left()
        
        if days_left is None:
            return "nedefinit"
        
        if days_left < 0:
            return STATE_EXPIRAT
        elif days_left <= PRAG_URGENT:
            return "urgent"
        elif days_left <= ROVINIETA_PRAG_AVERTISMENT:
            return STATE_APROAPE_EXPIRARE
        else:
            return STATE_ACTIV

    @property
    def state(self):
        return self._calculate_status()

    @property
    def icon(self):
        """Returnează iconița în funcție de status."""
        if self.state == STATE_EXPIRAT:
            return "mdi:alert-circle"
        elif self.state == "urgent":
            return "mdi:clock-alert"
        elif self.state == STATE_APROAPE_EXPIRARE:
            return "mdi:clock-alert-outline"
        else:
            return "mdi:check-circle"

    @property
    def extra_state_attributes(self):
        days_left = self._get_days_left()
        return {
            "data_achizitie": self._data.get(CONF_DATA_ROVINIETA),
            "data_expirare": self._data.get(CONF_ROVINIETA_EXPIRA),
            "zile_ramase": days_left if days_left is not None else "N/A",
        }


class RovinietaExpirySensor(SensorEntity):
    """Senzor zile până la expirare Rovinietă."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Rovinietă Expiră în"
        self._attr_unit_of_measurement = "zile"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_rovinieta_days"
        self._attr_icon = "mdi:calendar-clock"

    @property
    def state(self):
        expiry_date_str = self._data.get(CONF_ROVINIETA_EXPIRA)
        if not expiry_date_str:
            return None
        
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            return None
        
        today = date.today()
        days_left = (expiry_date - today).days
        return max(0, days_left)


class RovinietaUrgencySensor(SensorEntity):
    """Senzor nivel urgență Rovinietă."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Rovinietă Urgență"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_rovinieta_urgency"
        self._attr_icon = "mdi:alert"

    @property
    def state(self):
        expiry_date_str = self._data.get(CONF_ROVINIETA_EXPIRA)
        if not expiry_date_str:
            return "nedefinit"
        
        expiry_date = parse_date(expiry_date_str)
        if not expiry_date:
            return "eroare"
        
        today = date.today()
        days_left = (expiry_date - today).days
        
        if days_left < 0:
            return "critic"
        elif days_left <= PRAG_URGENT:
            return "urgent"
        elif days_left <= ROVINIETA_PRAG_AVERTISMENT:
            return "averizare"
        else:
            return "ok"


class ServiceInfoSensor(SensorEntity):
    """Senzor informații ultima revizie."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Ultima revizie"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_service"
        self._attr_icon = "mdi:oil"

    @property
    def state(self):
        return self._data.get(CONF_DATA_REVIZIE) or "Nu a fost efectuată"

    @property
    def extra_state_attributes(self):
        attributes = {
            "km_la_revizie": self._data.get(CONF_KM_REVIZIE),
            "schimb_ulei": "Da" if self._data.get(CONF_SCHIMB_ULEI) else "Nu",
            "schimb_filtru_ulei": "Da" if self._data.get(CONF_SCHIMB_FILTRU_ULEI) else "Nu",
            "schimb_filtru_aer": "Da" if self._data.get(CONF_SCHIMB_FILTRU_AER) else "Nu",
            "schimb_filtru_combustibil": "Da" if self._data.get(CONF_SCHIMB_FILTRU_COMBUSTIBIL) else "Nu",
        }
        return attributes


class ServiceKmSensor(SensorEntity):
    """Senzor kilometri de la ultima revizie."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Km de la revizie"
        self._attr_unit_of_measurement = "km"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_service_km"
        self._attr_icon = "mdi:counter"

    @property
    def state(self):
        current_km = self._data.get(CONF_KM_CURENTI, 0)
        service_km = self._data.get(CONF_KM_REVIZIE, 0)
        
        if service_km == 0:
            return None
            
        return current_km - service_km


class ServiceDaysSensor(SensorEntity):
    """Senzor zile de la ultima revizie."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Zile de la revizie"
        self._attr_unit_of_measurement = "zile"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_service_days"
        self._attr_icon = "mdi:calendar-range"

    @property
    def state(self):
        service_date_str = self._data.get(CONF_DATA_REVIZIE)
        if not service_date_str:
            return None
        
        service_date = parse_date(service_date_str)
        if not service_date:
            return None
        
        today = date.today()
        days_passed = (today - service_date).days
        return days_passed


class ServiceRecommendationSensor(SensorEntity):
    """Senzor recomandare revizie."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Recomandare revizie"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_service_recommendation"
        self._attr_icon = "mdi:tooltip-account"

    @property
    def state(self):
        current_km = self._data.get(CONF_KM_CURENTI, 0)
        service_km = self._data.get(CONF_KM_REVIZIE, 0)
        service_date_str = self._data.get(CONF_DATA_REVIZIE)
        
        if service_km == 0 or not service_date_str:
            return "Revizie neefectuată"
        
        service_date = parse_date(service_date_str)
        if not service_date:
            return "Eroare dată"
        
        km_diff = current_km - service_km
        days_diff = (date.today() - service_date).days
        
        # Recomandare revizie la 10.000 km sau 1 an
        if km_diff >= 10000:
            return "Revizie necesară (kilometraj)"
        elif days_diff >= 365:
            return "Revizie necesară (timp)"
        elif km_diff >= 8000:
            return "Aproape de revizie (kilometraj)"
        elif days_diff >= 300:
            return "Aproape de revizie (timp)"
        else:
            return "În regulă"

    @property
    def extra_state_attributes(self):
        current_km = self._data.get(CONF_KM_CURENTI, 0)
        service_km = self._data.get(CONF_KM_REVIZIE, 0)
        
        return {
            "km_pana_la_revizie": max(0, 10000 - (current_km - service_km)) if service_km > 0 else "N/A",
            "zile_pana_la_revizie": max(0, 365 - self.state_value) if self.state_value else "N/A",
        }
