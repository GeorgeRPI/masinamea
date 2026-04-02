# Changelog — Mașina Mea

Toate modificările notabile ale acestui proiect sunt documentate în acest fișier.
Formatul urmează [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/),
iar versionarea respectă [Semantic Versioning](https://semver.org/).

---

## [1.0.1] - 2025-04-03

### Remediat
- **Bug critic:** `AttributeError: 'ServiceRecommendationSensor' object has no attribute 'state_value'`
  — proprietatea inexistentă `self.state_value` înlocuită cu calcul corect în metoda `_compute()`
- **Bug critic:** Typo `"averizare"` corectat în `"avertizare"` în senzorii de urgență ITP și Rovinietă
  — automatizările care filtrau după această valoare eșuau silențios
- **Bug critic:** Typo `GeprgeRPI` corectat în `GeorgeRPI` în URL-ul de documentație din `manifest.json`
  — link-ul de documentație era mort în HACS
- **Bug:** Proprietatea `event` din `CarCalendar` returna un `dict` în loc de `CalendarEvent`
  — HA se așteaptă la un obiect `CalendarEvent` real
- **Bug:** Serviciile definite în `services.yaml` nu aveau handlere Python implementate
  — apelarea oricărui serviciu producea eroare
- **Bug:** `OptionsFlow` nu actualiza `hass.data`, deci modificările nu erau vizibile fără reload manual
  — adăugat `_async_update_listener` care reîncarcă integrarea automat

### Îmbunătățit
- Funcția `parse_date()` centralizată în `const.py` — eliminată duplicarea din `sensor.py` și `calendar.py`
- `unique_id` pentru toți senzorii și calendar include acum `entry_id`
  — suport corect pentru mai multe mașini cu același nume
- Adăugată clasa de bază `_BaseSensor` în `sensor.py` — elimină codul duplicat din senzorii de status
- Schema de validare și funcția de validare input extrase în funcții comune în `config_flow.py`
- Serviciile acceptă acum parametrul opțional `entry_id` pentru suport multi-mașină
- `__init__.py` combină `entry.data` cu `entry.options` la încărcare — date mereu sincronizate

---

## [1.0.0] - 2024-04-02

### Adăugat
- Lansare inițială a integrării
- Senzori pentru ITP, Rovinietă, Revizii, Kilometraj (14 senzori total)
- Calendar cu evenimente și reminder-uri automate
- Servicii pentru actualizare date: `update_km`, `update_itp`, `update_rovinieta`, `update_revizie`, `update_plate`
- Suport complet limba română
- Culori dinamice în funcție de status (activ / aproape expirare / urgent / expirat)
- Validare format dată `DD.MM.YYYY` și număr de înmatriculare românesc
- Config Flow și Options Flow pentru configurare din interfața HA
- Suport HACS
