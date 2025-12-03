# PRIORITERT PLAN - Infrastruktur-forbedringer

**Opprettet**: 2025-12-04
**Av**: General AI
**Status**: Aktiv

---

## 🔴 KRITISK (må fikses ASAP)

### 1. Backup-løsning
**Problem**: INGEN systematisk backup på plass!
**Risiko**: Total datatap ved hardware-feil, brann, eller korrupsjon
**Hva må backupes**:
- HA config (`/mnt/data/supervisor/homeassistant/`) - KRITISK
- Node-RED flows - KRITISK
- Paperless-NGX dokumenter - VIKTIG
- Proxmox VM/LXC configs - VIKTIG

**Forslag til løsning**:
1. Proxmox Backup Server (PBS) på separat disk/NAS
2. Daglige snapshots av kritiske VM/LXC
3. Off-site backup til jobb-servere via ZeroTier

**Estimat**: Medium kompleksitet

---

### 2. HA API Token for General AI
**Problem**: Kan ikke bruke HA REST API uten token
**Hvorfor viktig**: QEMU guest agent fungerer, men API er renere og raskere
**Løsning**:
1. Generer long-lived token i HA UI
2. Lagre sikkert (ikke i Git!)
3. Dokumenter i secrets-location.md

**Estimat**: 5 minutter

---

## 🟡 VIKTIG (bør fikses snart)

### 3. SSH-tilgang fra LXC 150 til HA
**Problem**: Må gå via Proxmox QEMU agent for å nå HA
**Hvorfor viktig**: Enklere og raskere tilgang for sub-agenter
**Løsning**:
1. Installer SSH addon i HA (via Supervisor)
2. Legg til General AI sin public key
3. Test passwordless SSH

**Estimat**: 15-30 minutter

---

### 4. Kartlegge alle VMID-er
**Problem**: Mange systemer har ukjent VMID
**Hvorfor viktig**: Lettere feilsøking og dokumentasjon
**Løsning**: Kjør `pct list` og `qm list`, oppdater dokumentasjon

**Status**: Delvis gjort - mangler noen LXC-er

**Kjent:**
- VMID 100: docker-services
- VMID 101: homebox
- VMID 102: paperless-ngx
- VMID 103: homeassistant (VM)
- VMID 104: esphome
- VMID 105: frigate
- VMID 106: emqx
- VMID 107: node-red
- VMID 108: grafana
- VMID 109: chirpstack
- VMID 110: zigbee2mqtt
- VMID 111: zigbee2mqtt-garasje (stopped)
- VMID 112: zwave-js-ui-hus
- VMID 113: zwave-js-ui-garasje (stopped)
- VMID 150: claude-agents
- VMID 200: win11-admin (VM)

**Estimat**: 10 minutter

---

### 5. InfluxDB IP-adresse
**Problem**: Ukjent hvor InfluxDB kjører
**Hvorfor viktig**: Trengs for Grafana og historiske data
**Løsning**: Sjekk Grafana datasources eller nmap subnet

**Estimat**: 5 minutter

---

## 🟢 NICE-TO-HAVE (kan vente)

### 6. Oppdatere React-HA dokumentasjon fullstendig
**Status**: Startet - OS-type og tilgangsmetode oppdatert
**Gjenstår**:
- Fjerne gamle/feil referanser til Ubuntu
- Oppdatere alle config-paths
- Dokumentere alle entities

---

### 7. Endre default-passord
**Problem**: Flere systemer bruker default credentials
**Berørte systemer**:
- ChirpStack (admin/admin)
- Grafana (admin/admin?)
- EMQX (admin/public?)
- Portainer (ukjent)

---

### 8. Secrets-rotasjon
**Problem**: Proxmox root-passord hardkodet flere steder
**Løsning**:
1. Generer nytt passord
2. Oppdater alle steder
3. Bruk KUN SSH-nøkler fremover

---

## 📋 NESTE STEG

**Anbefalt rekkefølge:**
1. ✅ ~~Oppdatere dokumentasjon (OS-type, tilgang)~~ DONE
2. ⬜ Generere HA API token (5 min)
3. ⬜ Kartlegge alle VMID-er (10 min)
4. ⬜ Finne InfluxDB IP (5 min)
5. ⬜ Sette opp SSH til HA (15-30 min)
6. ⬜ Planlegge backup-løsning (krever diskusjon med Ronny)

---

**Sist oppdatert**: 2025-12-04
