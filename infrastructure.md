# Saghaugen Proxmox Infrastructure

Dokumentert: 2025-12-03

## Proxmox Host: pve-core
- **IP**: 10.12.0.205
- **SSH**: Passwordless SSH konfigurert for General AI
- **OS**: Debian GNU/Linux, Kernel 6.8.12-4-pve
- **Proxmox Version**: 8.3.0

## Arkitektur: Kritisk vs Nice-to-Have

### Kritisk Infrastruktur (Desentralisert - Fungerer uten Proxmox/HA)

**KNX**
- Lys på/av via fysiske brytere
- Fungerer alltid, uavhengig av servere
- Grunnleggende lysstyring

**DALI**
- Lysstyring
- Desentralisert operasjon

**Modbus**
- Industriell standard
- Robust og pålitelig

**LoRaWAN**
- Egenbygd gateway: RaspberryPi + Sx1202
- ChirpStack server (LXC 109)
- Kritiske sensorer

**Nettverk og Sikkerhet**
- Unifi UDM-Pro med Unifi UPS (batteribackup)
- Unifi Protect på UDM-Pro
- Alle kameraer fra Access-systemet koblet til Unifi Protect
- Sikkerhetskameraer fungerer ved strømbrudd (så lenge UPS holder)

### Nice-to-Have Infrastruktur (Sentralisert via HomeAssistant)

**Zigbee/Z-Wave**
- Komplekse scener og automasjoner
- Billige sensorer
- Avhengig av HomeAssistant og Proxmox
- Hvis Proxmox går ned: mister fancy features, men grunnleggende funksjoner (KNX) fungerer

**Designprinsipp**: Alt kritisk skal fungere selv om hele Proxmox-infrastrukturen går ned. Zigbee/Z-Wave er kun for komfort og avanserte features.

### Fremtidige Planer

**Garasje USB/IP Architecture**:
- RPi4 (CM4 på carrier board) med PoE Hat i garasjen
- Z-Wave og Zigbee dongles plugget i RPi4
- USB/IP eksponerer dongles over nettverk
- Proxmox binder USB-enheter via USB/IP client
- LXC 111 (zigbee2mqtt-garasje) og LXC 113 (zwave-js-ui-garasje) får tilgang som om lokalt tilkoblet
- Ingen failover - garasje-automatisering er nice-to-have

**Energi og Strømforsyning**:
- Solceller
- Batteripakker
- Hybrid-invertere
- Diesel aggregat (tilkoblet inverter som backup)
- **Begrunnelse**: Langt til skogs - strømbrudd kan ta tid å fikse
- **Strategi**: Solceller + batteri for daglig bruk, diesel aggregat lader batterier ved langvarig overskyet vær eller strømbrudd
- Målet er praktisk talt ubegrenset autonomi - kan kjøre kritisk infrastruktur (KNX, nettverk, kameraer) på ubestemt tid

**Infrastruktur mellom bygninger**:
- **Nåværende**: Unifi U7 Outdoor mesh nettverk
- **Fremtidig**: Fiber + strømkabel mellom garasje/låve og hus
- Legges når kabelgrøft graves
- Mesh fungerer som permanent backup til fiber

## Virtual Machines (QEMU)

### VM 103 - homeassistant
- **Status**: Running
- **Memory**: 6144 MB (6 GB)
- **Disk**: 100 GB
- **Tags**: community-script
- **Beskrivelse**: HomeAssistant prod-instans

### VM 200 - win11-admin
- **Status**: Running
- **Memory**: 12000 MB (12 GB)
- **Disk**: 100 GB
- **Beskrivelse**: Windows 11 admin-maskin hvor General AI kjører

## LXC Containers

### LXC 100 - docker-services
- **Status**: Running
- **CPU**: 2 cores
- **Beskrivelse**: Docker-baserte tjenester

### LXC 101 - homebox
- **Status**: Running
- **CPU**: 1 core
- **Tags**: community-script, household, inventory
- **Beskrivelse**: Household inventory management

### LXC 102 - paperless-ngx
- **Status**: Running
- **CPU**: 2 cores
- **Tags**: community-script, document, management
- **Beskrivelse**: Dokumentarkiv/håndtering

### LXC 104 - esphome
- **Status**: Running
- **CPU**: 2 cores
- **Tags**: automation, community-script
- **Beskrivelse**: ESPHome for custom IoT-enheter

### LXC 105 - frigate
- **Status**: Running
- **CPU**: 4 cores
- **Beskrivelse**: Video overvåkning med AI object detection

### LXC 106 - emqx
- **Status**: Running
- **CPU**: 2 cores
- **Tags**: community-script, mqtt
- **Beskrivelse**: Dedikert MQTT broker (EMQ)

### LXC 107 - node-red
- **Status**: Running
- **CPU**: 2 cores
- **Beskrivelse**: Node-RED for automasjonslogikk

