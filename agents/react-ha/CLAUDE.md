# REACT-HA AGENT - KOMPLETT KUNNSKAPSBASE

**Agent**: React-HA Specialist for Saghaugen
**Opprettet**: Pre-2025 (eksisterte før multi-agent arkitektur)
**Migrert til sub-agent**: 3. desember 2025
**Parent Agent**: General AI (CTO for Saghaugen)

## 🎯 MIN ROLLE I DET STORE BILDET

Jeg er Home Assistant-spesialist for Saghaugen. General AI er CTO og tar overordnede beslutninger om infrastruktur, arkitektur og tekniske valg. Jeg fokuserer på:

- **Home Assistant** (prod + test) - konfigurasi, integrasjoner, automations
- **React Dashboard** - TypeScript/Vite webpanel for 10.1" entréskjerm
- **Node-RED** - avanserte automatiseringsflows
- **Grafana + InfluxDB** - visualisering og tidsseriedata
- **ChirpStack LoRaWAN** - network server for LoRa-sensorer
- **Paperless-NGX** - dokumentarkiv med email-import
- **Homepage** - service dashboard

**Hva jeg IKKE gjør:**
- Proxmox VM/LXC-oppsett (General AI)
- Nettverksinfrastruktur (General AI)
- Byggematerialer/elektriker (General AI)
- KNX SpaceLynk programmering (General AI)

---

## 📍 SAGHAUGEN - KONTEKST

**Adresse**: Trondsbuvegen 272, 2100 Skarnes (Sør-Odal kommune)
**Type**: Enebolig i skogsmiljø, nybygg/rehabilitering pågår
**Eier**: Ronny Smerud
**Nett**: Starlink (CG-NAT) med Cloudflare Tunnel for ekstern tilgang
**Domene**: saghaugen.no (DNS hos Domeneshop)

**Fysiske lokasjoner:**
- **Hus** (hovedbygning): 2 etasjer, entré-panel med 10.1" touchskjerm
- **Garasje/Låve**: Proxmox server, verksted, parkering
- **Avstand hus ↔ garasje**: ~50m, fri sikt for WiFi mesh

---

## 🖥️ SERVER-INFRASTRUKTUR (Oversikt)

**Proxmox Host**: 10.12.0.205 (garasje/låve)
- OS: Proxmox VE 9
- Root passord: 4pn44SJAg
- SSH: `ssh root@10.12.0.205` (passwordless med ~/.ssh/id_ed25519)

### Mine systemer (LXC/VM)

| System | VMID | IP | Port | Status | Kritisk |
|--------|------|----|----|--------|---------|
| **Home Assistant Prod** | 103 | 10.12.0.20 | 8123 | ✅ Prod | ⚠️ KRITISK |
| **Home Assistant Test** | ? | 10.12.0.9 | 8123 | ✅ Test | Nei |
| **Node-RED** | ? | 10.12.0.24 | 1880 | ✅ Running | ⚠️ KRITISK |
| **Grafana** | ? | 10.12.0.108 | 3000 | ✅ Running | Nei |
| **InfluxDB** | ? | ? | 8086 | ❓ (må verifiseres) | Nei |
| **ChirpStack** | 109 | 10.12.0.40 | 8080 | ✅ Running | Nei |
| **Paperless-NGX** | ? | 10.12.0.102 | 8000 | ✅ Running | Nei |
| **Homepage** | ? | 10.12.0.50 | 80 | ✅ Running | Nei |
| **Frigate NVR** | ? | 10.12.0.21 | 5000 | ✅ Running | Nei |
| **React Dashboard** | ? | ? | ? | ❓ (vite dev?) | Nei |

**VIKTIG:** VMID-er mangler for de fleste systemer - må kartlegges!

### Andre systemer (ikke mine, men må kjenne til)

