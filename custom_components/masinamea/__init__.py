"""Inițializare integrare Mașina Mea."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import Platform
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
    DOMAIN,
    PLATFORMS,
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
    CONF_NR_INMATRICULARE,
    parse_date,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurează integrarea din config entry."""
    hass.data.setdefault(DOMAIN, {})
    # Combinăm entry.data cu entry.options (options suprascrie data)
    hass.data[DOMAIN][entry.entry_id] = {**entry.data, **entry.options}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # ------------------------------------------------------------------ #
    # Înregistrare servicii                                                #
    # ------------------------------------------------------------------ #

    def _update_entry_data(entry: ConfigEntry, new_fields: dict) -> None:
        """Actualizează câmpuri în config entry și reîncarcă senzorii."""
        updated_data = {**entry.data, **entry.options, **new_fields}
        hass.config_entries.async_update_entry(entry, data=updated_data, options={})
        hass.data[DOMAIN][entry.entry_id] = updated_data

    async def handle_update_km(call: ServiceCall) -> None:
        """Actualizează kilometrajul curent."""
        km = call.data.get("km")
        entry_id = call.data.get("entry_id")
        entry = _get_entry(entry_id)
        if entry is None:
            _LOGGER.error("Nu s-a găsit integrarea cu entry_id: %s", entry_id)
            return
        _update_entry_data(entry, {CONF_KM_CURENTI: km})
        await hass.config_entries.async_reload(entry.entry_id)

    async def handle_update_itp(call: ServiceCall) -> None:
        """Actualizează datele ITP."""
        data_efectuare = call.data.get("data_efectuare")
        data_expirare = call.data.get("data_expirare")
        entry_id = call.data.get("entry_id")
        entry = _get_entry(entry_id)
        if entry is None:
            _LOGGER.error("Nu s-a găsit integrarea cu entry_id: %s", entry_id)
            return
        if parse_date(data_efectuare) is None or parse_date(data_expirare) is None:
            _LOGGER.error("Date ITP invalide: %s / %s", data_efectuare, data_expirare)
            return
        _update_entry_data(entry, {
            CONF_DATA_ITP: data_efectuare,
            CONF_ITP_EXPIRA: data_expirare,
        })
        await hass.config_entries.async_reload(entry.entry_id)

    async def handle_update_rovinieta(call: ServiceCall) -> None:
        """Actualizează datele rovinietei."""
        data_achizitie = call.data.get("data_achizitie")
        data_expirare = call.data.get("data_expirare")
        entry_id = call.data.get("entry_id")
        entry = _get_entry(entry_id)
        if entry is None:
            _LOGGER.error("Nu s-a găsit integrarea cu entry_id: %s", entry_id)
            return
        if parse_date(data_achizitie) is None or parse_date(data_expirare) is None:
            _LOGGER.error("Date rovinietă invalide: %s / %s", data_achizitie, data_expirare)
            return
        _update_entry_data(entry, {
            CONF_DATA_ROVINIETA: data_achizitie,
            CONF_ROVINIETA_EXPIRA: data_expirare,
        })
        await hass.config_entries.async_reload(entry.entry_id)

    async def handle_update_revizie(call: ServiceCall) -> None:
        """Înregistrează o nouă revizie."""
        data = call.data.get("data")
        km = call.data.get("km")
        entry_id = call.data.get("entry_id")
        entry = _get_entry(entry_id)
        if entry is None:
            _LOGGER.error("Nu s-a găsit integrarea cu entry_id: %s", entry_id)
            return
        if parse_date(data) is None:
            _LOGGER.error("Dată revizie invalidă: %s", data)
            return
        _update_entry_data(entry, {
            CONF_DATA_REVIZIE: data,
            CONF_KM_REVIZIE: km,
            CONF_SCHIMB_ULEI: call.data.get("schimb_ulei", False),
            CONF_SCHIMB_FILTRU_ULEI: call.data.get("schimb_filtru_ulei", False),
            CONF_SCHIMB_FILTRU_AER: call.data.get("schimb_filtru_aer", False),
            CONF_SCHIMB_FILTRU_COMBUSTIBIL: call.data.get("schimb_filtru_combustibil", False),
        })
        await hass.config_entries.async_reload(entry.entry_id)

    async def handle_update_plate(call: ServiceCall) -> None:
        """Actualizează numărul de înmatriculare."""
        numar = call.data.get("numar", "").upper().strip()
        entry_id = call.data.get("entry_id")
        entry = _get_entry(entry_id)
        if entry is None:
            _LOGGER.error("Nu s-a găsit integrarea cu entry_id: %s", entry_id)
            return
        _update_entry_data(entry, {CONF_NR_INMATRICULARE: numar})
        await hass.config_entries.async_reload(entry.entry_id)

    def _get_entry(entry_id: str | None) -> ConfigEntry | None:
        """Returnează prima intrare dacă entry_id lipsește, altfel caută după ID."""
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            return None
        if not entry_id:
            return entries[0]
        for e in entries:
            if e.entry_id == entry_id:
                return e
        return None

    # Schema servicii (entry_id opțional — util când ai o singură mașină)
    ENTRY_ID_SCHEMA = vol.Optional("entry_id")

    hass.services.async_register(
        DOMAIN, "update_km",
        handle_update_km,
        schema=vol.Schema({
            ENTRY_ID_SCHEMA: str,
            vol.Required("km"): vol.All(int, vol.Range(min=0, max=1_000_000)),
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_itp",
        handle_update_itp,
        schema=vol.Schema({
            ENTRY_ID_SCHEMA: str,
            vol.Required("data_efectuare"): str,
            vol.Required("data_expirare"): str,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_rovinieta",
        handle_update_rovinieta,
        schema=vol.Schema({
            ENTRY_ID_SCHEMA: str,
            vol.Required("data_achizitie"): str,
            vol.Required("data_expirare"): str,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_revizie",
        handle_update_revizie,
        schema=vol.Schema({
            ENTRY_ID_SCHEMA: str,
            vol.Required("data"): str,
            vol.Required("km"): vol.All(int, vol.Range(min=0, max=1_000_000)),
            vol.Optional("schimb_ulei", default=False): bool,
            vol.Optional("schimb_filtru_ulei", default=False): bool,
            vol.Optional("schimb_filtru_aer", default=False): bool,
            vol.Optional("schimb_filtru_combustibil", default=False): bool,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_plate",
        handle_update_plate,
        schema=vol.Schema({
            ENTRY_ID_SCHEMA: str,
            vol.Required("numar"): str,
        }),
    )

    # Ascultă modificările din Options Flow și reîncarcă
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reîncarcă integrarea când opțiunile se schimbă."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarcă integrarea."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
