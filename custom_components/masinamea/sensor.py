"""Senzori pentru integrarea Mașina Mea."""
from datetime import date
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
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
    PRAG_URGENT,
    REVIZIE_KM_PRAG,
    REVIZIE_KM_AVERTISMENT,
    REVIZIE_ZILE_PRAG,
    REVIZIE_ZILE_AVERTISMENT,
    parse_date,  # FIX: funcție centralizată în const.py, nu duplicată
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configurează senzorii."""
    # FIX: citim din hass.data (care include și options) în loc de config_entry.data direct
    data = hass.data[DOMAIN][config_entry.entry_id]
    entry_id = config_entry.entry_id

    sensors = [
        # Informații generale
        CarInfoSensor(data, entry_id),
        PlateNumberSensor(data, entry_id),
        CurrentKmSensor(data, entry_id),
        EngineCapacitySensor(data, entry_id),
        # ITP
        ItpStatusSensor(data, entry_id),
        ItpExpirySensor(data, entry_id),
        ItpUrgencySensor(data, entry_id),
        # Rovinietă
        RovinietaStatusSensor(data, entry_id),
        RovinietaExpirySensor(data, entry_id),
        RovinietaUrgencySensor(data, entry_id),
        # Revizie
        ServiceInfoSensor(data, entry_id),
        ServiceKmSensor(data, entry_id),
        ServiceDaysSensor(data, entry_id),
        ServiceRecommendationSensor(data, entry_id),
    ]
    async_add_entities(sensors, True)


# ---------------------------------------------------------------------------
# Clasă de bază — evită duplicarea de cod
# ---------------------------------------------------------------------------

class _BaseSensor(SensorEntity):
    """Clasă de bază pentru toți senzorii Mașina Mea."""

    def __init__(self, data: dict, entry_id: str):
        self._data = data
        self._entry_id = entry_id
        # Subclasele setează self._attr_name, self._attr_unique_id, self._attr_icon

    def _days_until(self, conf_key: str) -> int | None:
        """Returnează numărul de zile până la data din conf_key (negativ = expirat)."""
        d = parse_date(self._data.get(conf_key))
        if d is None:
            return None
        return (d - date.today()).days

    def _expiry_status(self, days_left: int | None, prag_avertisment: int) -> str:
        """Calculează starea generică pentru un document cu dată de expirare."""
        if days_left is None:
            return "nedefinit"
        if days_left < 0:
            return STATE_EXPIRAT
        if days_left <= PRAG_URGENT:
            return "urgent"
        if days_left <= prag_avertisment:
            return STATE_APROAPE_EXPIRARE
        return STATE_ACTIV

    def _expiry_icon(self, status: str) -> str:
        icons = {
            STATE_EXPIRAT: "mdi:alert-circle",
            "urgent": "mdi:clock-alert",
            STATE_APROAPE_EXPIRARE: "mdi:clock-alert-outline",
        }
        return icons.get(status, "mdi:check-circle")


# ---------------------------------------------------------------------------
# Senzori informații generale
# ---------------------------------------------------------------------------

class CarInfoSensor(_BaseSensor):
    """Senzor informații generale mașină."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Informații"
        # FIX: unique_id include entry_id — evită conflicte la mașini cu același nume
        self._attr_unique_id = f"{entry_id}_info"
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


class PlateNumberSensor(_BaseSensor):
    """Senzor număr înmatriculare."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Număr înmatriculare"
        self._attr_unique_id = f"{entry_id}_plate"
        self._attr_icon = "mdi:car-license-plate"

    @property
    def state(self):
        plate = self._data.get(CONF_NR_INMATRICULARE)
        return plate if plate else "Necunoscut"


class CurrentKmSensor(_BaseSensor):
    """Senzor kilometraj curent."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Kilometraj"
        self._attr_unit_of_measurement = "km"
        self._attr_unique_id = f"{entry_id}_km"
        self._attr_icon = "mdi:counter"

    @property
    def state(self):
        return self._data.get(CONF_KM_CURENTI, 0)


