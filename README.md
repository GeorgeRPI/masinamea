# 🚗 Mașina Mea — Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/v/release/GeorgeRPI/masinamea?style=flat-square)](https://github.com/GeorgeRPI/masinamea/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/Home_Assistant-2023.1%2B-blue?style=flat-square)](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/GeorgeRPI/masinamea?style=flat-square)](LICENSE)

Integrare locală pentru Home Assistant care îți permite să gestionezi toate datele importante ale mașinii tale direct din interfața HA: **ITP**, **Rovinietă**, **RCA**, **Revizii**, **Kilometraj** — cu notificări, calendar și senzori dinamici.

---

## ✨ Funcționalități

- 🔴🟡🟢 **Status dinamic** — culori în funcție de cât timp a mai rămas (activ / aproape expirare / urgent / expirat)
- ⏰ **Calendar integrat** — evenimente și reminder-uri automate pentru ITP, Rovinietă, RCA și Revizie
- 🔔 **Notificări proactive** — avertizare cu 30 zile înainte de expirarea ITP-ului și RCA, 7 zile pentru rovinietă
- 📊 **17 senzori** — date detaliate pentru fiecare categorie
- 🛠️ **Servicii HA** — actualizezi datele direct din interfață sau din automatizări, fără să reintri în configurare
- 🚗 **Multi-mașină** — poți adăuga mai multe mașini ca intrări separate
- 🇷🇴 **Interfață complet în română**

---

## 📦 Instalare

### Prin HACS (recomandat)

1. Deschide **HACS** în Home Assistant
2. Mergi la **Integrations → Custom repositories**
3. Adaugă URL-ul: `https://github.com/GeorgeRPI/masinamea` cu categoria `Integration`
4. Caută **Mașina Mea** și apasă **Download**
5. Restartează Home Assistant
6. Mergi la **Settings → Devices & Services → Add Integration** și caută **Mașina Mea**

### Manual

