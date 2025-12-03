# INFRASTRUCTURE DUMP - Konkret teknisk informasjon

**Generert**: 2025-12-03
**Formål**: Rask referanse for General AI når han trenger tekniske detaljer

---

## 🌐 NETTVERKSOVERSIKT

**Subnet**: 10.12.0.0/24
**Gateway**: 10.12.0.1 (UniFi UDM-Pro)
**DNS**: Via UDM-Pro (Starlink upstream)
**Ekstern tilgang**: Cloudflare Tunnel (saghaugen.no)

---

## 🖥️ ALLE SYSTEMER (IP-TABELL)

| IP | Port | Tjeneste | VMID | OS | Eier | Status |
|----|------|----------|------|----|------|--------|
| 10.12.0.1 | - | UniFi UDM-Pro | - | UniFi OS | General AI | ✅ |
| 10.12.0.9 | 8123 | Home Assistant Test | ? | Ubuntu 22.04 | React-HA | ✅ |
| 10.12.0.20 | 8123 | **Home Assistant Prod** | ? | Ubuntu 22.04 | React-HA | ✅ ⚠️ KRITISK |
| 10.12.0.21 | 5000 | Frigate NVR | ? | LXC | React-HA | ✅ |
| 10.12.0.22 | 1883, 18083 | EMQX MQTT Broker | ? | LXC | General AI | ✅ |
| 10.12.0.23 | 6052 | ESPHome | ? | LXC | General AI | ✅ |
| 10.12.0.24 | 1880 | **Node-RED** | ? | LXC | React-HA | ✅ ⚠️ KRITISK |
| 10.12.0.25 | 8080 | Zigbee2MQTT (Hus) | 110 | Ubuntu LXC | General AI | ✅ |
| 10.12.0.26 | 8080 | Zigbee2MQTT (Garasje) | 111 | Ubuntu LXC | General AI | ⏸️ (venter USB/IP) |
| 10.12.0.27 | 8091, 3000 | Z-Wave JS UI (Hus) | 112 | Ubuntu LXC | General AI | ✅ |
| 10.12.0.28 | 8091, 3000 | Z-Wave JS UI (Garasje) | 113 | Ubuntu LXC | General AI | ⏸️ (venter USB/IP) |
| 10.12.0.30 | - | USB/IP Gateway #1 (planlagt) | - | RPi4 | General AI | ❌ Planlagt |
| 10.12.0.31 | - | USB/IP Gateway #2 (planlagt) | - | RPi4 | General AI | ❌ Planlagt |
| 10.12.0.40 | 8080 | **ChirpStack LoRaWAN** | 109 | Ubuntu LXC | React-HA | ✅ |
| 10.12.0.50 | 80, 9000, 9443 | Docker Services (Homepage, Portainer) | ? | Ubuntu LXC | General AI | ✅ |
| 10.12.0.51 | - | UniFi U7 Outdoor (hus) | - | UniFi AP | General AI | ✅ |
| 10.12.0.52 | - | UniFi U7 Outdoor (låve, planlagt) | - | UniFi AP | General AI | ❌ Planlagt |
| 10.12.0.55 | 3389 | Windows 10 VM | ? | Windows 10 | General AI | ✅ |
| 10.12.0.102 | 8000 | **Paperless-NGX** | ? | Ubuntu LXC | React-HA | ✅ |
| 10.12.0.108 | 3000 | **Grafana** | ? | LXC | React-HA | ✅ |
| 10.12.0.150 | - | Claude Agents LXC | 150 | Ubuntu LXC | General AI | ✅ |
| 10.12.0.154 | 554 (RTSP), 80 | Reolink CX810 #1 | - | Kamera | React-HA | ✅ |
| 10.12.0.205 | 8006 | **Proxmox Host** | - | Proxmox VE 9 | General AI | ✅ |

**MANGLER INFO:**
- InfluxDB IP (må finnes via `pct list` eller nmap)
- VMID for de fleste LXC/VM-er (må kartlegges)
- React Dashboard deployment-IP (kjører dev-server på Windows VM for nå)

---

## 🔗 AVHENGIGHETER MELLOM TJENESTER

### Start-rekkefølge (viktig ved reboot)

1. **EMQX MQTT Broker** (10.12.0.22) - ALT er avhengig av MQTT
2. **Zigbee2MQTT** (10.12.0.25) - Enheter må være online før HA
3. **Z-Wave JS UI** (10.12.0.27) - Enheter må være online før HA
4. **Home Assistant Prod** (10.12.0.20) - Hovedsystem
5. **Node-RED** (10.12.0.24) - Bruker HA WebSocket
6. **Grafana + InfluxDB** - Logger fra HA
7. **Homepage, Paperless, Frigate** - Standalone, ingen hard dependencies