| System | VMID | IP | Port | Eier |
|--------|------|----|----|------|
| **EMQX MQTT Broker** | ? | 10.12.0.22 | 1883/18083 | General AI |
| **ESPHome** | ? | 10.12.0.23 | 6052 | General AI |
| **Zigbee2MQTT (Hus)** | 110 | 10.12.0.25 | 8080 | General AI |
| **Zigbee2MQTT (Garasje)** | 111 | 10.12.0.26 | 8080 | General AI (venter USB/IP) |
| **Z-Wave JS UI (Hus)** | 112 | 10.12.0.27 | 8091 | General AI |
| **Z-Wave JS UI (Garasje)** | 113 | 10.12.0.28 | 8091 | General AI (venter USB/IP) |
| **Docker Services** | ? | 10.12.0.50 | flere | General AI |
| **Windows VM** | ? | 10.12.0.55 | 3389 | General AI |

---

## 🏠 HOME ASSISTANT - PRODUKSJON

**IP**: 10.12.0.20:8123
**VMID**: 103 (VM, ikke LXC)
**OS**: Home Assistant OS 16.3 (HAOS) - IKKE Ubuntu!
**Installasjon**: Home Assistant OS (full appliance med Supervisor)
**Config path**: `/mnt/data/supervisor/homeassistant/`

### Tilgangsmetoder (prioritert rekkefølge)

**1. QEMU Guest Agent via Proxmox (FUNGERER ✅)**
```bash
# Kjør kommandoer direkte på HA via Proxmox
ssh root@10.12.0.205 "qm guest exec 103 -- <kommando>"

# Eksempler:
ssh root@10.12.0.205 "qm guest exec 103 -- cat /mnt/data/supervisor/homeassistant/automations.yaml"
ssh root@10.12.0.205 "qm guest exec 103 -- ha core restart"
```

**2. HA CLI (inne på VM)**
```bash
# Via QEMU agent
ssh root@10.12.0.205 "qm guest exec 103 -- ha core restart"
ssh root@10.12.0.205 "qm guest exec 103 -- ha supervisor info"
```

**3. SSH addon (IKKE SATT OPP)**
- Krever at SSH addon installeres i HA
- Foreløpig ikke konfigurert

**4. REST API (krever token)**
- Trenger long-lived access token fra HA UI
- Token ikke lagret i General AI enda

### Viktige mapper (HAOS paths)
- `/mnt/data/supervisor/homeassistant/` - ALLE konfigurasjonsfiler
- `/mnt/data/supervisor/homeassistant/automations.yaml` - Automations
- `/mnt/data/supervisor/homeassistant/configuration.yaml` - Hovedkonfig
- `/mnt/data/supervisor/homeassistant/scripts.yaml` - Scripts
- `/mnt/data/supervisor/homeassistant/.storage/` - UI-genererte configs
- `/mnt/data/supervisor/homeassistant/custom_components/` - HACS og custom integrations
- `/mnt/data/supervisor/homeassistant/www/` - Static files (logos, etc.)

### Installerte integrasjoner
- **MQTT** (EMQX @ 10.12.0.22:1883)
  - User: `homeassistant`
  - Discovery aktivert
- **Z-Wave JS** (Z-Wave JS UI @ 10.12.0.27:3000 WebSocket)
  - Aeotec Z-Stick 7 Gen5+ via USB passthrough
  - Fibaro Wallplug (motorvarmer): `switch.motorvarmer`
- **Zigbee2MQTT** (via MQTT auto-discovery)
  - Conbee II @ 10.12.0.25
  - Hue gang-lys: `light.gang_lys` (0x0017880109400db6)
- **Frigate** (via HACS)
  - Camera entities: `camera.reolink_cx810_*`
- **Reolink** (native integration)
  - Camera @ 10.12.0.154
- **Yr.no** (værdata)
- **Sun** (soloppgang/nedgang for automatiseringer)

### Viktige entities

**Lys:**
- `light.gang_lys` - Hue gang 2. etg (Zigbee2MQTT)
- Mange flere lys (må kartlegges)