1. Descarcă ultima versiune din [Releases](https://github.com/GeorgeRPI/masinamea/releases)
2. Copiază folderul `custom_components/masinamea` în directorul `custom_components` al instalației tale HA
3. Restartează Home Assistant
4. Mergi la **Settings → Devices & Services → Add Integration** și caută **Mașina Mea**

---

## ⚙️ Configurare

La prima configurare vei completa un formular cu datele mașinii:

| Câmp | Obligatoriu | Descriere |
|------|:-----------:|-----------|
| Nume mașină | ✅ | Numele afișat în HA (ex: „Dacia Logan") |
| Număr înmatriculare | — | Format românesc, ex: `B 123 ABC` |
| Marcă / Model | ✅ | Ex: Dacia / Logan |
| Capacitate cilindrică | — | În cm³ |
| Kilometraj curent | ✅ | Valoarea de pe bord |
| Data ITP / Expirare ITP | — | Format `DD.MM.YYYY` |
| Data rovinietă / Expirare rovinietă | — | Format `DD.MM.YYYY` |
| Data de intrare în vigoare RCA / Expirare RCA | — | Format `DD.MM.YYYY` |
| Data ultimei revizii | — | Format `DD.MM.YYYY` |
| Km la ultima revizie | — | Kilometrajul la care s-a făcut revizia |
| Componente schimbate la revizie | — | Ulei, filtre (bifă) |

Poți modifica orice dată ulterior din **Settings → Devices & Services → Mașina Mea → Configure**.

---

## 📊 Senzori disponibili

| Senzor | Descriere |
|--------|-----------|
| `sensor.<nume>_informatii` | Marcă, model, nr. înmatriculare |
| `sensor.<nume>_numar_inmatriculare` | Numărul de înmatriculare |
| `sensor.<nume>_kilometraj` | Kilometraj curent (km) |
| `sensor.<nume>_capacitate_cilindrica` | Capacitate motor (cm³) |
| `sensor.<nume>_itp_status` | `activ` / `aproape_expirare` / `urgent` / `expirat` |
| `sensor.<nume>_itp_expira_in` | Zile până la expirarea ITP |
| `sensor.<nume>_itp_urgenta` | `ok` / `avertizare` / `urgent` / `critic` |
| `sensor.<nume>_rovinieta_status` | Status rovinietă |
| `sensor.<nume>_rovinieta_expira_in` | Zile până la expirarea rovinietei |
| `sensor.<nume>_rovinieta_urgenta` | Nivel urgență rovinietă |
| `sensor.<nume>_rca_status` | `activ` / `aproape_expirare` / `urgent` / `expirat` |
| `sensor.<nume>_rca_expira_in` | Zile până la expirarea RCA |
| `sensor.<nume>_rca_urgenta` | `ok` / `avertizare` / `urgent` / `critic` |
| `sensor.<nume>_ultima_revizie` | Data și detalii ultima revizie |
| `sensor.<nume>_km_de_la_revizie` | Km parcurși de la ultima revizie |
| `sensor.<nume>_zile_de_la_revizie` | Zile de la ultima revizie |
| `sensor.<nume>_recomandare_revizie` | Recomandare revizie (km / timp) |

---

## 🛠️ Servicii

Poți actualiza datele mașinii din **Developer Tools → Services** sau din automatizări.

### `masinamea.update_km`
```yaml
service: masinamea.update_km
data:
  km: 85000
```

### `masinamea.update_itp`
```yaml
service: masinamea.update_itp
data:
  data_efectuare: "15.03.2024"
  data_expirare: "15.03.2025"
```

### `masinamea.update_rovinieta`
```yaml
service: masinamea.update_rovinieta
data:
  data_achizitie: "01.01.2025"
  data_expirare: "31.12.2025"
```

### `masinamea.update_rca`
```yaml
service: masinamea.update_rca
data:
  data_intrare_vigoare: "01.01.2025"
  data_expirare: "31.12.2025"
```

### `masinamea.update_revizie`
```yaml
service: masinamea.update_revizie
data:
  data: "10.02.2025"
  km: 84000
  schimb_ulei: true
  schimb_filtru_ulei: true
  schimb_filtru_aer: false
  schimb_filtru_combustibil: false
```

### `masinamea.update_plate`
```yaml
service: masinamea.update_plate
data:
  numar: "B 123 ABC"
```

> **Notă:** Dacă ai mai multe mașini configurate, adaugă `entry_id` la fiecare apel. `entry_id`-ul îl găsești în **Settings → Devices & Services → Mașina Mea → (cele 3 puncte) → System information**.

---

## 📅 Calendar

Integrarea adaugă automat un calendar în HA cu următoarele evenimente:

| Eveniment | Când apare |
|-----------|-----------|
| Expirare ITP | Ziua exactă de expirare |
| Reminder ITP | Cu 30 de zile înainte |
| Expirare Rovinietă | Ziua exactă de expirare |
| Reminder Rovinietă | Cu 7 zile înainte |
| Expirare RCA | Ziua exactă de expirare |
| Reminder RCA | Cu 30 de zile înainte |
| Revizie recomandată | La 6 luni după ultima revizie |

---

## 📋 Stări senzori

| Valoare | Semnificație |
|---------|-------------|
| `activ` | Document valid, nu expiră curând |
| `aproape_expirare` | ITP/RCA < 30 zile / Rovinietă < 7 zile |
| `urgent` | Expiră în 1–2 zile |
| `expirat` | Document expirat |

---

## 🔔 Exemplu automatizare — notificare expirare RCA

```yaml
alias: "Notificare RCA aproape de expirare"
trigger:
  - platform: numeric_state
    entity_id: sensor.masina_mea_rca_expira_in
    below: 30
condition: []
action:
  - service: notify.mobile_app_telefonul_meu
    data:
      title: "⚠️ RCA aproape de expirare"
      message: >
        Asigurarea RCA expiră în {{ states('sensor.masina_mea_rca_expira_in') }} zile.
        Reînnoiește asigurarea!
mode: single
```

---

## 🤝 Contribuții

Contribuțiile sunt binevenite! Dacă găsești un bug sau ai o idee nouă:

1. Deschide un [Issue](https://github.com/GeorgeRPI/masinamea/issues)
2. Fork → branch nou → Pull Request

---

## 📄 Licență

Distribuit sub licența MIT. Vezi [LICENSE](LICENSE) pentru detalii.

---

<p align="center">Făcut cu ❤️ pentru comunitatea Home Assistant din România</p>