**Kritisk hvis nede:**
- EMQX → Alt MQTT-basert bryter sammen
- HA Prod → Ingen smarthus-kontroll
- Node-RED → Mange automatiseringer stopper

---

## 📁 FILSYSTEM-STRUKTURER

### Home Assistant Prod (10.12.0.20)

```
/config/
├── automations.yaml          # UI-genererte automations
├── scripts.yaml              # Scripts
├── configuration.yaml        # Hovedkonfig + input helpers
├── secrets.yaml              # Secrets (passord, tokens)
├── .storage/
│   ├── core.entity_registry  # Alle entities
│   ├── core.device_registry  # Alle devices
│   └── ...
├── custom_components/
│   └── hacs/                 # HACS + custom integrations
├── www/
│   └── saghaugen-logo.png    # Logo for frontend
└── deps/                     # Python dependencies
```

### Node-RED (10.12.0.24)

```
/home/ronny/.node-red/        # (eller /opt/node-red?)
├── flows.json                # Alle flows
├── flows_cred.json           # Encrypted credentials
├── settings.js               # Node-RED config
└── node_modules/             # Installerte nodes
```

### Paperless-NGX (10.12.0.102)

```
/opt/paperless/
├── consume/                  # Drop zone for nye filer
├── media/                    # Lagrede PDFer
├── data/                     # Database og index
└── scripts/
    ├── office-watcher.sh     # Office → PDF converter
    └── cleanup-emails.py     # Email cleanup script
```

### ChirpStack (10.12.0.40)

```
/etc/chirpstack/
├── chirpstack.toml           # Hovedkonfig
└── region_eu868.toml         # Region-config

PostgreSQL database: `chirpstack`
Redis: localhost
```

---

## 🔌 PORTER OG PROTOKOLLER

| Service | Protocol | Port(s) | Beskrivelse |
|---------|----------|---------|-------------|
| Home Assistant | HTTP | 8123 | Web UI + REST API |
| Home Assistant | WebSocket | 8123 | `/api/websocket` |
| EMQX MQTT | MQTT | 1883 | Broker (plain) |
| EMQX MQTT | HTTP | 18083 | Web management GUI |
| Zigbee2MQTT | HTTP | 8080 | Web frontend |
| Z-Wave JS UI | HTTP | 8091 | Web frontend |
| Z-Wave JS UI | WebSocket | 3000 | Z-Wave JS server |
| Node-RED | HTTP | 1880 | Flow editor |
| Grafana | HTTP | 3000 | Dashboards |
| InfluxDB | HTTP | 8086 | Database API |
| ChirpStack | HTTP | 8080 | Web GUI |
| ChirpStack | UDP | 1700 | Semtech Packet Forwarder (gateway) |
| Paperless-NGX | HTTP | 8000 | Web UI |
| Homepage | HTTP | 80 | Dashboard |
| Portainer | HTTPS | 9443 | Docker management |
| Frigate | HTTP | 5000 | NVR web UI |
| Reolink Kamera | RTSP | 554 | Video stream |
| Proxmox | HTTPS | 8006 | Web management |
| UniFi UDM-Pro | HTTPS | 443 | UniFi Network UI |

---

## ⏰ CRON JOBS & SCHEDULED TASKS

### Paperless-NGX

**Email cleanup (systemd timer)**:
- Timer: `paperless-email-cleanup.timer`
- Schedule: Daglig kl. 03:00
- Script: `/opt/paperless/scripts/cleanup-emails.py`
- Beskrivelse: Sletter leste emails eldre enn 7 dager

**Office watcher (systemd service)**:
- Service: `paperless-office-watcher.service`
- Type: Continuous (ikke timer)
- Script: `/opt/paperless/scripts/office-watcher.sh`
- Beskrivelse: Overvåker consume/ og konverterer Office → PDF hvert 10. sek

### Home Assistant

**Automation-baserte schedules** (ikke cron):
- Gang-lys dimming kl. 21:00 og 09:00
- Motorvarmer planlagt start (user-defined tid)
- Utelys soloppgang/nedgang automation

---

## 🔒 SIKKERHET & BRANNMURER

### Proxmox Firewall
- Status: Ukjent (må sjekkes)
- LXC-containere har sannsynligvis ingen firewall

### LXC-containers
- Ingen iptables eller ufw konfigurert (må verifiseres)
- Alle tjenester eksponert på LAN (10.12.0.0/24)

### Ekstern tilgang
- **Cloudflare Tunnel** for saghaugen.no
- Ingen direkte port forwarding (Starlink CG-NAT)
- SSH kun på LAN (ikke eksponert)

---

## 📦 BACKUP-STATUS

⚠️ **KRITISK: INGEN SYSTEMATISK BACKUP PÅ PLASS!**

