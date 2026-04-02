"""Config flow pentru Mașina Mea."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from datetime import datetime
import re

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
)


def validate_date(date_str: str) -> bool:
    """Validează data în format DD.MM.YYYY."""
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def validate_plate(plate_str: str) -> bool:
    """Validează numărul de înmatriculare românesc."""
    if not plate_str:
        return True
    # Format românesc: B 123 ABC, B-123-ABC, B123ABC etc.
    pattern = r'^[A-Z]{1,2}[-\s]?[0-9]{1,3}[-\s]?[A-Z]{1,3}$'
    return bool(re.match(pattern, plate_str.upper()))


def _build_schema(defaults: dict) -> vol.Schema:
    """Construiește schema de validare cu valorile implicite date."""
    return vol.Schema({
        vol.Required(CONF_NUME_AUTO, default=defaults.get(CONF_NUME_AUTO, "Mașina mea")): str,
        vol.Optional(CONF_NR_INMATRICULARE, default=defaults.get(CONF_NR_INMATRICULARE, "")): str,
        vol.Required(CONF_MARCA, default=defaults.get(CONF_MARCA, "")): str,
        vol.Required(CONF_MODEL, default=defaults.get(CONF_MODEL, "")): str,
        vol.Optional(CONF_CAPACITATE_CILINDRICA, default=defaults.get(CONF_CAPACITATE_CILINDRICA, "")): str,
        vol.Required(CONF_KM_CURENTI, default=defaults.get(CONF_KM_CURENTI, 0)): int,
        vol.Optional(CONF_DATA_ITP, default=defaults.get(CONF_DATA_ITP, "")): str,
        vol.Optional(CONF_ITP_EXPIRA, default=defaults.get(CONF_ITP_EXPIRA, "")): str,
        vol.Optional(CONF_DATA_ROVINIETA, default=defaults.get(CONF_DATA_ROVINIETA, "")): str,
        vol.Optional(CONF_ROVINIETA_EXPIRA, default=defaults.get(CONF_ROVINIETA_EXPIRA, "")): str,
        vol.Optional(CONF_DATA_REVIZIE, default=defaults.get(CONF_DATA_REVIZIE, "")): str,
        vol.Optional(CONF_KM_REVIZIE, default=defaults.get(CONF_KM_REVIZIE, 0)): int,
        vol.Optional(CONF_SCHIMB_ULEI, default=defaults.get(CONF_SCHIMB_ULEI, False)): bool,
        vol.Optional(CONF_SCHIMB_FILTRU_ULEI, default=defaults.get(CONF_SCHIMB_FILTRU_ULEI, False)): bool,
        vol.Optional(CONF_SCHIMB_FILTRU_AER, default=defaults.get(CONF_SCHIMB_FILTRU_AER, False)): bool,
        vol.Optional(CONF_SCHIMB_FILTRU_COMBUSTIBIL, default=defaults.get(CONF_SCHIMB_FILTRU_COMBUSTIBIL, False)): bool,
    })


def _validate_user_input(user_input: dict) -> dict:
    """Validează inputul utilizatorului și returnează erorile găsite."""
    errors = {}

    if user_input.get(CONF_NR_INMATRICULARE):
        if not validate_plate(user_input[CONF_NR_INMATRICULARE]):
            errors[CONF_NR_INMATRICULARE] = "invalid_plate"

    date_fields = [CONF_DATA_ITP, CONF_ITP_EXPIRA, CONF_DATA_ROVINIETA, CONF_ROVINIETA_EXPIRA, CONF_DATA_REVIZIE]
    for field in date_fields:
        if user_input.get(field) and not validate_date(user_input[field]):
            errors[field] = "invalid_date"

    return errors


class MasinaMeaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pentru Mașina Mea."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Primul pas de configurare."""
        errors = {}

        if user_input is not None:
            errors = _validate_user_input(user_input)

            if not errors:
                # Normalizăm numărul de înmatriculare
                if user_input.get(CONF_NR_INMATRICULARE):
                    user_input[CONF_NR_INMATRICULARE] = user_input[CONF_NR_INMATRICULARE].upper().strip()

                return self.async_create_entry(
                    title=user_input[CONF_NUME_AUTO],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(user_input or {}),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Returnează options flow."""
        return MasinaMeaOptionsFlow(config_entry)


class MasinaMeaOptionsFlow(config_entries.OptionsFlow):
    """Opțiuni configurare pentru Mașina Mea."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Gestionare opțiuni."""
        errors = {}

        # Valorile curente = data + options existente (options suprascrie data)
        current = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            errors = _validate_user_input(user_input)

            if not errors:
                if user_input.get(CONF_NR_INMATRICULARE):
                    user_input[CONF_NR_INMATRICULARE] = user_input[CONF_NR_INMATRICULARE].upper().strip()

                # FIX: salvăm datele actualizate în entry.data (nu doar în options)
                # Astfel senzorii care citesc din hass.data[DOMAIN][entry_id] vor vedea
                # valorile noi după ce __init__.py merge data + options
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(current),
            errors=errors,
        )