class EngineCapacitySensor(_BaseSensor):
    """Senzor capacitate cilindrică."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Capacitate cilindrică"
        self._attr_unit_of_measurement = "cm³"
        self._attr_unique_id = f"{entry_id}_capacity"
        self._attr_icon = "mdi:engine"

    @property
    def state(self):
        return self._data.get(CONF_CAPACITATE_CILINDRICA) or "N/A"


# ---------------------------------------------------------------------------
# Senzori ITP
# ---------------------------------------------------------------------------

class ItpStatusSensor(_BaseSensor):
    """Senzor status ITP."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} ITP Status"
        self._attr_unique_id = f"{entry_id}_itp_status"
        self._attr_icon = "mdi:car-wrench"

    @property
    def state(self):
        days = self._days_until(CONF_ITP_EXPIRA)
        return self._expiry_status(days, ITP_PRAG_AVERTISMENT)

    @property
    def icon(self):
        return self._expiry_icon(self.state)

    @property
    def extra_state_attributes(self):
        days = self._days_until(CONF_ITP_EXPIRA)
        return {
            "data_efectuare": self._data.get(CONF_DATA_ITP),
            "data_expirare": self._data.get(CONF_ITP_EXPIRA),
            "zile_ramase": days if days is not None else "N/A",
        }


class ItpExpirySensor(_BaseSensor):
    """Senzor zile până la expirare ITP."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} ITP Expiră în"
        self._attr_unit_of_measurement = "zile"
        self._attr_unique_id = f"{entry_id}_itp_days"
        self._attr_icon = "mdi:calendar-clock"

    @property
    def state(self):
        days = self._days_until(CONF_ITP_EXPIRA)
        if days is None:
            return None
        return max(0, days)


class ItpUrgencySensor(_BaseSensor):
    """Senzor nivel urgență ITP."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} ITP Urgență"
        self._attr_unique_id = f"{entry_id}_itp_urgency"
        self._attr_icon = "mdi:alert"

    @property
    def state(self):
        days = self._days_until(CONF_ITP_EXPIRA)
        if days is None:
            return "nedefinit"
        if days < 0:
            return "critic"
        if days <= PRAG_URGENT:
            return "urgent"
        if days <= ITP_PRAG_AVERTISMENT:
            # FIX: era "averizare" (typo) — corectat la "avertizare"
            return "avertizare"
        return "ok"


# ---------------------------------------------------------------------------
# Senzori Rovinietă
# ---------------------------------------------------------------------------

class RovinietaStatusSensor(_BaseSensor):
    """Senzor status Rovinietă."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Rovinietă Status"
        self._attr_unique_id = f"{entry_id}_rovinieta_status"
        self._attr_icon = "mdi:road-variant"

    @property
    def state(self):
        days = self._days_until(CONF_ROVINIETA_EXPIRA)
        return self._expiry_status(days, ROVINIETA_PRAG_AVERTISMENT)

    @property
    def icon(self):
        return self._expiry_icon(self.state)

    @property
    def extra_state_attributes(self):
        days = self._days_until(CONF_ROVINIETA_EXPIRA)
        return {
            "data_achizitie": self._data.get(CONF_DATA_ROVINIETA),
            "data_expirare": self._data.get(CONF_ROVINIETA_EXPIRA),
            "zile_ramase": days if days is not None else "N/A",
        }


class RovinietaExpirySensor(_BaseSensor):
    """Senzor zile până la expirare Rovinietă."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Rovinietă Expiră în"
        self._attr_unit_of_measurement = "zile"
        self._attr_unique_id = f"{entry_id}_rovinieta_days"
        self._attr_icon = "mdi:calendar-clock"

    @property
    def state(self):
        days = self._days_until(CONF_ROVINIETA_EXPIRA)
        if days is None:
            return None
        return max(0, days)


