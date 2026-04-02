# 🚗 Mașina Mea — Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/v/release/GeorgeRPI/masinamea?style=flat-square)](https://github.com/GeorgeRPI/masinamea/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/Home_Assistant-2023.1%2B-blue?style=flat-square)](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/GeorgeRPI/masinamea?style=flat-square)](LICENSE)

Integrare locală pentru Home Assistant care îți permite să gestionezi toate datele importante ale mașinii tale direct din interfața HA: **ITP**, **rovinietă**, **revizii**, **kilometraj** — cu notificări, calendar și senzori dinamici.

---

## ✨ Funcționalități

- 🔴🟡🟢 **Status dinamic** — culori în funcție de cât timp a mai rămas (activ / aproape expirare / urgent / expirat)
- ⏰ **Calendar integrat** — evenimente și reminder-uri automate pentru ITP, rovinietă și revizie
- 🔔 **Notificări proactive** — avertizare cu 30 zile înainte de expirarea ITP-ului și 7 zile pentru rovinietă
- 📊 **14+ senzori** — date detaliate pentru fiecare categorie
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

> **Notă:** Dacă ai mai multe mașini configurate, adaugă `entry_id` la fiecare apel de serviciu pentru a specifica ce mașină vrei să actualizezi. `entry_id`-ul îl găsești în **Settings → Devices & Services → Mașina Mea → (cele 3 puncte) → System information**.

---

## 📅 Calendar

Integrarea adaugă automat un calendar în HA cu următoarele evenimente:

- **Expirare ITP** — ziua exactă de expirare
- **Reminder ITP** — cu 30 de zile înainte
- **Expirare rovinietă** — ziua exactă de expirare
- **Reminder rovinietă** — cu 7 zile înainte
- **Revizie recomandată** — la 6 luni după ultima revizie

---

## 🎨 Exemplu dashboard

Copiază cardul de mai jos în editorul YAML al dashboard-ului tău. Necesită [card-mod](https://github.com/thomasloven/lovelace-card-mod) instalat prin HACS.

```yaml
type: vertical-stack
cards:
  - type: entities
    title: 🚗 Mașina Mea
    entities:
      - entity: sensor.masina_mea_informatii
        name: Informații generale
      - entity: sensor.masina_mea_kilometraj
        name: Kilometraj
      - entity: sensor.masina_mea_itp_status
        name: Status ITP
      - entity: sensor.masina_mea_itp_expira_in
        name: ITP expiră în
      - entity: sensor.masina_mea_rovinieta_status
        name: Status rovinietă
      - entity: sensor.masina_mea_rovinieta_expira_in
        name: Rovinietă expiră în
      - entity: sensor.masina_mea_recomandare_revizie
        name: Recomandare revizie
```

> Înlocuiește `masina_mea` cu numele pe care l-ai dat mașinii tale la configurare (cu litere mici și spațiile înlocuite cu `_`).

---

## 🔔 Exemplu automatizare — notificare expirare ITP

```yaml
alias: "Notificare ITP aproape de expirare"
trigger:
  - platform: numeric_state
    entity_id: sensor.masina_mea_itp_expira_in
    below: 30
condition: []
action:
  - service: notify.mobile_app_telefonul_meu
    data:
      title: "⚠️ ITP aproape de expirare"
      message: >
        ITP-ul expiră în {{ states('sensor.masina_mea_itp_expira_in') }} zile.
        Programează inspecția tehnică!
mode: single
```

---

## 📋 Stări senzori

| Valoare | Semnificație |
|---------|-------------|
| `activ` | Document valid, nu expiră curând |
| `aproape_expirare` | ITP < 30 zile / Rovinietă < 7 zile |
| `urgent` | Expiră în 1–2 zile |
| `expirat` | Document expirat |

---

## 🤝 Contribuții

Contribuțiile sunt binevenite! Dacă găsești un bug sau ai o idee de funcționalitate nouă:

1. Deschide un [Issue](https://github.com/GeorgeRPI/masinamea/issues) cu descrierea problemei
2. Fork la repository
3. Creează un branch nou: `git checkout -b feature/nume-functionalitate`
4. Commit și push: `git commit -m "Adaugă funcționalitate X"` → `git push origin feature/nume-functionalitate`
5. Deschide un Pull Request

---

## 📄 Licență

Distribuit sub licența MIT. Vezi [LICENSE](LICENSE) pentru detalii.

---

<p align="center">Făcut cu ❤️ pentru comunitatea Home Assistant din România</p>
