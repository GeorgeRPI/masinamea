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
type: custom:mod-card
card:
  type: entities
  entities:
    - entity: sensor.masinamea_informatii
      name: 🚗 Mașina Mea
    - entity: sensor.masinamea_kilometraj
      name: Kilometraj
    - entity: sensor.masinamea_itp_status
      name: Status ITP
      state_color: true
    - entity: sensor.masinamea_itp_expira_in
      name: Zile până la expirare ITP
    - entity: sensor.masinamea_rovinieta_status
      name: Status Rovinietă
      state_color: true
    - entity: sensor.masinamea_rovinieta_expira_in
      name: Zile până la expirare Rovinietă
    - entity: sensor.masinamea_ultima_revizie
      name: Ultima revizie
    - entity: sensor.masinamea_recomandare_revizie
      name: Recomandare revizie
      state_color: true
  title: 📊 Dashboard Mașină