**Brytere:**
- `switch.motorvarmer` - Fibaro Wallplug for May sin bil (Z-Wave)

**Sensorer:**
- `sensor.motorvarmer_power` - Effekt (W)
- `sensor.motorvarmer_electric_consumption_kwh` - Forbruk (kWh)
- `weather.*` - Yr.no værdata
- Mange temperatur-sensorer (må kartlegges)

**Input Helpers** (configuration.yaml):
- `input_boolean.motorvarmer_mandag` til `*_søndag` - Ukeplan
- `input_datetime.motorvarmer_starttid` - Start-tid (default 07:00)
- `input_number.motorvarmer_varighet` - Minutter (auto-beregnet fra temp)
- `input_boolean.motorvarmer_enable` - Hovedbryter
- `input_text.motorvarmer_status` - Status-melding
- `input_datetime.motorvarmer_ferdig` - Ferdig-tid
- `input_boolean.utelys_auto` - Utelys automatikk on/off

### Automations (automations.yaml)

**Gang-lys:**
- `automation.gang_2_etg_dimme_til_1_kl_21_00` - Dimmer til 1% kl 21:00 (60s transition)
- `automation.gang_2_etg_sette_til_50_kl_09_00` - Setter til 50% kl 09:00 (60s transition)

**Motorvarmer:**
- `automation.motorvarmer_temperatur_varighet` - Beregner varighet fra utetemp
  - <-20°C → 60 min
  - <-10°C → 45 min
  - >-10°C → 30 min
- `automation.motorvarmer_planlagt_start` - Starter på valgte dager til valgt tid
- `automation.motorvarmer_auto_av` - Slår av etter varighet, setter status "Bilen er klar!"

**Utelys:**
- Soloppgang/nedgang med 30 min offset
- Manual override via `input_boolean.utelys_auto`

### Scripts (scripts.yaml)
- `script.motorvarmer_start_na` - Start motorvarmer nå med smart feedback

### API-tilgang
- **Long-lived token**: Genereres via UI (Profile → Security)
- **Miljøvariabel**: `VITE_HA_API_KEY` i React dashboard .env
- **REST API**: `http://10.12.0.20:8123/api/`
- **WebSocket API**: `ws://10.12.0.20:8123/api/websocket`

### Reload services (via API)
```bash
# Reload automations uten restart
curl -X POST http://10.12.0.20:8123/api/services/automation/reload \
  -H "Authorization: Bearer TOKEN"

# Andre reload services:
# - script.reload
# - input_boolean.reload
# - homeassistant.restart (full restart)
```

### Kjente problemer
- Ingen backup-rutine på plass ennå! ⚠️
- Entity registry kan bli stor - må ryddes periodisk
- Zigbee-enheter kan miste kobling (reconnect via Zigbee2MQTT)
- Z-Wave Z-Stick kan få USB I/O error (fysisk reset nødvendig)

---

## 🏠 HOME ASSISTANT - TEST

**IP**: 10.12.0.9:8123
**Formål**: Testing av nye integrations, automations og dashboard-endringer før prod

**Status**: Mindre vedlikeholdt, kan være utdatert

---

## 🔄 NODE-RED

**IP**: 10.12.0.24:1880
**OS**: Ubuntu LXC (unprivileged)
**Installasjon**: Manuell (Node.js 20.x LTS + npm install -g node-red)

### Systemd service
```bash
# /etc/systemd/system/node-red.service
[Service]
ExecStart=/usr/bin/node-red
User=ronny  # (eller node-red bruker?)
Restart=always
```

### Installerte nodes
- `node-red-contrib-home-assistant-websocket` - HA WebSocket integration

### Flows (viktige)
- **Utelys automatikk** - Soloppgang/nedgang med offset
- (Flere flows må dokumenteres når jeg får tilgang)

### Tilgang til HA
- WebSocket: `ws://10.12.0.20:8123/api/websocket`
- Token: Lagret i Node-RED flow credentials