**Hva som finnes:**
- Git repos for kod (Claude_HA-React, andre?)
- Manuelle snapshots? (må sjekkes i Proxmox)

**Hva som MÅ backupes daglig:**
- HA `/config/` - KRITISK
- Node-RED flows - KRITISK
- Paperless documents - VIKTIG

**Hva som MÅ backupes ukentlig:**
- Grafana dashboards
- ChirpStack device registrations
- LXC configs (`/etc/pve/lxc/*.conf`)

---

## 🔧 SYSTEMD SERVICES (Per system)

### Home Assistant (10.12.0.20)
```bash
# Må sjekkes - sannsynligvis:
systemctl status home-assistant@homeassistant.service
```

### Node-RED (10.12.0.24)
```bash
systemctl status node-red.service
# User: ronny (eller node-red?)
```

### Paperless-NGX (10.12.0.102)
```bash
systemctl status paperless-webserver.service
systemctl status paperless-consumer.service
systemctl status paperless-office-watcher.service
systemctl status paperless-email-cleanup.timer
```

### Zigbee2MQTT (10.12.0.25)
```bash
systemctl status zigbee2mqtt.service
# User: zigbee2mqtt
```

### Z-Wave JS UI (10.12.0.27)
```bash
systemctl status docker.service  # (Docker Compose setup)
docker ps                         # zwavejs/zwave-js-ui container
```

### ChirpStack (10.12.0.40)
```bash
systemctl status chirpstack.service
systemctl status chirpstack-gateway-bridge.service
systemctl status postgresql.service
systemctl status redis.service
```

---

## 🐛 KJENTE QUIRKS & WORKAROUNDS

### Z-Wave Z-Stick USB I/O Error
**Symptom**: `error -71 EPROTO` i Z-Wave JS UI logs
**Årsak**: USB-kommunikasjonsfeil
**Fix**: Fysisk koble ut og inn Z-Stick (ikke software reset)

### Zigbee-enheter mister kobling
**Symptom**: Entity unavailable i HA
**Årsak**: Zigbee mesh routing issues
**Fix**: Re-pair enhet via Zigbee2MQTT web UI

### Paperless Office-filer avvist
**Symptom**: "Unknown file extension" error
**Årsak**: Paperless consumer sjekker filtype FØR pre-consume script
**Fix**: Office-watcher service konverterer FØR consumer ser filen

### HA automations ikke lastet
**Symptom**: Endringer i automations.yaml ikke aktive
**Årsak**: Må reload
**Fix**: `POST /api/services/automation/reload` eller restart HA

### AppArmor blokkerer Docker i LXC
**Symptom**: Docker fails to start i LXC
**Årsak**: AppArmor security i Proxmox
**Fix**: `lxc.apparmor.profile: unconfined` i LXC config

---

## 📊 RESSURSFORBRUK (estimert)

| System | vCPU | RAM | Disk | Lastenivå |
|--------|------|-----|------|-----------|
| HA Prod | 4 | 8 GB | 100 GB | Medium |
| HA Test | 4 | 8 GB | 100 GB | Lav |
| Node-RED | 2 | 2 GB | 16 GB | Lav |
| Grafana | 2 | 2 GB | 32 GB | Lav |
| InfluxDB | 2 | 4 GB | 100 GB | Medium |
| ChirpStack | 2 | 2 GB | 32 GB | Lav |
| Paperless-NGX | 2 | 4 GB | 100 GB | Lav |
| Frigate | 4 | 4 GB | 100 GB | Medium-High |
| Zigbee2MQTT | 1 | 1 GB | 8 GB | Veldig lav |
| Z-Wave JS UI | 2 | 2 GB | 16 GB | Lav |

**Total**: ~30 vCPU, ~40 GB RAM, ~700 GB disk (grovt estimat)

---

## 🔍 VERKTØY FOR FEILSØKING

### Sjekke alle LXC/VM-er
```bash
ssh proxmox "pct list"          # LXC-containere
ssh proxmox "qm list"            # VM-er
```

### Finne IP fra VMID
```bash
ssh proxmox "pct exec <VMID> -- hostname -I"
```

### Sjekke entity i HA
```bash
ssh homeassistant@10.12.0.20 "grep -i 'entity_name' /config/.storage/core.entity_registry"
```

### Reload HA services
```bash
curl -X POST http://10.12.0.20:8123/api/services/automation/reload \
  -H "Authorization: Bearer TOKEN"
```

### Sjekke MQTT topics
```bash
# Fra hvilken som helst maskin med mosquitto-clients
mosquitto_sub -h 10.12.0.22 -t '#' -v
```

---

**Sluttnot**: Denne filen inneholder det jeg vet om infrastrukturen. Mye må verifiseres ved å faktisk logge på systemene og sjekke.

**Sist oppdatert**: 2025-12-03
