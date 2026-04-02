# Mașina Mea - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/Home_Assistant-2023.1%2B-green.svg)](https://www.home-assistant.io/)
[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/GeorgeRPI/masinamea)
[![maintenance](https://img.shields.io/badge/maintainer-GeorgeRPI-blue.svg)](https://github.com/GeorgeRPI)

Integrare pentru Home Assistant care îți permite să gestionezi toate datele mașinii tale: kilometraj, ITP, rovinietă, revizii și multe altele.

## 📋 Funcționalități

- ✅ **Gestionare completă** a datelor mașinii
- ✅ **ITP** - monitorizare status, expirare, notificări
- ✅ **Rovinietă** - urmărire achiziție și expirare
- ✅ **Revizii** - înregistrare istoric, componente schimbate
- ✅ **Kilometraj** - urmărire evoluție
- ✅ **Calendar integrat** - evenimente și reminder-e
- ✅ **Culori dinamice** - verde/portocaliu/roșu în funcție de status
- ✅ **Notificări proactive** - alertă înainte de expirare
- ✅ **Suport Română** - interfață complet în limba română

## 🚗 Date gestionate

| Categorie | Date |
|-----------|------|
| **Mașină** | Nume, număr înmatriculare, marcă, model, capacitate cilindrică |
| **Kilometraj** | Valoare curentă, istoric |
| **ITP** | Data efectuare, data expirare, zile rămase, status |
| **Rovinietă** | Data achiziție, data expirare, zile rămase, status |
| **Revizii** | Data, kilometraj, componente schimbate (ulei, filtre) |

## 📊 Stări și culori

| Status | Culoare | Descriere |
|--------|---------|-----------|
| Activ | 🟢 Verde | Document în regulă |
| Aproape expirare | 🟡 Galben | ITP < 30 zile / Rovinietă < 7 zile |
| Urgent | 🟠 Portocaliu | Expiră în 1-2 zile |
| Expirat | 🔴 Roșu | Document expirat |

## 📦 Instalare

### Prin HACS (recomandat)

1. Deschide HACS în Home Assistant
2. Click pe "Integrations"
3. Click pe "Custom repositories"
4. Adaugă URL-ul: `https://github.com/yourusername/masinamea`
5. Selectează categoriile: "Integration"
6. Click "Add"
7. Găsește "Mașina Mea" în HACS și instalează
8. Restartează Home Assistant

### Manual

1. Copiază folderul `custom_components/masinamea` în directorul `custom_components` din Home Assistant
2. Restartează Home Assistant

## ⚙️ Configurare

1. Mergi la **Settings → Devices & Services**
2. Click pe **Add Integration** (butonul + din dreapta jos)
3. Caută **Mașina Mea**
4. Completează datele mașinii tale:
   - Nume mașină
   - Număr înmatriculare
   - Marcă și model
   - Capacitate cilindrică
   - Kilometraj curent
   - Date ITP, rovinietă, revizii
5. Click **Submit**

## 🎨 Card dashboard

Adaugă acest card în dashboard-ul tău pentru a vizualiza toate datele:

```yaml
type: vertical-stack
cards:
  - type: custom:mod-card
    card:
      type: entities
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_informatii
          name: 🚗 Mașina Mea
          secondary: >-
            {{ state_attr('sensor.masina_mea_informatii', 'marca') }} {{
            state_attr('sensor.masinamea_informatii', 'model') }}
        - type: custom:template-entity-row
          entity: sensor.masina_mea_informatii
          name: 📝 Număr înmatriculare
          secondary: "{{ state_attr('sensor.masina_mea_informatii', 'nr_inmatriculare') }}"
          icon: mdi:car-license-plate
        - type: custom:template-entity-row
          entity: sensor.masina_mea_informatii
          name: 🔧 Capacitate cilindrică
          secondary: >-
            {{ state_attr('sensor.masina_mea_informatii',
            'capacitate_cilindrica') }} cm³
          icon: mdi:engine
        - type: custom:template-entity-row
          entity: sensor.masina_mea_kilometraj
          name: 📍 Kilometraj curent
          secondary: "{{ states('sensor.masina_mea_kilometraj') }} km"
          icon: mdi:counter
      title: 📋 Informații Generale
    card_mod:
      style: |
        ha-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 20px;
          color: white;
          padding: 5px;
        }
        .card-header {
          color: white !important;
          font-size: 20px;
          font-weight: bold;
          border-bottom: 2px solid rgba(255,255,255,0.3);
          padding-bottom: 10px;
        }
        .entity {
          background: rgba(255,255,255,0.15);
          border-radius: 12px;
          margin: 8px 0;
          padding: 10px;
          backdrop-filter: blur(5px);
        }
  - type: horizontal-stack
    cards:
      - type: custom:mod-card
        card:
          type: entities
          entities:
            - type: custom:template-entity-row
              entity: sensor.masina_mea_itp_status
              name: 📊 Status
              secondary: >
                {% set status = states('sensor.masina_mea_itp_status') %} {% if
                status == 'activ' %}✅ ACTIV {% elif status == 'urgent' %}🔴
                URGENT! {% elif status == 'aproape_expirare' %}⚠️ APROAPE
                EXPIRARE {% elif status == 'expirat' %}❌ EXPIRAT {% else %}⚪
                NEDEFINIT{% endif %}
              icon: mdi:car-wrench
            - type: custom:template-entity-row
              entity: sensor.masina_mea_itp_expira_in
              name: ⏰ Zile rămase
              secondary: "{{ states('sensor.masina_mea_itp_expira_in') }} zile"
              icon: mdi:calendar-clock
            - type: custom:template-entity-row
              entity: sensor.masinamea_itp_status
              name: 📅 Expiră la
              secondary: >-
                {{ state_attr('sensor.masina_mea_itp_status', 'data_expirare')
                }}
              icon: mdi:calendar
            - type: custom:template-entity-row
              entity: sensor.masina_mea_itp_status
              name: ✅ Efectuat la
              secondary: >-
                {{ state_attr('sensor.masina_mea_itp_status', 'data_efectuare')
                }}
              icon: mdi:calendar-check
          title: 🔧 ITP
        card_mod:
          style: |
            {% set days = states('sensor.masina_mea_itp_expira_in') | int(0) %}
            ha-card {
              background: {% if days <= 0 %}linear-gradient(135deg, #e74c3c, #c0392b)
              {% elif days <= 2 %}linear-gradient(135deg, #f39c12, #e67e22)
              {% elif days <= 30 %}linear-gradient(135deg, #f1c40f, #f39c12)
              {% else %}linear-gradient(135deg, #27ae60, #2ecc71){% endif %};
              border-radius: 20px;
              color: white;
              padding: 5px;
              animation: {% if days <= 2 %}pulse-card 1.5s infinite{% endif %};
            }
            .card-header {
              color: white !important;
              font-size: 18px;
              font-weight: bold;
              border-bottom: 2px solid rgba(255,255,255,0.3);
            }
            .entity {
              background: rgba(255,255,255,0.2);
              border-radius: 12px;
              margin: 8px 0;
              padding: 10px;
            }
            @keyframes pulse-card {
              0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(243, 156, 18, 0.7); }
              70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(243, 156, 18, 0); }
              100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(243, 156, 18, 0); }
            }
      - type: custom:mod-card
        card:
          type: entities
          entities:
            - type: custom:template-entity-row
              entity: sensor.masina_mea_rovinieta_status
              name: 📊 Status
              secondary: >
                {% set status = states('sensor.masina_mea_rovinieta_status') %}
                {% if status == 'activ' %}✅ ACTIVĂ {% elif status == 'urgent'
                %}🔴 URGENT! {% elif status == 'aproape_expirare' %}⚠️ APROAPE
                EXPIRARE {% elif status == 'expirat' %}❌ EXPIRATĂ {% else %}⚪
                NEDEFINIT{% endif %}
              icon: mdi:road-variant
            - type: custom:template-entity-row
              entity: sensor.masina_mea_rovinieta_expira_in
              name: ⏰ Zile rămase
              secondary: "{{ states('sensor.masina_mea_rovinieta_expira_in') }} zile"
              icon: mdi:calendar-clock
            - type: custom:template-entity-row
              entity: sensor.masina_mea_rovinieta_status
              name: 📅 Expiră la
              secondary: >-
                {{ state_attr('sensor.masina_mea_rovinieta_status',
                'data_expirare') }}
              icon: mdi:calendar
            - type: custom:template-entity-row
              entity: sensor.masina_mea_rovinieta_status
              name: 🛒 Achiziționată la
              secondary: >-
                {{ state_attr('sensor.masina_mea_rovinieta_status',
                'data_achizitie') }}
              icon: mdi:calendar-check
          title: 🛣️ Rovinietă
        card_mod:
          style: >
            {% set days = states('sensor.masina_mea_rovinieta_expira_in') |
            int(0) %}

            ha-card {
              background: {% if days <= 0 %}linear-gradient(135deg, #e74c3c, #c0392b)
              {% elif days <= 2 %}linear-gradient(135deg, #f39c12, #e67e22)
              {% elif days <= 7 %}linear-gradient(135deg, #f1c40f, #f39c12)
              {% else %}linear-gradient(135deg, #27ae60, #2ecc71){% endif %};
              border-radius: 20px;
              color: white;
              padding: 5px;
              animation: {% if days <= 2 %}pulse-card 1.5s infinite{% endif %};
            }

            .card-header {
              color: white !important;
              font-size: 18px;
              font-weight: bold;
              border-bottom: 2px solid rgba(255,255,255,0.3);
            }

            .entity {
              background: rgba(255,255,255,0.2);
              border-radius: 12px;
              margin: 8px 0;
              padding: 10px;
            }

            @keyframes pulse-card {
              0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(243, 156, 18, 0.7); }
              70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(243, 156, 18, 0); }
              100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(243, 156, 18, 0); }
            }
  - type: custom:mod-card
    card:
      type: entities
      entities:
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 📅 Data revizie
          secondary: "{{ states('sensor.masina_mea_ultima_revizie') }}"
          icon: mdi:calendar
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 📍 Kilometraj la revizie
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie', 'km_la_revizie')
            }} km
          icon: mdi:counter
        - type: custom:template-entity-row
          entity: sensor.masina_mea_km_de_la_revizie
          name: 📊 Km de la revizie
          secondary: "{{ states('sensor.masina_mea_km_de_la_revizie') }} km"
          icon: mdi:counter
        - type: custom:template-entity-row
          entity: sensor.masina_mea_zile_de_la_revizie
          name: 📅 Zile de la revizie
          secondary: "{{ states('sensor.masina_mea_zile_de_la_revizie') }} zile"
          icon: mdi:calendar-range
        - type: custom:template-entity-row
          entity: sensor.masina_mea_recomandare_revizie
          name: 💡 Recomandare
          secondary: "{{ states('sensor.masina_mea_recomandare_revizie') }}"
          icon: mdi:tooltip-account
        - type: divider
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 🛢️ Schimb ulei
          secondary: "{{ state_attr('sensor.masina_mea_ultima_revizie', 'schimb_ulei') }}"
          icon: mdi:oil
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 🔍 Schimb filtru ulei
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie',
            'schimb_filtru_ulei') }}
          icon: mdi:oil
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: 💨 Schimb filtru aer
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie',
            'schimb_filtru_aer') }}
          icon: mdi:air-filter
        - type: custom:template-entity-row
          entity: sensor.masina_mea_ultima_revizie
          name: ⛽ Schimb filtru combustibil
          secondary: >-
            {{ state_attr('sensor.masina_mea_ultima_revizie',
            'schimb_filtru_combustibil') }}
          icon: mdi:fuel
      title: 🔧 Revizii și Întreținere
    card_mod:
      style: |
        ha-card {
          background: linear-gradient(135deg, #3498db, #2980b9);
          border-radius: 20px;
          color: white;
          margin-top: 15px;
          padding: 5px;
        }
        .card-header {
          color: white !important;
          font-size: 20px;
          font-weight: bold;
          border-bottom: 2px solid rgba(255,255,255,0.3);
          padding-bottom: 10px;
        }
        .entity {
          background: rgba(255,255,255,0.15);
          border-radius: 12px;
          margin: 8px 0;
          padding: 10px;
          backdrop-filter: blur(5px);
        }
        .divider {
          background: rgba(255,255,255,0.3);
          margin: 10px 0;
        }
  - type: custom:mod-card
    card:
      type: markdown
      content: >
        {% set itp_days = states('sensor.masina_mea_itp_expira_in') | int(0) %}

        {% set itp_status = states('sensor.masina_mea_itp_status') %}

        {% set rovinieta_days = states('sensor.masina_mea_rovinieta_expira_in')
        | int(0) %}

        {% set rovinieta_status = states('sensor.masina_mea_rovinieta_status')
        %}


        {% if itp_days <= 0 or rovinieta_days <= 0 %}

        <div style="text-align: center; padding: 15px;">
          <div style="font-size: 32px; margin-bottom: 10px;">⚠️⚠️⚠️</div>
          <div style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">URGENȚĂ! DOCUMENTE EXPIRATE!</div>
          <div style="font-size: 14px;">
            {% if itp_days <= 0 %}🔴 ITP EXPIRAT! Programează imediat inspecția tehnică!<br>{% endif %}
            {% if rovinieta_days <= 0 %}🔴 ROVINIETĂ EXPIRATĂ! Achiziționează urgent o nouă rovinietă!<br>{% endif %}
          </div>
        </div>

        {% elif itp_days <= 2 or rovinieta_days <= 2 %}

        <div style="text-align: center; padding: 15px;">
          <div style="font-size: 32px; margin-bottom: 10px;">⚠️⚠️⚠️</div>
          <div style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">ATENȚIE! EXPIRĂ ÎN URMĂTOARELE ZILE!</div>
          <div style="font-size: 14px;">
            {% if itp_days <= 2 and itp_days > 0 %}🟠 ITP expiră în {{ itp_days }} zile!<br>{% endif %}
            {% if rovinieta_days <= 2 and rovinieta_days > 0 %}🟠 Rovinieta expiră în {{ rovinieta_days }} zile!<br>{% endif %}
          </div>
        </div>

        {% elif itp_status == 'aproape_expirare' or rovinieta_status ==
        'aproape_expirare' %}

        <div style="text-align: center; padding: 15px;">
          <div style="font-size: 32px; margin-bottom: 10px;">⚠️</div>
          <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">Documente aproape de expirare</div>
          <div style="font-size: 14px;">
            {% if itp_days <= 30 and itp_days > 0 %}📅 ITP expiră în {{ itp_days }} zile<br>{% endif %}
            {% if rovinieta_days <= 7 and rovinieta_days > 0 %}📅 Rovinieta expiră în {{ rovinieta_days }} zile<br>{% endif %}
          </div>
        </div>

        {% else %}

        <div style="text-align: center; padding: 15px;">
          <div style="font-size: 32px; margin-bottom: 10px;">✅</div>
          <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">TOATE DOCUMENTELE SUNT ÎN REGULĂ</div>
          <div style="font-size: 14px;">ITP activ pentru {{ itp_days }} zile | Rovinietă activă pentru {{ rovinieta_days }} zile</div>
        </div>

        {% endif %}
    card_mod:
      style: |
        ha-card {
          background: {% set itp_days = states('sensor.masinamea_itp_expira_in') | int(0) %}
                    {% set rovinieta_days = states('sensor.masinamea_rovinieta_expira_in') | int(0) %}
                    {% if itp_days <= 0 or rovinieta_days <= 0 %}
                      linear-gradient(135deg, #e74c3c, #c0392b)
                    {% elif itp_days <= 2 or rovinieta_days <= 2 %}
                      linear-gradient(135deg, #f39c12, #e67e22)
                    {% elif itp_days <= 30 or rovinieta_days <= 7 %}
                      linear-gradient(135deg, #f1c40f, #f39c12)
                    {% else %}
                      linear-gradient(135deg, #27ae60, #2ecc71)
                    {% endif %};
          border-radius: 20px;
          color: white;
          margin-top: 15px;
          animation: {% if itp_days <= 2 or rovinieta_days <= 2 %}pulse-banner 1.5s infinite{% endif %};
        }
        @keyframes pulse-banner {
          0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(243, 156, 18, 0.7); }
          70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(243, 156, 18, 0); }
          100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(243, 156, 18, 0); }
        }