### MQTT
- Broker: EMQX @ 10.12.0.22:1883
- Mange flows publiserer/subscriber til MQTT topics

---

## 📊 GRAFANA + INFLUXDB

**Grafana**: 10.12.0.108:3000
**InfluxDB**: IP ukjent (må finnes)

### Grafana dashboards
- System health monitoring
- HA sensor data visualization
- Strømforbruk (fremtidig)

### InfluxDB
- Tidsseriedata fra HA sensors
- Retention policy: Må defineres
- Backup: Må defineres

---

## 📡 CHIRPSTACK LoRaWAN

**IP**: 10.12.0.40:8080
**VMID**: 109
**OS**: Ubuntu 22.04 LXC (unprivileged)

### Komponenter
- ChirpStack v4.15.0 (Network Server + Application Server)
- ChirpStack Gateway Bridge v4.1.1
- PostgreSQL 14 database
- Redis cache

### Konfigurasjon
- Region: EU868 (868 MHz - Norge)
- MQTT integration: EMQX @ 10.12.0.22:1883
- API secret: Generert med `openssl rand -base64 32`
- Web GUI: admin/admin (default)

### Gateway
- Semtech UDP port 1700 for gateway kobling
- Ingen gateway koblet ennå (kommer)

### HA integration
- Via MQTT topics (uplink/downlink/events)
- Devices må legges manuelt i HA etter ChirpStack registration

---

## 📄 PAPERLESS-NGX

**IP**: 10.12.0.102:8000
**OS**: Ubuntu LXC

### Konfigurasjon
- **Email**: paperless@saghaugen.no
- **IMAP**: imap.domeneshop.no:993 (SSL)
- **User**: saghaugen3 (Domeneshop mailbox)
- **Polling**: Hvert 5. minutt

### Office-konvertering
- **LibreOffice 7.4.7 + unoconv** installert
- **Office-watcher service**: `/opt/paperless/scripts/office-watcher.sh`
  - Overvåker `/opt/paperless/consume/` hvert 10. sekund
  - Konverterer .xlsx/.docx/.pptx → PDF automatisk
  - Systemd service: `paperless-office-watcher.service`

### Email cleanup
- **Script**: `/opt/paperless/scripts/cleanup-emails.py`
- **Timer**: Daglig kl. 03:00
- **Regel**: Sletter leste emails eldre enn 7 dager

### Viktige mapper
- `/opt/paperless/consume/` - Drop zone for nye dokumenter
- `/opt/paperless/media/` - Lagrede PDFer
- `/opt/paperless/data/` - Database og index

---

## 🏠 HOMEPAGE DASHBOARD

**IP**: 10.12.0.50:80
**Docker**: Docker Compose oppsett

### Konfigurasjon
- YAML-basert (services.yaml, widgets.yaml, bookmarks.yaml)
- Environment variables:
  - `HOMEPAGE_VAR_HA_TOKEN` - HA API token
  - `HOMEPAGE_VAR_PROXMOX_USER` - root@pam!homepage
  - `HOMEPAGE_VAR_PROXMOX_PASS` - Proxmox API secret

### Custom CSS
- Stor Saghaugen logo (400px)
- Spesifikke selektorer for å ikke påvirke service-ikoner

### Services listed
- Home Assistant, Proxmox, Frigate, Grafana, ChirpStack, Paperless, etc.

### Bookmarks
- Kursfortegnelse Saghaugen (⚡)
- Servert via nginx-static container

---

## 🎨 REACT DASHBOARD (Saghaugen Infopanel)

**Repo**: Claude_HA-React (dette prosjektet)
**Tech Stack**: React 19 + TypeScript + Vite
**Deployment**: Dev-server for nå (ingen prod deployment ennå)

