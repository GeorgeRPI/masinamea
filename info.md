# Mașina Mea

[![GitHub Release](https://img.shields.io/github/v/release/GeorgeRPI/masinamea?style=flat-square)](https://github.com/GeorgeRPI/masinamea/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://github.com/GeorgeRPI/masinamea)

## 🚗 Gestionează-ți mașina direct din Home Assistant

Integrare 100% locală pentru șoferii din România. Urmărești din HA:
- **Kilometraj** curent
- **ITP** – dată efectuare, expirare, status
- **Rovinietă** – achiziție, expirare, status
- **RCA** – intrare în vigoare, expirare, status
- **Revizii** – istoric complet cu componente schimbate

## ✨ Caracteristici principale

- 🔴🟡🟢 **Culori dinamice** în funcție de status (activ / aproape / urgent / expirat)
- ⏰ **Reminder-e automate** în calendar (30 zile ITP/RCA, 7 zile rovinietă)
- 📊 **Senzori dedicați** pentru fiecare categorie
- 🔔 **Notificări proactive** înainte de expirare
- 🛠 **Servicii HA** pentru update rapid din automatizări
- 🇷🇴 **Interfață complet în limba română**

## 📥 Instalare rapidă

1. HACS → Integrations → ⋮ → Custom repositories
2. Adaugă: `https://github.com/GeorgeRPI/masinamea` (categorie: Integration)
3. Instalează „Mașina Mea” → Restart Home Assistant
4. Settings → Devices & Services → Add Integration → Mașina Mea

## 🎯 Configurare inițială

Completezi o singură dată: nume, număr înmatriculare, marcă/model, km curent, date ITP, rovinietă, RCA și ultima revizie. Poți modifica oricând din Configure.

După configurare primești automat senzori, calendar și servicii de actualizare.

## 📸 Exemple dashboard

Vezi [README complet](https://github.com/GeorgeRPI/masinamea#readme) pentru carduri Lovelace gata de copiat.
