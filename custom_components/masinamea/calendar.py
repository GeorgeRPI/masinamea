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
    ROVINIETA_PRAG_AVERTISMENT,
    parse_date,  # FIX: funcție centralizată din const.py
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Configurează calendarul."""
    # FIX: citim din hass.data (include și options) în loc de config_entry.data direct
    data = hass.data[DOMAIN][config_entry.entry_id]
    entry_id = config_entry.entry_id
    async_add_entities([CarCalendar(data, entry_id)], True)


class CarCalendar(CalendarEntity):
    """Calendar cu evenimentele mașinii."""

    def __init__(self, data: dict, entry_id: str):
        self._data = data
        self._entry_id = entry_id
        self._attr_name = f"{data[CONF_NUME_AUTO]} Calendar"
        # FIX: unique_id include entry_id
        self._attr_unique_id = f"{entry_id}_calendar"

    # ------------------------------------------------------------------ #
    # Proprietatea "event" — FIX: returnează CalendarEvent, nu dict       #
    # ------------------------------------------------------------------ #

    @property
    def event(self) -> CalendarEvent | None:
        """Returnează cel mai apropiat eveniment viitor."""
        today = date.today()
        today_dt = datetime.combine(today, datetime.min.time())
        far_future = today_dt + timedelta(days=365 * 5)

        # Obținem evenimentele din intervalul de azi până în 5 ani
        events = self._build_events(today_dt, far_future)
        if not events:
            return None
        # Sortăm și returnăm primul eveniment viitor
        events.sort(key=lambda e: e.start)
        return events[0]

    # ------------------------------------------------------------------ #
    # async_get_events — interfața oficială HA                            #
    # ------------------------------------------------------------------ #

    async def async_get_events(
        self,
        hass,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Returnează evenimentele dintr-un interval."""
        return self._build_events(start_date, end_date)

    # ------------------------------------------------------------------ #
    # Construire evenimente                                               #
    # ------------------------------------------------------------------ #

    def _build_events(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Construiește lista de CalendarEvent pentru intervalul dat."""
        events: list[CalendarEvent] = []
        nr = self._data.get(CONF_NR_INMATRICULARE, "Necunoscut")
        name = self._data.get(CONF_NUME_AUTO, "Mașina mea")

        def in_range(d: date) -> bool:
            """Verifică dacă o dată se află în intervalul cerut."""
            return start_date.date() <= d <= end_date.date()

        def make_event(d: date, summary: str, description: str) -> CalendarEvent:
            return CalendarEvent(
                start=d,
                end=d + timedelta(days=1),
                summary=summary,
                description=description,
            )

        # --- ITP: expirare ---
        itp_expiry = parse_date(self._data.get(CONF_ITP_EXPIRA))
        if itp_expiry:
            if in_range(itp_expiry):
                events.append(make_event(
                    itp_expiry,
                    f"ITP expiră — {name}",
                    f"ITP-ul expiră pe {itp_expiry.strftime('%d.%m.%Y')}.\n"
                    f"Programează o inspecție tehnică periodică.\n"
                    f"Nr. înmatriculare: {nr}",
                ))
            # ITP: reminder cu ITP_PRAG_AVERTISMENT zile înainte
            reminder_itp = itp_expiry - timedelta(days=ITP_PRAG_AVERTISMENT)
            if in_range(reminder_itp):
                events.append(make_event(
                    reminder_itp,
                    f"Reminder: ITP expiră în {ITP_PRAG_AVERTISMENT} zile — {name}",
                    f"ITP-ul expiră pe {itp_expiry.strftime('%d.%m.%Y')}.\n"
                    f"Programează inspecția tehnică periodică.\n"
                    f"Nr. înmatriculare: {nr}",
                ))

        # --- Rovinietă: expirare ---
        rov_expiry = parse_date(self._data.get(CONF_ROVINIETA_EXPIRA))
        if rov_expiry:
            if in_range(rov_expiry):
                events.append(make_event(
                    rov_expiry,
                    f"Rovinieta expiră — {name}",
                    f"Rovinieta expiră pe {rov_expiry.strftime('%d.%m.%Y')}.\n"
                    f"Achiziționează o nouă rovinietă.\n"
                    f"Nr. înmatriculare: {nr}",
                ))
            # Rovinietă: reminder cu ROVINIETA_PRAG_AVERTISMENT zile înainte
            reminder_rov = rov_expiry - timedelta(days=ROVINIETA_PRAG_AVERTISMENT)
            if in_range(reminder_rov):
                events.append(make_event(
                    reminder_rov,
                    f"Reminder: Rovinieta expiră în {ROVINIETA_PRAG_AVERTISMENT} zile — {name}",
                    f"Rovinieta expiră pe {rov_expiry.strftime('%d.%m.%Y')}.\n"
                    f"Achiziționează o nouă rovinietă.\n"
                    f"Nr. înmatriculare: {nr}",
                ))

        # --- Revizie: reminder la 6 luni după ultima revizie ---
        service_date = parse_date(self._data.get(CONF_DATA_REVIZIE))
        if service_date:
            reminder_service = service_date + timedelta(days=180)
            if in_range(reminder_service):
                events.append(make_event(
                    reminder_service,
                    f"Revizie recomandată — {name}",
                    f"Au trecut 6 luni de la ultima revizie "
                    f"({service_date.strftime('%d.%m.%Y')}).\n"
                    f"Verifică starea mașinii.\n"
                    f"Nr. înmatriculare: {nr}",
                ))

        return events