### Komponenter
- `FloorPlan.tsx` - Hovedkomponent med SVG 2D floorplan
- `WeatherModule.tsx` - Yr.no + HA weather entities
- `AlarmModule.tsx` - Alarm kontroll med keypad
- `SceneModule.tsx` - HA scenes og scripts
- `MediaModule.tsx` - Sonos/AppleTV kontroll
- `CameraModule.tsx` - Frigate/Reolink live stream
- `EnergyModule.tsx` - Strømforbruk (planlagt)
- `NotificationModule.tsx` - Varsling
- `ClockModule.tsx` - Digital klokke

### API-integrasjon
- `src/services/homeAssistant.ts` - HA REST API wrapper
- Bearer token autentisering via `.env`
- Vite proxy for CORS i dev mode

### Vite proxy (vite.config.ts)
```typescript
proxy: {
  '/api': {
    target: 'http://10.12.0.20:8123',
    headers: { 'Authorization': `Bearer ${process.env.VITE_HA_API_KEY}` }
  }
}
```

### Deployment-plan
- Provisorisk til vår 2026 (gulv-skifte i entré)
- 10.1" touchskjerm på Raspberry Pi 4B med PoE HAT
- Kjøkken-panel: 7" RPi skjerm for musikk-kontroll

### Kjente bugs
- Tekst-hopping i Media/Energi-moduler (kosmetisk)
- 3D-rendering (FloorPlan3D.tsx) fungerer ikke over RDP

---

## 📡 MQTT TOPIC-STRUKTUR

**Broker**: EMQX @ 10.12.0.22:1883

### Topic-namespaces (det jeg vet om)

**Zigbee2MQTT:**
- `zigbee2mqtt/hus/#` - Alle enheter i hus
- `zigbee2mqtt/garasje/#` - Alle enheter i garasje (fremtidig)

**Z-Wave JS UI:**
- `zwave/hus/#` - Z-Wave enheter i hus
- `zwave/garasje/#` - Z-Wave enheter i garasje (fremtidig)

**ChirpStack:**
- `application/+/device/+/event/up` - LoRa uplink
- `application/+/device/+/event/down` - LoRa downlink

**Home Assistant:**
- `homeassistant/#` - HA discovery topics (auto-generated)

**Node-RED:**
- Mange custom topics (må kartlegges)

---

## 🗄️ BACKUP-STRATEGI (MANGLER!)

⚠️ **KRITISK**: Ingen systematisk backup på plass!

**Hva som MÅ backupes:**
- Home Assistant `/config/` - KRITISK
- Node-RED flows - KRITISK
- Paperless-NGX dokumenter - Viktig
- Grafana dashboards - Nice-to-have
- ChirpStack device registrations - Nice-to-have

**Plan (ikke implementert):**
- Proxmox Backup Server
- OpenMediaVault VM
- Cloud replikering (Backblaze B2 / Wasabi S3)

---

## 🔐 SECRETS & CREDENTIALS

**Hvor de ligger (IKKE verdiene, kun plasseringer):**

### Home Assistant
- `/config/secrets.yaml` - HA secrets file
- `/config/.storage/` - OAuth tokens, integrations
- Long-lived tokens: Genereres via UI

### MQTT
- EMQX Web GUI (10.12.0.22:18083) → Users
- User: `homeassistant` (må ha passord lagret et sted)
- User: `Zigbee2MQTT_hus` / Zigbee2024!
- User: `ZWave_hus` / Zigbee2024!

### Proxmox
- Root passord: 4pn44SJAg (JA, dette er hardkodet flere steder - dårlig praksis!)

### SSH-nøkler
- `~/.ssh/id_ed25519` - Proxmox root
- `~/.ssh/id_ed25519_ha` - Home Assistant
- `~/.ssh/config` - SSH alias-config

### API tokens
- HA long-lived tokens: Må genereres og lagres i `.env` files
- Proxmox API token: `root@pam!homepage` + secret
- ChirpStack API secret: Generert, lagret i ChirpStack config

---

## 🔧 TROUBLESHOOTING - VANLIGE PROBLEMER

### Home Assistant
**Problem**: Automation endringer ikke lastet inn
**Løsning**: `POST /api/services/automation/reload` eller restart HA

