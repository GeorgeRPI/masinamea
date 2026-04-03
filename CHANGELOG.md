# Changelog — Mașina Mea

Toate modificările notabile ale acestui proiect sunt documentate în acest fișier.
Formatul urmează [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/),
iar versionarea respectă [Semantic Versioning](https://semver.org/).

---

## [1.1.0] - 2025-04-03

### Adăugat
- **Senzori RCA (Asigurare obligatorie):**
  - `RCA Status` — activ / aproape_expirare / urgent / expirat
  - `RCA Expiră în` — numărul de zile rămase (unitate: zile)
  - `RCA Urgență` — ok / avertizare / urgent / critic
- **Serviciu `masinamea.update_rca`** — actualizează data de intrare în vigoare și data de expirare a RCA direct din HA sau din automatizări
- **Evenimente calendar pentru RCA:**
  - Eveniment în ziua expirării RCA
  - Reminder cu 30 de zile înainte de expirarea RCA
- Câmpuri RCA (`data_rca`, `rca_expira`) în formularul de configurare și Options Flow
- Câmpuri RCA în `strings.json` și `services.yaml`

---

## [1.0.1] - 2025-04-03

### Remediat
- **Bug critic:** `AttributeError: 'ServiceRecommendationSensor' has no attribute 'state_value'` — înlocuit cu metoda `_compute()`
- **Bug critic:** Typo `"averizare"` corectat în `"avertizare"` în senzorii de urgență ITP și Rovinietă
- **Bug critic:** Typo `GeprgeRPI` corectat în `GeorgeRPI` în `manifest.json`
- **Bug:** Proprietatea `event` din `CarCalendar` returna un `dict` în loc de `CalendarEvent`
- **Bug:** Serviciile din `services.yaml` nu aveau handlere Python implementate
- **Bug:** `OptionsFlow` nu actualiza `hass.data` — modificările nu erau vizibile fără reload manual

### Îmbunătățit
- Funcția `parse_date()` centralizată în `const.py`
- `unique_id` include `entry_id` — suport corect pentru mai multe mașini
- Clasă de bază `_BaseSensor` elimină codul duplicat
- Serviciile acceptă parametrul opțional `entry_id` pentru suport multi-mașină
- `__init__.py` combină `entry.data` cu `entry.options` la încărcare

---

## [1.0.0] - 2024-04-02

### Adăugat
- Lansare inițială a integrării
- 14 senzori: ITP, Rovinietă, Revizii, Kilometraj, Informații generale
- Calendar cu evenimente și reminder-uri automate
- Servicii: `update_km`, `update_itp`, `update_rovinieta`, `update_revizie`, `update_plate`
- Suport complet limba română
- Culori dinamice: activ / aproape expirare / urgent / expirat
- Validare format dată `DD.MM.YYYY` și număr de înmatriculare românesc
- Config Flow și Options Flow
- Suport HACS
