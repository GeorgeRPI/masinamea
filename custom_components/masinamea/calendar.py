"""Calendar pentru integrarea Mașina Mea."""
from datetime import datetime, timedelta, date
from homeassistant.components.calendar import CalendarEntity, CalendarEvent

from .const import (
    DOMAIN,
    CONF_NUME_AUTO,
    CONF_NR_INMATRICULARE,
    CONF_ITP_EXPIRA,
    CONF_ROVINIETA_EXPIRA,
    CONF_DATA_REVIZIE,
    ITP_PRAG_AVERTISMENT,
    ROVINIETA_PRAG_AVERTISMENT
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
    """Configurează calendarul."""
    data = config_entry.data
    async_add_entities([CarCalendar(data)], True)


class CarCalendar(CalendarEntity):
    """Calendar cu evenimentele mașinii."""

    def __init__(self, data):
        self._data = data
        self._attr_name = f"{data[CONF_NUME_AUTO]} Calendar"
        self._attr_unique_id = f"{data[CONF_NUME_AUTO]}_calendar"

    @property
    def event(self):
        """Returnează următorul eveniment."""
        events = self._get_events()
        if events:
            return events[0]
        return None

    async def async_get_events(self, hass, start_date, end_date):
        """Returnează evenimentele dintr-un interval."""
        events = []
        
        # Adaugă eveniment ITP
        itp_expiry_str = self._data.get(CONF_ITP_EXPIRA)
        if itp_expiry_str:
            expiry_date = parse_date(itp_expiry_str)
            if expiry_date:
                if start_date.date() <= expiry_date <= end_date.date():
                    events.append(CalendarEvent(
                        start=expiry_date,
                        end=expiry_date + timedelta(days=1),
                        summary=f"ITP expiră pentru {self._data.get(CONF_NUME_AUTO)}",
                        description=f"ITP-ul expiră pe {expiry_date.strftime('%d.%m.%Y')}. Programează o inspecție tehnică periodică.\n\nNumăr înmatriculare: {self._data.get(CONF_NR_INMATRICULARE, 'Necunoscut')}"
                    ))
        
        # Adaugă eveniment Rovinietă
        rovinieta_expiry_str = self._data.get(CONF_ROVINIETA_EXPIRA)
        if rovinieta_expiry_str:
            expiry_date = parse_date(rovinieta_expiry_str)
            if expiry_date:
                if start_date.date() <= expiry_date <= end_date.date():
                    events.append(CalendarEvent(
                        start=expiry_date,
                        end=expiry_date + timedelta(days=1),
                        summary=f"Rovinieta expiră pentru {self._data.get(CONF_NUME_AUTO)}",
                        description=f"Rovinieta expiră pe {expiry_date.strftime('%d.%m.%Y')}. Achiziționează o nouă rovinietă.\n\nNumăr înmatriculare: {self._data.get(CONF_NR_INMATRICULARE, 'Necunoscut')}"
                    ))
        
        # Adaugă reminder revizie (la 6 luni după ultima revizie)
        service_date_str = self._data.get(CONF_DATA_REVIZIE)
        if service_date_str:
            service_date = parse_date(service_date_str)
            if service_date:
                reminder_date = service_date + timedelta(days=180)  # 6 luni
                if start_date.date() <= reminder_date <= end_date.date():
                    events.append(CalendarEvent(
                        start=reminder_date,
                        end=reminder_date + timedelta(days=1),
                        summary=f"Revizie recomandată pentru {self._data.get(CONF_NUME_AUTO)}",
                        description=f"Au trecut 6 luni de la ultima revizie ({service_date.strftime('%d.%m.%Y')}). Verifică starea mașinii.\n\nNumăr înmatriculare: {self._data.get(CONF_NR_INMATRICULARE, 'Necunoscut')}"
                    ))
        
        # Adaugă reminder ITP (cu 30 zile înainte)
        itp_expiry_str = self._data.get(CONF_ITP_EXPIRA)
        if itp_expiry_str:
            expiry_date = parse_date(itp_expiry_str)
            if expiry_date:
                reminder_date = expiry_date - timedelta(days=ITP_PRAG_AVERTISMENT)
                if start_date.date() <= reminder_date <= end_date.date():
                    events.append(CalendarEvent(
                        start=reminder_date,
                        end=reminder_date + timedelta(days=1),
                        summary=f"ITP expiră în {ITP_PRAG_AVERTISMENT} zile",
                        description=f"ITP-ul expiră pe {expiry_date.strftime('%d.%m.%Y')}. Programează inspecția tehnică periodică.\n\nNumăr înmatriculare: {self._data.get(CONF_NR_INMATRICULARE, 'Necunoscut')}"
                    ))
        
        # Adaugă reminder Rovinietă (cu 7 zile înainte)
        rovinieta_expiry_str = self._data.get(CONF_ROVINIETA_EXPIRA)
        if rovinieta_expiry_str:
            expiry_date = parse_date(rovinieta_expiry_str)
            if expiry_date:
                reminder_date = expiry_date - timedelta(days=ROVINIETA_PRAG_AVERTISMENT)
                if start_date.date() <= reminder_date <= end_date.date():
                    events.append(CalendarEvent(
                        start=reminder_date,
                        end=reminder_date + timedelta(days=1),
                        summary=f"Rovinieta expiră în {ROVINIETA_PRAG_AVERTISMENT} zile",
                        description=f"Rovinieta expiră pe {expiry_date.strftime('%d.%m.%Y')}. Achiziționează o nouă rovinietă.\n\nNumăr înmatriculare: {self._data.get(CONF_NR_INMATRICULARE, 'Necunoscut')}"
                    ))
        
        return events

    def _get_events(self):
        """Returnează toate evenimentele viitoare."""
        events = []
        today = date.today()
        
        # ITP
        itp_expiry_str = self._data.get(CONF_ITP_EXPIRA)
        if itp_expiry_str:
            expiry_date = parse_date(itp_expiry_str)
            if expiry_date and expiry_date >= today:
                events.append({
                    "start": expiry_date,
                    "summary": f"ITP expiră pentru {self._data.get(CONF_NUME_AUTO)}",
                    "days_left": (expiry_date - today).days
                })
        
        # Rovinietă
        rovinieta_expiry_str = self._data.get(CONF_ROVINIETA_EXPIRA)
        if rovinieta_expiry_str:
            expiry_date = parse_date(rovinieta_expiry_str)
            if expiry_date and expiry_date >= today:
                events.append({
                    "start": expiry_date,
                    "summary": f"Rovinieta expiră pentru {self._data.get(CONF_NUME_AUTO)}",
                    "days_left": (expiry_date - today).days
                })
        
        # Sortează după dată
        events.sort(key=lambda x: x["start"])
        return events
