# WORK IN PROGRESS (WIP)

**Generert**: 2025-12-03
**Formål**: Dokumentere uferdig arbeid, planlagte features og problemer under feilsøking

---

## ✅ NYLIG FULLFØRT (siste 7 dager)

### Gang-lys automatisering (28. nov 2025)
- ✅ Funnet entity: `light.gang_lys` (Hue via Zigbee2MQTT)
- ✅ Kveldsdimming kl. 21:00 (til 1% over 60s)
- ✅ Morgendimming kl. 09:00 (til 50% over 60s)
- ✅ Begge automations aktive i HA Prod
- **Status**: Ferdig og fungerer

### Passwordless SSH til Home Assistant (28. nov 2025)
- ✅ SSH config opprettet (`~/.ssh/config`)
- ✅ Ingen flere passord-prompts
- ✅ `ssh homeassistant` fungerer perfekt
- **Status**: Ferdig

### Paperless-NGX Office-konvertering (27. nov 2025)
- ✅ LibreOffice + unoconv installert
- ✅ Office-watcher service (overvåker consume/ hvert 10. sek)
- ✅ Auto-konvertering .xlsx/.docx/.pptx → PDF
- ✅ Email cleanup automation (daglig kl. 03:00)
- **Status**: Ferdig og testet

### Motorvarmer-system for May (24. nov 2025)
- ✅ Input helpers (9 stk) opprettet
- ✅ 3 automations (temperatur, planlagt start, auto-av)
- ✅ Script for "start nå"
- ✅ Dashboard card i Lovelace
- **Status**: Ferdig og i produksjon

### Z-Wave JS UI oppsett (21-24. nov 2025)
- ✅ LXC 112 @ 10.12.0.27 fullt funksjonell
- ✅ Aeotec Z-Stick 7 Gen5+ med USB passthrough
- ✅ Fibaro Wallplug inkludert (`switch.motorvarmer`)
- ✅ AppArmor workaround implementert
- **Status**: Ferdig

---

## 🚧 PÅGÅENDE ARBEID

**INGEN PÅGÅENDE ARBEID PER NÅ.**

Siste oppgave var denne migreringen til LXC 150! 🚀

---

## 📋 PLANLAGTE FEATURES (prioritert rekkefølge)

### 1. Backup-løsning (KRITISK)
- **Prioritet**: 🔴 HØYEST
- **Beskrivelse**: Sette opp systematisk backup av alle kritiske systemer
- **Komponenter**:
  - Proxmox Backup Server (PBS)
  - OpenMediaVault VM for storage
  - Daglige backups av HA, Node-RED, Paperless
  - Cloud replikering (Backblaze B2 / Wasabi S3?)
- **Ansvar**: General AI (infrastruktur)
- **Status**: Planlagt, ikke startet
- **Notater**: KRITISK - ingen backup på plass nå!

### 2. PT1000 Værstasjon med ESPHome
- **Prioritet**: 🟡 Medium
- **Beskrivelse**: ESPHome-basert værstasjon med PT1000 temperatursensor
- **Hardware nødvendig**:
  - MAX31865 RTD breakout board (~50-100 kr fra AliExpress)
  - ESP32/ESP8266
  - PT1000 sensor (Regin PT1000 kanalsensor, allerede på plass?)
- **Konfigurasjon**: ESPHome YAML klar i CLAUDE.md
- **Integrasjon**: ESPHome → MQTT → HA
- **Status**: Venter på hardware-bestilling
- **Ansvar**: General AI (hardware) + React-HA (HA integration)

### 3. USB/IP Gateway for Zigbee/Z-Wave garasje
- **Prioritet**: 🟡 Medium
- **Beskrivelse**: RPi4-basert USB/IP server for remote Zigbee/Z-Wave dongles
- **Hardware nødvendig**:
  - RPi4 @ 10.12.0.30 (kan være eksisterende hardware)
  - Conbee II for Zigbee garasje
  - Z-Stick for Z-Wave garasje