class RovinietaUrgencySensor(_BaseSensor):
    """Senzor nivel urgență Rovinietă."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Rovinietă Urgență"
        self._attr_unique_id = f"{entry_id}_rovinieta_urgency"
        self._attr_icon = "mdi:alert"

    @property
    def state(self):
        days = self._days_until(CONF_ROVINIETA_EXPIRA)
        if days is None:
            return "nedefinit"
        if days < 0:
            return "critic"
        if days <= PRAG_URGENT:
            return "urgent"
        if days <= ROVINIETA_PRAG_AVERTISMENT:
            # FIX: era "averizare" (typo) — corectat la "avertizare"
            return "avertizare"
        return "ok"


# ---------------------------------------------------------------------------
# Senzori Revizie
# ---------------------------------------------------------------------------

class ServiceInfoSensor(_BaseSensor):
    """Senzor informații ultima revizie."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Ultima revizie"
        self._attr_unique_id = f"{entry_id}_service"
        self._attr_icon = "mdi:oil"

    @property
    def state(self):
        return self._data.get(CONF_DATA_REVIZIE) or "Nu a fost efectuată"

    @property
    def extra_state_attributes(self):
        return {
            "km_la_revizie": self._data.get(CONF_KM_REVIZIE),
            "schimb_ulei": "Da" if self._data.get(CONF_SCHIMB_ULEI) else "Nu",
            "schimb_filtru_ulei": "Da" if self._data.get(CONF_SCHIMB_FILTRU_ULEI) else "Nu",
            "schimb_filtru_aer": "Da" if self._data.get(CONF_SCHIMB_FILTRU_AER) else "Nu",
            "schimb_filtru_combustibil": "Da" if self._data.get(CONF_SCHIMB_FILTRU_COMBUSTIBIL) else "Nu",
        }


class ServiceKmSensor(_BaseSensor):
    """Senzor kilometri de la ultima revizie."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Km de la revizie"
        self._attr_unit_of_measurement = "km"
        self._attr_unique_id = f"{entry_id}_service_km"
        self._attr_icon = "mdi:counter"

    @property
    def state(self):
        current_km = self._data.get(CONF_KM_CURENTI, 0)
        service_km = self._data.get(CONF_KM_REVIZIE, 0)
        if not service_km:
            return None
        return max(0, current_km - service_km)


class ServiceDaysSensor(_BaseSensor):
    """Senzor zile de la ultima revizie."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Zile de la revizie"
        self._attr_unit_of_measurement = "zile"
        self._attr_unique_id = f"{entry_id}_service_days"
        self._attr_icon = "mdi:calendar-range"

    @property
    def state(self):
        service_date = parse_date(self._data.get(CONF_DATA_REVIZIE))
        if service_date is None:
            return None
        return (date.today() - service_date).days


class ServiceRecommendationSensor(_BaseSensor):
    """Senzor recomandare revizie."""

    def __init__(self, data, entry_id):
        super().__init__(data, entry_id)
        self._attr_name = f"{data[CONF_NUME_AUTO]} Recomandare revizie"
        self._attr_unique_id = f"{entry_id}_service_recommendation"
        self._attr_icon = "mdi:tooltip-account"

    def _compute(self) -> dict:
        """Calculează km_diff, days_diff și recomandarea. Returnează un dict."""
        current_km = self._data.get(CONF_KM_CURENTI, 0)
        service_km = self._data.get(CONF_KM_REVIZIE, 0)
        service_date = parse_date(self._data.get(CONF_DATA_REVIZIE))

        if not service_km or service_date is None:
            return {
                "recommendation": "Revizie neefectuată",
                "km_diff": None,
                "days_diff": None,
            }

        km_diff = current_km - service_km
        days_diff = (date.today() - service_date).days

        # Determinăm recomandarea — km are prioritate față de timp
        if km_diff >= REVIZIE_KM_PRAG:
            rec = "Revizie necesară (kilometraj)"
        elif days_diff >= REVIZIE_ZILE_PRAG:
            rec = "Revizie necesară (timp)"
        elif km_diff >= REVIZIE_KM_AVERTISMENT:
            rec = "Aproape de revizie (kilometraj)"
        elif days_diff >= REVIZIE_ZILE_AVERTISMENT:
            rec = "Aproape de revizie (timp)"
        else:
            rec = "În regulă"

        return {
            "recommendation": rec,
            "km_diff": km_diff,
            "days_diff": days_diff,
        }

    @property
    def state(self):
        return self._compute()["recommendation"]

    @property
    def extra_state_attributes(self):
        # FIX: înlocuit self.state_value (inexistent) cu calcul corect din _compute()
        c = self._compute()
        km_diff = c["km_diff"]
        days_diff = c["days_diff"]

        km_pana = (
            max(0, REVIZIE_KM_PRAG - km_diff) if km_diff is not None else "N/A"
        )
        zile_pana = (
            max(0, REVIZIE_ZILE_PRAG - days_diff) if days_diff is not None else "N/A"
        )

        return {
            "km_pana_la_revizie": km_pana,
            "zile_pana_la_revizie": zile_pana,
        }
