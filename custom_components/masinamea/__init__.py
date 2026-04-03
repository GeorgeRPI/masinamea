"""Inițializare integrare Mașina Mea."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
import voluptuous as vol

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_KM_CURENTI,
    CONF_DATA_ITP,
    CONF_ITP_EXPIRA,
    CONF_DATA_ROVINIETA,
    CONF_ROVINIETA_EXPIRA,
    CONF_DATA_RCA,
    CONF_RCA_EXPIRA,
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
    # Combinăm entry.data cu entry.options — options suprascrie data
    hass.data[DOMAIN][entry.entry_id] = {**entry.data, **entry.options}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # ------------------------------------------------------------------ #
    # Funcții ajutătoare                                                   #
    # ------------------------------------------------------------------ #

    def _get_entry(entry_id=None):
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

    def _update_entry_data(target_entry: ConfigEntry, new_fields: dict):
        """Actualizează câmpuri în config entry și sincronizează hass.data."""
        updated_data = {**target_entry.data, **target_entry.options, **new_fields}
        hass.config_entries.async_update_entry(target_entry, data=updated_data, options={})
        hass.data[DOMAIN][target_entry.entry_id] = updated_data

    # ------------------------------------------------------------------ #
    # Handlere servicii                                                    #
    # ------------------------------------------------------------------ #

    async def handle_update_km(call: ServiceCall):
        """Actualizează kilometrajul curent."""
        target = _get_entry(call.data.get("entry_id"))
        if target is None:
            _LOGGER.error("masinamea.update_km: integrare negăsită")
            return
        _update_entry_data(target, {CONF_KM_CURENTI: call.data["km"]})
        await hass.config_entries.async_reload(target.entry_id)

    async def handle_update_itp(call: ServiceCall):
        """Actualizează datele ITP."""
        target = _get_entry(call.data.get("entry_id"))
        if target is None:
            _LOGGER.error("masinamea.update_itp: integrare negăsită")
            return
        data_ef = call.data["data_efectuare"]
        data_ex = call.data["data_expirare"]
        if parse_date(data_ef) is None or parse_date(data_ex) is None:
            _LOGGER.error("masinamea.update_itp: date invalide %s / %s", data_ef, data_ex)
            return
        _update_entry_data(target, {CONF_DATA_ITP: data_ef, CONF_ITP_EXPIRA: data_ex})
        await hass.config_entries.async_reload(target.entry_id)

    async def handle_update_rovinieta(call: ServiceCall):
        """Actualizează datele rovinietei."""
        target = _get_entry(call.data.get("entry_id"))
        if target is None:
            _LOGGER.error("masinamea.update_rovinieta: integrare negăsită")
            return
        data_ach = call.data["data_achizitie"]
        data_ex = call.data["data_expirare"]
        if parse_date(data_ach) is None or parse_date(data_ex) is None:
            _LOGGER.error("masinamea.update_rovinieta: date invalide %s / %s", data_ach, data_ex)
            return
        _update_entry_data(target, {CONF_DATA_ROVINIETA: data_ach, CONF_ROVINIETA_EXPIRA: data_ex})
        await hass.config_entries.async_reload(target.entry_id)

    async def handle_update_rca(call: ServiceCall):
        """Actualizează datele RCA."""
        target = _get_entry(call.data.get("entry_id"))
        if target is None:
            _LOGGER.error("masinamea.update_rca: integrare negăsită")
            return
        data_vg = call.data["data_intrare_vigoare"]
        data_ex = call.data["data_expirare"]
        if parse_date(data_vg) is None or parse_date(data_ex) is None:
            _LOGGER.error("masinamea.update_rca: date invalide %s / %s", data_vg, data_ex)
            return
        _update_entry_data(target, {CONF_DATA_RCA: data_vg, CONF_RCA_EXPIRA: data_ex})
        await hass.config_entries.async_reload(target.entry_id)

    async def handle_update_revizie(call: ServiceCall):
        """Înregistrează o nouă revizie."""
        target = _get_entry(call.data.get("entry_id"))
        if target is None:
            _LOGGER.error("masinamea.update_revizie: integrare negăsită")
            return
        data_rev = call.data["data"]
        if parse_date(data_rev) is None:
            _LOGGER.error("masinamea.update_revizie: dată invalidă %s", data_rev)
            return
        _update_entry_data(target, {
            CONF_DATA_REVIZIE: data_rev,
            CONF_KM_REVIZIE: call.data["km"],
            CONF_SCHIMB_ULEI: call.data.get("schimb_ulei", False),
            CONF_SCHIMB_FILTRU_ULEI: call.data.get("schimb_filtru_ulei", False),
            CONF_SCHIMB_FILTRU_AER: call.data.get("schimb_filtru_aer", False),
            CONF_SCHIMB_FILTRU_COMBUSTIBIL: call.data.get("schimb_filtru_combustibil", False),
        })
        await hass.config_entries.async_reload(target.entry_id)

    async def handle_update_plate(call: ServiceCall):
        """Actualizează numărul de înmatriculare."""
        target = _get_entry(call.data.get("entry_id"))
        if target is None:
            _LOGGER.error("masinamea.update_plate: integrare negăsită")
            return
        _update_entry_data(target, {CONF_NR_INMATRICULARE: call.data["numar"].upper().strip()})
        await hass.config_entries.async_reload(target.entry_id)

    # ------------------------------------------------------------------ #
    # Înregistrare servicii                                                #
    # ------------------------------------------------------------------ #

    ENTRY_ID = vol.Optional("entry_id")
    KM_RANGE = vol.All(int, vol.Range(min=0, max=1_000_000))

    hass.services.async_register(
        DOMAIN, "update_km", handle_update_km,
        schema=vol.Schema({ENTRY_ID: str, vol.Required("km"): KM_RANGE}),
    )
    hass.services.async_register(
        DOMAIN, "update_itp", handle_update_itp,
        schema=vol.Schema({
            ENTRY_ID: str,
            vol.Required("data_efectuare"): str,
            vol.Required("data_expirare"): str,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_rovinieta", handle_update_rovinieta,
        schema=vol.Schema({
            ENTRY_ID: str,
            vol.Required("data_achizitie"): str,
            vol.Required("data_expirare"): str,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_rca", handle_update_rca,
        schema=vol.Schema({
            ENTRY_ID: str,
            vol.Required("data_intrare_vigoare"): str,
            vol.Required("data_expirare"): str,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_revizie", handle_update_revizie,
        schema=vol.Schema({
            ENTRY_ID: str,
            vol.Required("data"): str,
            vol.Required("km"): KM_RANGE,
            vol.Optional("schimb_ulei", default=False): bool,
            vol.Optional("schimb_filtru_ulei", default=False): bool,
            vol.Optional("schimb_filtru_aer", default=False): bool,
            vol.Optional("schimb_filtru_combustibil", default=False): bool,
        }),
    )
    hass.services.async_register(
        DOMAIN, "update_plate", handle_update_plate,
        schema=vol.Schema({ENTRY_ID: str, vol.Required("numar"): str}),
    )

    # Reîncarcă automat când se salvează din Options Flow
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Reîncarcă integrarea când opțiunile se schimbă din UI."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarcă integrarea."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