- **LXC-er klare**:
  - Zigbee2MQTT Garasje (LXC 111 @ 10.12.0.26) - venter
  - Z-Wave JS UI Garasje (LXC 113 @ 10.12.0.28) - venter
- **Status**: Planlagt, venter på hardware-oppsett
- **Ansvar**: General AI

### 4. Energimonitoring dashboard-modul
- **Prioritet**: 🟢 Lav
- **Beskrivelse**: Strømforbruk og produksjon i React dashboard
- **Hardware nødvendig**: Strømmåler (Shelly EM / Tibber Pulse / Aeotec Z-Wave)
- **UI**: `EnergyModule.tsx` allerede eksisterer (tom/placeholder)
- **Status**: Planlagt, venter på hardware
- **Ansvar**: React-HA (når hardware er på plass)

### 5. LoRaWAN sensorer med ChirpStack
- **Prioritet**: 🟢 Lav
- **Beskrivelse**: Koble LoRaWAN gateway til ChirpStack og legge til sensorer i HA
- **ChirpStack**: Allerede satt opp (LXC 109 @ 10.12.0.40)
- **Gateway nødvendig**: Semtech UDP Packet Forwarder (hardware må kjøpes)
- **Sensorer**: Ukjent - må bestemmes basert på bruk
- **Status**: ChirpStack klar, venter på gateway-hardware
- **Ansvar**: General AI (hardware) + React-HA (HA integration)

### 6. Schneider SpaceLynk KNX programmering
- **Prioritet**: 🟡 Medium (når hardware ankommer)
- **Beskrivelse**: Lua-programmering for driftskritisk infrastruktur (lys, varme)
- **Hardware**: Bestilt, ikke ankommet
- **Arkitektur**: KNX = kritisk, HA = nice-to-have
- **Status**: Venter på hardware-levering
- **Ansvar**: General AI

### 7. "Når kommer Posten"-modul
- **Prioritet**: 🟢 Lav (nice-to-have)
- **Beskrivelse**: Dashboard-modul som viser forventet postleveringstid
- **API**: Bring/Posten API
- **UI**: Ny modul i React dashboard
- **Status**: Idé-fase, ikke påbegynt
- **Ansvar**: React-HA

---

## 🔍 PROBLEMER UNDER FEILSØKING

**INGEN ÅPNE FEILSØKINGSSAKER PER NÅ.**

### Tidligere løste problemer (for referanse)

#### Z-Stick USB I/O error (løst)
- **Problem**: `error -71 EPROTO` i Z-Wave JS UI
- **Løsning**: Fysisk reset ved å koble ut/inn Z-Stick
- **Dato**: 21-24. nov 2025
- **Status**: ✅ Løst, dokumentert i infrastructure-dump.md

#### Paperless Office-filer avvist (løst)
- **Problem**: "Unknown file extension" for .xlsx/.docx/.pptx
- **Løsning**: Office-watcher service som konverterer FØR consumer
- **Dato**: 27. nov 2025
- **Status**: ✅ Løst, service kjører

---

## 💡 IDEER (ikke prioritert ennå)

### Bilskilt-avlesing med Coral TPU
- **Beskrivelse**: AI-basert bilskilt-gjenkjenning ved innkjørsel
- **Hardware**: Google Coral TPU + dedikert kamera
- **Use case**: Automatisk åpne garasjeport, logg besøkende
- **Status**: Ambisjonsprosjekt, ikke planlagt
- **Ansvar**: General AI (hardware) + React-HA (automation)

### Paperless multi-user for jobb (Lasse-prosjekt)
- **Beskrivelse**: Felles Paperless-instans for 3-5 brukere på jobb
- **Arkitektur**: Owner-basert privacy, email-import per bruker
- **Servere**: 2x Proxmox på jobb (48 vCPU, 1TB RAM)
- **Status**: Lasse gjør research
- **Ansvar**: Lasse (project lead) + React-HA (support)

