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

## 📋 Card
Înlocuiește " masina_mea " cu numele mașinii tale (cu litere mici, spații → _)

```yaml

type: vertical-stack
cards:
  - type: custom:mod-card
    card:
      type: entities
      title: 🚗 Masina Mea
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_informatii
          name: Marcă / Model
          secondary: >-
            {{ state_attr('sensor.masina_mea_informatii', 'marca') }} {{
            state_attr('sensor.masina_mea_informatii', 'model') }}
          icon: mdi:car
        - type: custom:template-entity-row
          entity: sensor.masina_mea_numar_inmatriculare
          name: Număr înmatriculare
          secondary: "{{ states('sensor.masina_mea_numar_inmatriculare') }}"
          icon: mdi:car-license-plate
        - type: custom:template-entity-row
          entity: sensor.masina_mea_kilometraj
          name: Kilometraj curent
          secondary: "{{ states('sensor.masina_mea_kilometraj') }} km"
          icon: mdi:counter
        - type: custom:template-entity-row
          entity: sensor.masina_mea_capacitate_cilindrica
          name: Capacitate cilindrică
          secondary: "{{ states('sensor.masina_mea_capacitate_cilindrica') }} cm³"
          icon: mdi:engine
    card_mod:
      style: |
        ha-card {
          background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
          border-radius: 20px;
          border: none;
          padding: 5px;
          box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        .card-header {
          color: #e0e0ff !important;
          font-size: 22px;
          font-weight: bold;
          letter-spacing: 1px;
          padding-bottom: 10px;
          border-bottom: 1px solid rgba(255,255,255,0.15);
        }
        hui-generic-entity-row, .entity {
          background: rgba(255,255,255,0.07);
          border-radius: 12px;
          margin: 6px 0;
          padding: 8px 12px;
          color: white !important;
        }
        state-badge { display: none; }
  - type: custom:mod-card
    card:
      type: entities
      title: 🔧 ITP
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_itp_status
          name: Status
          secondary: >-
            {% set s = states('sensor.masina_mea_itp_status') %} {% if s ==
            'activ' %}✅ ACTIV {% elif s == 'aproape_expirare' %}⚠️ APROAPE {%
            elif s == 'urgent' %}🔴 URGENT! {% elif s == 'expirat' %}❌ EXPIRAT
            {% else %}⚪ —{% endif %}
          icon: mdi:car-wrench
        - type: custom:template-entity-row
          entity: sensor.masina_mea_itp_expira_in
          name: Expiră în
          secondary: "{{ states('sensor.masina_mea_itp_expira_in') }} zile"
          icon: mdi:calendar-clock
        - type: custom:template-entity-row
          entity: sensor.masina_mea_itp_status
          name: Dată expirare
          secondary: "{{ state_attr('sensor.masina_mea_itp_status', 'data_expirare') }}"
          icon: mdi:calendar
        - type: custom:template-entity-row
          entity: sensor.masina_mea_itp_status
          name: Dată efectuare
          secondary: "{{ state_attr('sensor.masina_mea_itp_status', 'data_efectuare') }}"
          icon: mdi:calendar-check
    card_mod:
      style: |
        {% set days = states('sensor.masina_mea_itp_expira_in') | int(999) %}
        {% set exp  = states('sensor.masina_mea_itp_status') %}
        ha-card {
          background: {% if exp == 'expirat' or days <= 0 %}
            linear-gradient(145deg, #7f0000, #c0392b)
          {% elif days <= 2 %}
            linear-gradient(145deg, #7f3f00, #e67e22)
          {% elif days <= 30 %}
            linear-gradient(145deg, #7f6a00, #f1c40f)
          {% else %}
            linear-gradient(145deg, #145a32, #27ae60)
          {% endif %};
          border-radius: 18px;
          border: none;
          padding: 4px;
          animation: {% if days <= 2 %}pulse 1.8s infinite{% endif %};
        }
        .card-header {
          color: white !important;
          font-size: 17px;
          font-weight: bold;
          border-bottom: 1px solid rgba(255,255,255,0.25);
          padding-bottom: 8px;
        }
        hui-generic-entity-row, .entity {
          background: rgba(0,0,0,0.2);
          border-radius: 10px;
          margin: 5px 0;
          padding: 6px 10px;
          color: white !important;
        }
        state-badge { display: none; }
        @keyframes pulse {
          0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); }
          70%  { box-shadow: 0 0 0 12px rgba(255,255,255,0); }
          100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
        }
  - type: custom:mod-card
    card:
      type: entities
      title: 🛣️ Rovinietă
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rovinieta_status
          name: Status
          secondary: >-
            {% set s = states('sensor.masina_mea_rovinieta_status') %} {% if s
            == 'activ' %}✅ ACTIV {% elif s == 'aproape_expirare' %}⚠️ APROAPE {%
            elif s == 'urgent' %}🔴 URGENT! {% elif s == 'expirat' %}❌ EXPIRAT
            {% else %}⚪ —{% endif %}
          icon: mdi:road-variant
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rovinieta_expira_in
          name: Expiră în
          secondary: "{{ states('sensor.masina_mea_rovinieta_expira_in') }} zile"
          icon: mdi:calendar-clock
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rovinieta_status
          name: Dată expirare
          secondary: >-
            {{ state_attr('sensor.masina_mea_rovinieta_status', 'data_expirare')
            }}
          icon: mdi:calendar
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rovinieta_status
          name: Dată achiziție
          secondary: >-
            {{ state_attr('sensor.masina_mea_rovinieta_status',
            'data_achizitie') }}
          icon: mdi:calendar-check
    card_mod:
      style: >
        {% set days = states('sensor.masina_mea_rovinieta_expira_in') | int(999)
        %}

        {% set exp  = states('sensor.masina_mea_rovinieta_status') %}

        ha-card {
          background: {% if exp == 'expirat' or days <= 0 %}
            linear-gradient(145deg, #7f0000, #c0392b)
          {% elif days <= 2 %}
            linear-gradient(145deg, #7f3f00, #e67e22)
          {% elif days <= 7 %}
            linear-gradient(145deg, #7f6a00, #f1c40f)
          {% else %}
            linear-gradient(145deg, #145a32, #27ae60)
          {% endif %};
          border-radius: 18px;
          border: none;
          padding: 4px;
          animation: {% if days <= 2 %}pulse 1.8s infinite{% endif %};
        }

        .card-header {
          color: white !important;
          font-size: 17px;
          font-weight: bold;
          border-bottom: 1px solid rgba(255,255,255,0.25);
          padding-bottom: 8px;
        }

        hui-generic-entity-row, .entity {
          background: rgba(0,0,0,0.2);
          border-radius: 10px;
          margin: 5px 0;
          padding: 6px 10px;
          color: white !important;
        }

        state-badge { display: none; }

        @keyframes pulse {
          0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); }
          70%  { box-shadow: 0 0 0 12px rgba(255,255,255,0); }
          100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
        }
  - type: custom:mod-card
    card:
      type: entities
      title: 🛡️ Asigurare RCA
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rca_status
          name: Status
          secondary: >-
            {% set s = states('sensor.masina_mea_rca_status') %} {% if s ==
            'activ' %}✅ ACTIV {% elif s == 'aproape_expirare' %}⚠️ APROAPE DE
            EXPIRARE {% elif s == 'urgent' %}🔴 URGENT — EXPIRĂ ÎN CURÂND! {%
            elif s == 'expirat' %}❌ EXPIRAT — RISC AMENDĂ! {% else %}⚪
            Nedefinit{% endif %}
          icon: mdi:shield-car
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rca_expira_in
          name: Expiră în
          secondary: "{{ states('sensor.masina_mea_rca_expira_in') }} zile"
          icon: mdi:calendar-clock
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rca_status
          name: Dată expirare
          secondary: "{{ state_attr('sensor.masina_mea_rca_status', 'data_expirare') }}"
          icon: mdi:calendar-remove
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rca_status
          name: Dată intrare vigoare
          secondary: >-
            {{ state_attr('sensor.masina_mea_rca_status',
            'data_intrare_vigoare') }}
          icon: mdi:calendar-check
        - type: custom:template-entity-row
          entity: sensor.masina_mea_rca_urgenta
          name: Nivel urgență
          secondary: "{{ states('sensor.masina_mea_rca_urgenta') | upper }}"
          icon: mdi:alert-circle
    card_mod:
      style: |
        {% set days = states('sensor.masina_mea_rca_expira_in') | int(999) %}
        {% set exp  = states('sensor.masina_mea_rca_status') %}
        ha-card {
          background: {% if exp == 'expirat' or days <= 0 %}
            linear-gradient(135deg, #7f0000 0%, #c0392b 100%)
          {% elif days <= 2 %}
            linear-gradient(135deg, #7f3f00 0%, #e67e22 100%)
          {% elif days <= 30 %}
            linear-gradient(135deg, #7f6a00 0%, #f1c40f 100%)
          {% else %}
            linear-gradient(135deg, #145a32 0%, #27ae60 100%)
          {% endif %};
          border-radius: 20px;
          border: none;
          padding: 5px;
          margin-top: 0px;
          animation: {% if days <= 2 %}pulse 1.8s infinite{% endif %};
        }
        .card-header {
          color: white !important;
          font-size: 20px;
          font-weight: bold;
          border-bottom: 1px solid rgba(255,255,255,0.25);
          padding-bottom: 10px;
        }
        hui-generic-entity-row, .entity {
          background: rgba(0,0,0,0.2);
          border-radius: 12px;
          margin: 6px 0;
          padding: 8px 12px;
          color: white !important;
        }
        state-badge { display: none; }
        @keyframes pulse {
          0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); }
          70%  { box-shadow: 0 0 0 14px rgba(255,255,255,0); }
          100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
        }
  - type: custom:mod-card
    card:
      type: entities
      title: 🔩 Revizii și Întreținere
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_recomandare_revizie
          name: Recomandare
          secondary: "{{ states('sensor.masina_mea_recomandare_revizie') }}"
          icon: mdi:tooltip-account
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: Ultima revizie
          secondary: "{{ states('sensor.masina_mea_ultima_revizie') }}"
          icon: mdi:calendar
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: Km la revizie
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie', 'km_la_revizie')
            }} km
          icon: mdi:counter
        - type: custom:template-entity-row
          entity: sensor.masina_mea_km_de_la_revizie
          name: Km de la revizie
          secondary: "{{ states('sensor.masina_mea_km_de_la_revizie') }} km"
          icon: mdi:map-marker-distance
        - type: custom:template-entity-row
          entity: sensor.masina_mea_zile_de_la_revizie
          name: Zile de la revizie
          secondary: "{{ states('sensor.masina_mea_zile_de_la_revizie') }} zile"
          icon: mdi:calendar-range
        - type: custom:template-entity-row
          entity: sensor.masina_mea_recomandare_revizie
          name: Km până la revizie
          secondary: >-
            {{ state_attr('sensor.masina_mea_recomandare_revizie',
            'km_pana_la_revizie') }} km
          icon: mdi:road
        - type: divider
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 🛢️ Schimb ulei
          secondary: "{{ state_attr('sensor.masina_mea_ultima_revizie', 'schimb_ulei') }}"
          icon: mdi:oil
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 🔍 Filtru ulei
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie',
            'schimb_filtru_ulei') }}
          icon: mdi:oil
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 💨 Filtru aer
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie',
            'schimb_filtru_aer') }}
          icon: mdi:air-filter
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: ⛽ Filtru combustibil
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie',
            'schimb_filtru_combustibil') }}
          icon: mdi:fuel
    card_mod:
      style: |
        {% set rec = states('sensor.masina_mea_recomandare_revizie') %}
        ha-card {
          background: {% if 'necesară' in rec %}
            linear-gradient(135deg, #7f0000 0%, #c0392b 100%)
          {% elif 'Aproape' in rec %}
            linear-gradient(135deg, #7f6a00 0%, #f39c12 100%)
          {% else %}
            linear-gradient(135deg, #1a3a5c 0%, #2980b9 100%)
          {% endif %};
          border-radius: 20px;
          border: none;
          padding: 5px;
        }
        .card-header {
          color: white !important;
          font-size: 20px;
          font-weight: bold;
          border-bottom: 1px solid rgba(255,255,255,0.25);
          padding-bottom: 10px;
        }
        hui-generic-entity-row, .entity {
          background: rgba(0,0,0,0.2);
          border-radius: 12px;
          margin: 5px 0;
          padding: 7px 12px;
          color: white !important;
        }
        .divider {
          background: rgba(255,255,255,0.2);
          height: 1px;
          margin: 8px 0;
        }
        state-badge { display: none; }
  - type: custom:mod-card
    card:
      type: markdown
      content: >
        {% set itp_days = states('sensor.masina_mea_itp_expira_in') | int(0) %}
        {% set rov_days = states('sensor.masina_mea_rovinieta_expira_in') |
        int(0) %} {% set rca_days = states('sensor.masina_mea_rca_expira_in') |
        int(0) %} {% set itp_exp  = states('sensor.masina_mea_itp_status') ==
        'expirat' %} {% set rov_exp  =
        states('sensor.masina_mea_rovinieta_status') == 'expirat' %} {% set
        rca_exp  = states('sensor.masina_mea_rca_status') == 'expirat' %}

        {% if itp_exp or rov_exp or rca_exp %} <div
        style="text-align:center;padding:16px;">
          <div style="font-size:36px;margin-bottom:8px;">🚨</div>
          <div style="font-size:19px;font-weight:bold;margin-bottom:10px;">DOCUMENTE EXPIRATE!</div>
          <div style="font-size:14px;line-height:2;">
            {% if itp_exp %}❌ ITP EXPIRAT — Programează inspecția imediat!<br>{% endif %}
            {% if rov_exp %}❌ ROVINIETĂ EXPIRATĂ — Achiziționează urgent!<br>{% endif %}
            {% if rca_exp %}❌ RCA EXPIRAT — Risc amendă și accident neacoperit!<br>{% endif %}
          </div>
        </div>

        {% elif itp_days <= 2 or rov_days <= 2 or rca_days <= 2 %} <div
        style="text-align:center;padding:16px;">
          <div style="font-size:36px;margin-bottom:8px;">⚠️</div>
          <div style="font-size:18px;font-weight:bold;margin-bottom:10px;">URGENT — Expiră în câteva zile!</div>
          <div style="font-size:14px;line-height:2;">
            {% if itp_days <= 2 and itp_days > 0 %}🟠 ITP expiră în {{ itp_days }} zile<br>{% endif %}
            {% if rov_days <= 2 and rov_days > 0 %}🟠 Rovinieta expiră în {{ rov_days }} zile<br>{% endif %}
            {% if rca_days <= 2 and rca_days > 0 %}🟠 RCA expiră în {{ rca_days }} zile<br>{% endif %}
          </div>
        </div>

        {% elif itp_days <= 30 or rov_days <= 7 or rca_days <= 30 %} <div
        style="text-align:center;padding:16px;">
          <div style="font-size:36px;margin-bottom:8px;">📅</div>
          <div style="font-size:17px;font-weight:bold;margin-bottom:10px;">Documente aproape de expirare</div>
          <div style="font-size:14px;line-height:2;">
            {% if itp_days <= 30 %}📋 ITP — mai sunt {{ itp_days }} zile<br>{% endif %}
            {% if rov_days <= 7 %}🛣️ Rovinietă — mai sunt {{ rov_days }} zile<br>{% endif %}
            {% if rca_days <= 30 %}🛡️ RCA — mai sunt {{ rca_days }} zile<br>{% endif %}
          </div>
        </div>

        {% else %} <div style="text-align:center;padding:16px;">
          <div style="font-size:36px;margin-bottom:8px;">✅</div>
          <div style="font-size:18px;font-weight:bold;margin-bottom:10px;">TOATE DOCUMENTELE ÎN REGULĂ</div>
          <div style="font-size:13px;line-height:2;opacity:0.9;">
            🔧 ITP valid — {{ itp_days }} zile<br>
            🛣️ Rovinietă validă — {{ rov_days }} zile<br>
            🛡️ RCA valid — {{ rca_days }} zile
          </div>
        </div> {% endif %}
    card_mod:
      style: >
        {% set itp_days = states('sensor.masina_mea_itp_expira_in') | int(0) %}

        {% set rov_days = states('sensor.masina_mea_rovinieta_expira_in') |
        int(0) %}

        {% set rca_days = states('sensor.masina_mea_rca_expira_in') | int(0) %}

        {% set itp_exp  = states('sensor.masina_mea_itp_status') == 'expirat' %}

        {% set rov_exp  = states('sensor.masina_mea_rovinieta_status') ==
        'expirat' %}

        {% set rca_exp  = states('sensor.masina_mea_rca_status') == 'expirat' %}

        {% set critical = itp_exp or rov_exp or rca_exp %}

        {% set urgent   = itp_days <= 2 or rov_days <= 2 or rca_days <= 2 %}

        {% set warning  = itp_days <= 30 or rov_days <= 7 or rca_days <= 30 %}

        ha-card {
          background: {% if critical %}
            linear-gradient(135deg, #7f0000, #c0392b)
          {% elif urgent %}
            linear-gradient(135deg, #7f3f00, #e67e22)
          {% elif warning %}
            linear-gradient(135deg, #7f6a00, #f1c40f)
          {% else %}
            linear-gradient(135deg, #145a32, #27ae60)
          {% endif %};
          border-radius: 20px;
          border: none;
          color: white;
          animation: {% if urgent or critical %}pulse-banner 1.8s infinite{% endif %};
        }

        @keyframes pulse-banner {
          0%   { box-shadow: 0 0 0 0 rgba(255,255,255,0.35); }
          70%  { box-shadow: 0 0 0 16px rgba(255,255,255,0); }
          100% { box-shadow: 0 0 0 0 rgba(255,255,255,0); }
        }

        ha-markdown { color: white !important; }

```
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
