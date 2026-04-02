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
    CONF_SCHIMB_FILTRU_COMBUSTIBIL
)

def validate_date(date_str):
    """Validează data în format DD.MM.YYYY."""
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def validate_plate(plate_str):
    """Validează numărul de înmatriculare românesc."""
    if not plate_str:
        return True
    # Format românesc: B 123 ABC, B-123-ABC, B123ABC, etc.
    pattern = r'^[A-Z]{1,2}[-\s]?[0-9]{1,3}[-\s]?[A-Z]{1,3}$'
    return bool(re.match(pattern, plate_str.upper()))

class MasinaMeaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pentru Mașina Mea."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Primul pas de configurare."""
        errors = {}

        if user_input is not None:
            # Validare date
            errors = {}
            
            # Validare număr înmatriculare
            if user_input.get(CONF_NR_INMATRICULARE):
                if not validate_plate(user_input[CONF_NR_INMATRICULARE]):
                    errors[CONF_NR_INMATRICULARE] = "invalid_plate"
            
            # Validare date
            if user_input.get(CONF_DATA_ITP) and not validate_date(user_input[CONF_DATA_ITP]):
                errors[CONF_DATA_ITP] = "invalid_date"
            if user_input.get(CONF_ITP_EXPIRA) and not validate_date(user_input[CONF_ITP_EXPIRA]):
                errors[CONF_ITP_EXPIRA] = "invalid_date"
            if user_input.get(CONF_DATA_ROVINIETA) and not validate_date(user_input[CONF_DATA_ROVINIETA]):
                errors[CONF_DATA_ROVINIETA] = "invalid_date"
            if user_input.get(CONF_ROVINIETA_EXPIRA) and not validate_date(user_input[CONF_ROVINIETA_EXPIRA]):
                errors[CONF_ROVINIETA_EXPIRA] = "invalid_date"
            if user_input.get(CONF_DATA_REVIZIE) and not validate_date(user_input[CONF_DATA_REVIZIE]):
                errors[CONF_DATA_REVIZIE] = "invalid_date"

            if not errors:
                # Formatează numărul de înmatriculare
                if user_input.get(CONF_NR_INMATRICULARE):
                    user_input[CONF_NR_INMATRICULARE] = user_input[CONF_NR_INMATRICULARE].upper().strip()
                
                return self.async_create_entry(
                    title=user_input[CONF_NUME_AUTO], 
                    data=user_input
                )

        # Schema configurare
        data_schema = vol.Schema({
            vol.Required(CONF_NUME_AUTO, default="Mașina mea"): str,
            vol.Optional(CONF_NR_INMATRICULARE, default=""): str,
            vol.Required(CONF_MARCA, default=""): str,
            vol.Required(CONF_MODEL, default=""): str,
            vol.Optional(CONF_CAPACITATE_CILINDRICA, default=""): str,
            vol.Required(CONF_KM_CURENTI, default=0): int,
            vol.Optional(CONF_DATA_ITP, default=""): str,
            vol.Optional(CONF_ITP_EXPIRA, default=""): str,
            vol.Optional(CONF_DATA_ROVINIETA, default=""): str,
            vol.Optional(CONF_ROVINIETA_EXPIRA, default=""): str,
            vol.Optional(CONF_DATA_REVIZIE, default=""): str,
            vol.Optional(CONF_KM_REVIZIE, default=0): int,
            vol.Optional(CONF_SCHIMB_ULEI, default=False): bool,
            vol.Optional(CONF_SCHIMB_FILTRU_ULEI, default=False): bool,
            vol.Optional(CONF_SCHIMB_FILTRU_AER, default=False): bool,
            vol.Optional(CONF_SCHIMB_FILTRU_COMBUSTIBIL, default=False): bool,
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Returnează opțiunile flow."""
        return MasinaMeaOptionsFlow(config_entry)


class MasinaMeaOptionsFlow(config_entries.OptionsFlow):
    """Opțiuni configurare pentru Mașina Mea."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Gestionare opțiuni."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Preia valorile existente
        options = {
            CONF_NUME_AUTO: self.config_entry.data.get(CONF_NUME_AUTO),
            CONF_NR_INMATRICULARE: self.config_entry.data.get(CONF_NR_INMATRICULARE, ""),
            CONF_MARCA: self.config_entry.data.get(CONF_MARCA),
            CONF_MODEL: self.config_entry.data.get(CONF_MODEL),
            CONF_CAPACITATE_CILINDRICA: self.config_entry.data.get(CONF_CAPACITATE_CILINDRICA),
            CONF_KM_CURENTI: self.config_entry.data.get(CONF_KM_CURENTI),
            CONF_DATA_ITP: self.config_entry.data.get(CONF_DATA_ITP),
            CONF_ITP_EXPIRA: self.config_entry.data.get(CONF_ITP_EXPIRA),
            CONF_DATA_ROVINIETA: self.config_entry.data.get(CONF_DATA_ROVINIETA),
            CONF_ROVINIETA_EXPIRA: self.config_entry.data.get(CONF_ROVINIETA_EXPIRA),
            CONF_DATA_REVIZIE: self.config_entry.data.get(CONF_DATA_REVIZIE),
            CONF_KM_REVIZIE: self.config_entry.data.get(CONF_KM_REVIZIE),
            CONF_SCHIMB_ULEI: self.config_entry.data.get(CONF_SCHIMB_ULEI, False),
            CONF_SCHIMB_FILTRU_ULEI: self.config_entry.data.get(CONF_SCHIMB_FILTRU_ULEI, False),
            CONF_SCHIMB_FILTRU_AER: self.config_entry.data.get(CONF_SCHIMB_FILTRU_AER, False),
            CONF_SCHIMB_FILTRU_COMBUSTIBIL: self.config_entry.data.get(CONF_SCHIMB_FILTRU_COMBUSTIBIL, False),
        }

        data_schema = vol.Schema({
            vol.Required(CONF_NUME_AUTO, default=options[CONF_NUME_AUTO]): str,
            vol.Optional(CONF_NR_INMATRICULARE, default=options[CONF_NR_INMATRICULARE]): str,
            vol.Required(CONF_MARCA, default=options[CONF_MARCA]): str,
            vol.Required(CONF_MODEL, default=options[CONF_MODEL]): str,
            vol.Optional(CONF_CAPACITATE_CILINDRICA, default=options[CONF_CAPACITATE_CILINDRICA]): str,
            vol.Required(CONF_KM_CURENTI, default=options[CONF_KM_CURENTI]): int,
            vol.Optional(CONF_DATA_ITP, default=options[CONF_DATA_ITP]): str,
            vol.Optional(CONF_ITP_EXPIRA, default=options[CONF_ITP_EXPIRA]): str,
            vol.Optional(CONF_DATA_ROVINIETA, default=options[CONF_DATA_ROVINIETA]): str,
            vol.Optional(CONF_ROVINIETA_EXPIRA, default=options[CONF_ROVINIETA_EXPIRA]): str,
            vol.Optional(CONF_DATA_REVIZIE, default=options[CONF_DATA_REVIZIE]): str,
            vol.Optional(CONF_KM_REVIZIE, default=options[CONF_KM_REVIZIE]): int,
            vol.Optional(CONF_SCHIMB_ULEI, default=options[CONF_SCHIMB_ULEI]): bool,
            vol.Optional(CONF_SCHIMB_FILTRU_ULEI, default=options[CONF_SCHIMB_FILTRU_ULEI]): bool,
            vol.Optional(CONF_SCHIMB_FILTRU_AER, default=options[CONF_SCHIMB_FILTRU_AER]): bool,
            vol.Optional(CONF_SCHIMB_FILTRU_COMBUSTIBIL, default=options[CONF_SCHIMB_FILTRU_COMBUSTIBIL]): bool,
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
