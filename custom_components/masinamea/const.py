"""Constante pentru integrarea Mașina Mea."""
from homeassistant.const import Platform
from datetime import datetime

DOMAIN = "masinamea"
PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]

# Constante configurare
CONF_NUME_AUTO = "nume_auto"
CONF_NR_INMATRICULARE = "nr_inmatriculare"
CONF_MARCA = "marca"
CONF_MODEL = "model"
CONF_CAPACITATE_CILINDRICA = "capacitate_cilindrica"
CONF_KM_CURENTI = "km_curenti"
CONF_DATA_INREGISTRARE_KM = "data_inregistrare_km"

# ITP
CONF_DATA_ITP = "data_itp"
CONF_ITP_EXPIRA = "itp_expira"

# Rovinietă
CONF_DATA_ROVINIETA = "data_rovinieta"
CONF_ROVINIETA_EXPIRA = "rovinieta_expira"

# Revizie
CONF_DATA_REVIZIE = "data_revizie"
CONF_KM_REVIZIE = "km_revizie"
CONF_SCHIMB_ULEI = "schimb_ulei"
CONF_SCHIMB_FILTRU_ULEI = "schimb_filtru_ulei"
CONF_SCHIMB_FILTRU_AER = "schimb_filtru_aer"
CONF_SCHIMB_FILTRU_COMBUSTIBIL = "schimb_filtru_combustibil"
CONF_OBSERVATII_REVIZIE = "observatii_revizie"

# Stări senzori
STATE_ACTIV = "activ"
STATE_EXPIRAT = "expirat"
STATE_APROAPE_EXPIRARE = "aproape_expirare"

# Praguri expirare
ITP_PRAG_AVERTISMENT = 30       # 30 zile
ROVINIETA_PRAG_AVERTISMENT = 7  # 7 zile
PRAG_URGENT = 2                 # 2 zile

# Praguri revizie
REVIZIE_KM_PRAG = 10000         # km
REVIZIE_KM_AVERTISMENT = 8000   # km
REVIZIE_ZILE_PRAG = 365         # 1 an
REVIZIE_ZILE_AVERTISMENT = 300  # ~10 luni


def parse_date(date_str: str | None):
    """Convertește data din format DD.MM.YYYY în obiect date.
    
    Funcție centralizată — folosită în sensor.py, calendar.py și __init__.py.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        return None