### Solceller/batteri-integrasjon
- **Beskrivelse**: Energimonitoring for fremtidig solcelleanlegg
- **Hardware**: Inverter (Fronius / SolarEdge / Huawei)
- **Dashboard**: Produksjon, netto forbruk, batteri-status
- **Status**: Langsiktig plan, ingen dato
- **Ansvar**: General AI (hardware) + React-HA (dashboard)

---

## 📦 UFERDIGE TESTER/DEPLOYMENTS

**INGEN UFERDIGE DEPLOYMENTS.**

Alt som er implementert er deployet til prod og fungerer.

---

## 🐛 KJENTE BUGS (ikke kritiske)

### Tekst-hopping i Media/Energi-moduler
- **Beskrivelse**: Dynamisk tekst "hopper" visuelt ved oppdatering
- **Påvirkning**: Kun kosmetisk, ingen funksjonsfeil
- **Frekvens**: Hvert 10. sekund (Media), hvert minutt (Energi)
- **Forsøkt løsning**: Flere CSS-fixes (positioning, containment, font-rendering)
- **Status**: ❌ Uløst, lav prioritet
- **Fil**: `MediaModule.tsx`, `EnergyModule.tsx`
- **Ansvar**: React-HA

### 3D-rendering over RDP
- **Beskrivelse**: `FloorPlan3D.tsx` (Three.js) renderer ikke riktig over Remote Desktop
- **Påvirkning**: Kun i dev-miljø, ikke prod
- **Årsak**: WebGL/GPU-akselerasjon fungerer ikke optimalt over RDP
- **Løsning**: Teste lokalt på maskinen (ikke over RDP)
- **Status**: ❌ Ikke en faktisk bug, forventet oppførsel
- **Ansvar**: React-HA

---

## 📚 DOKUMENTASJON SOM MANGLER

### Hva jeg MÅ dokumentere når jeg får tilgang

**Home Assistant:**
- [ ] Komplett entity-liste (alle lys, brytere, sensorer)
- [ ] Alle scenes (Borte, Hjemme, Stemning, Ferie)
- [ ] Lovelace dashboards (motorvarmer card dokumentert, andre?)
- [ ] HACS custom integrations (liste med versjoner)

**Node-RED:**
- [ ] Eksportere alle flows til JSON
- [ ] Dokumentere hver flow (formål, trigger, action)
- [ ] MQTT topic-struktur brukt i flows

**Grafana:**
- [ ] Liste over alle dashboards med screenshots
- [ ] InfluxDB queries og retention policies
- [ ] Alerts/notifications som er konfigurert

**Generelt:**
- [ ] Full VMID-kartlegging for alle LXC/VM-er
- [ ] InfluxDB IP-adresse og konfigurasjon
- [ ] React dashboard prod deployment-plan

---

## 🔄 MIGRERING TIL SUB-AGENT (dette dokumentet)

**Status**: 🚧 PÅGÅENDE

**Hva som er gjort:**
- ✅ CLAUDE.md (full kunnskapsbase)
- ✅ infrastructure-dump.md (IP, porter, tjenester)
- ✅ automations.md (alle automations, scripts, flows)
- ✅ wip.md (denne filen)
- ⏳ secrets-location.md (neste)
- ⏳ Kopiere filer til LXC 150
- ⏳ Git commit og push
- ⏳ Verifisere med General AI

**Mål**: Bli sub-agent under General AI i LXC 150 (10.12.0.150)

**Deadline**: Ingen hard deadline, men gjerne ferdig i dag (3. des 2025)

---

**Sluttnot**: Denne filen skal oppdateres hver gang jeg starter/fullfører arbeid, eller får nye ideer. Den skal gi General AI full oversikt over hva jeg holder på med til enhver tid.

**Sist oppdatert**: 2025-12-03