**Problem**: Entity ikke funnet
**Løsning**: `ssh homeassistant@10.12.0.20 "grep -i 'entity_id' /config/.storage/core.entity_registry"`

**Problem**: Zigbee enhet offline
**Løsning**: Sjekk Zigbee2MQTT @ 10.12.0.25:8080, re-pair hvis nødvendig

### Z-Wave
**Problem**: Z-Stick USB I/O error
**Løsning**: Fysisk koble ut/inn Z-Stick (error -71 EPROTO)

**Problem**: Z-Wave JS UI ikke starter
**Løsning**: AppArmor issues - sjekk `lxc.apparmor.profile: unconfined` i LXC config

### MQTT
**Problem**: Enheter ikke synlig i HA
**Løsning**: Sjekk MQTT integration discovery er aktivert

### Paperless-NGX
**Problem**: Office-filer ikke importert
**Løsning**: Sjekk `systemctl status paperless-office-watcher`

---

## 📝 PÅGÅENDE ARBEID (WIP)

**Hva jeg jobbet med sist:**
- Gang-lys automatisering (✅ ferdig)
- Motorvarmer-system for May (✅ ferdig)
- Passwordless SSH til HA (✅ ferdig)

**Hva som er planlagt:**
- PT1000 værstasjon med ESPHome (hardware må bestilles)
- USB/IP gateway for Zigbee/Z-Wave garasje (RPi4 @ 10.12.0.30)
- Energimonitoring i dashboard (strømmåler må kjøpes)
- Backup-løsning (PBS + OMV)

**Hva som er "hacky" og bør fikses:**
- Proxmox root passord hardkodet mange steder
- Ingen systematisk backup
- VMID-er ikke kartlagt for alle systemer
- React dashboard kjører dev-server, ikke prod build
- InfluxDB IP ukjent

---

## 🤝 SAMARBEID MED GENERAL AI

**Hvordan spawne meg:**
General AI kan spawne meg som sub-agent når han trenger HA-ekspertise.

**Hva jeg forventer av input:**
- Klar beskrivelse av problem/oppgave
- Hvilke systemer som er involvert
- Om det er prod eller test

**Hva jeg leverer tilbake:**
- Løsningsforslag med HA-konfig
- YAML-filer for automations/scripts
- Deployment-instruksjoner
- Dokumentasjon av endringer

**Eskalering til General AI:**
- VM/LXC-endringer
- Nettverks-konfig
- Breaking changes som påvirker andre systemer
- Major version upgrades av kritiske tjenester

---

## 📚 RESSURSER & DOKUMENTASJON

**Offisiell dokumentasjon:**
- Home Assistant: https://www.home-assistant.io/docs/
- Node-RED: https://nodered.org/docs/
- ChirpStack: https://www.chirpstack.io/docs/
- Paperless-NGX: https://docs.paperless-ngx.com/

**Lokale filer:**
- `/config/` på HA-server
- Git repo: Claude_HA-React
- Denne filen (CLAUDE.md)

---

## 🏁 SLUTTNOT

Dette er min komplette kunnskapsbase per 3. desember 2025. Det finnes sikkert ting jeg har glemt eller ikke dokumentert - jeg vil oppdatere dette etter hvert som jeg husker mer eller General AI spør om ting jeg ikke har dekket.

**Hvis General AI trenger mer info:**
- Spør! Jeg vil utdype alt som mangler
- Sjekk faktiske konfig-filer på serverne
- Koordiner med Ronny for ting jeg ikke har tilgang til

**Neste steg:**
- Eksportere denne filen til LXC 150
- Lage infrastructure-dump.md
- Lage automations.md
- Lage wip.md
- Lage secrets-location.md
- Git commit og verifisere med General AI

---

**Versjon**: 1.0 (Initial migration export)
**Sist oppdatert**: 2025-12-03
**Av**: React-HA Agent (Claude Code)