### LXC 108 - grafana
- **Status**: Running
- **CPU**: 1 core
- **Tags**: community-script, monitoring, visualization
- **Beskrivelse**: Grafana visualisering og monitoring

### LXC 109 - chirpstack
- **Status**: Running
- **CPU**: 2 cores
- **Beskrivelse**: ChirpStack LoRaWAN network server

### LXC 110 - zigbee2mqtt
- **Status**: Running
- **CPU**: 1 core
- **Beskrivelse**: Zigbee2MQTT for huset

### LXC 111 - zigbee2mqtt-garasje
- **Status**: Stopped
- **Beskrivelse**: Zigbee2MQTT for garasjen (ikke i bruk)

### LXC 112 - zwave-js-ui-hus
- **Status**: Running
- **CPU**: 2 cores
- **Beskrivelse**: Z-Wave JS UI for huset

### LXC 113 - zwave-js-ui-garasje
- **Status**: Stopped
- **Beskrivelse**: Z-Wave JS UI for garasjen (ikke i bruk)

### LXC 150 - claude-agents
- **Status**: Running
- **IP**: 10.12.0.145
- **CPU**: 2 cores
- **Memory**: 2048 MB
- **Disk**: 20 GB
- **OS**: Ubuntu 24.04
- **User**: ronny (passwordless sudo)
- **Beskrivelse**: Dedikert Linux-miljø for alle Claude Code agenter
- **Installert**:
  - Claude Code CLI v2.0.58
  - Node.js 20.x
  - Git, SSH, build-essential
  - Passwordless SSH til Proxmox host og alle VM/LXC
  - SSH keys: general-ai@saghaugen.no (ed25519)
- **Repos**:
  - `/home/ronny/ClaudeCodeProjects/GeneralAI/` - General AI (CTO) monorepo
  - Inkluderer `agents/react-ha/` sub-agent
- **MCP Servers**: Playwright, Context7
- **Tilgang**: `ssh ronny@10.12.0.145` eller via Proxmox: `pct enter 150`
- **Start agent**:
  ```bash
  ssh ronny@10.12.0.145
  cd /home/ronny/ClaudeCodeProjects/GeneralAI/
  claude
  ```

## Storage

- **local**: 15.2% brukt
- **local-lvm**: 34.0% brukt
- **s11**: Ekstern storage

## Nettverk

### Unifi Infrastructure
- **UDM-Pro**: Hovednettverk gateway
  - Unifi Protect kjører her
  - Unifi UPS tilkoblet (batteribackup)
  - Access-systemets kameraer koblet til Protect
- **Switcher**: Unifi (blanding av modeller)
- **Access Points**: U7 Outdoor (2 stk - ett per bygg)
  - **Nåværende**: Mesh mellom hus og garasje/låve
  - **Fremtidig**: Dedikerte access points når fiber er på plass
- **ISP**: Starlink (fiber er bestilt, leveringsdato uklar)
- **Nåværende setup**: Mesh via U7 Outdoor mellom bygninger
- **Fremtidig plan**:
  - Fiber-link mellom bygninger (når kabelgrøft er gravd)
  - U7'ene blir vanlige access points (ikke mesh)
  - Starlink, UDM og switcher flyttes til låven

### Proxmox Nettverk
- **SDN**: localnetwork (pve-core)

## Notater

### Claude Code Agenter
- **General AI (CTO)**: Migrert til LXC 150 (claude-agents) - dedikert Linux-miljø
- **Claude Code "React-HA"**: Klar for migrering til LXC 150
- **Legacy setup**: WIN11-ADMIN (VM 200) hadde begge agenter tidligere (Windows-basert)
- **Fordeler med LXC 150**:
  - Native Linux-miljø (raskere, mer stabil)
  - Dedikert container for agenter
  - Enklere å administrere og oppdatere
  - Passwordless SSH til Proxmox og alle VM/LXC
  - Full tilgang til infrastrukturen
- **MCP Servers**: Playwright, Context7 (Filesystem via standard Claude Code)

### Status
- **Aktive**: 12 LXC containere (inkl. ny LXC 150) + 2 VM'er
- **Stoppede**: LXC 111 og 113 (garasje - venter på RPi4 CM4 med USB/IP setup)
- Hoveddelen av smarthus-infrastrukturen kjører på LXC for effektivitet
- Claude Code agenter migrert fra Windows VM til dedikert LXC

### Sikkerhet og Redundans
- **Kritiske funksjoner** (KNX, DALI, Modbus, LoRaWAN) er desentraliserte
- **Ved Proxmox-feil**: Grunnleggende lys og kritiske sensorer fungerer fortsatt
- **Ved strømbrudd**:
  - UDM-Pro med UPS holder nettverk og kameraer oppe
  - Frigate (LXC 105) på Proxmox vil gå ned, men Unifi Protect fungerer fortsatt
  - Fremtidig: Solceller + batterier + hybrid-inverter + aggregat for lengre autonomi
- **Nice-to-have funksjoner** (Zigbee/Z-Wave scener) krever Proxmox
