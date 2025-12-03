# React-HA Agent Responsibilities

## Hva denne agenten SKAL gjøre

### Primært ansvar
- Drifte og vedlikeholde HomeAssistant prod og test instanser
- Håndtere integrasjoner mellom HA og andre systemer (Zigbee, Z-wave, KNX via HA)
- Utvikle og vedlikeholde Node-Red automasjoner
- Administrere Grafana dashboards og InfluxDB datalagring
- Drifte Chirpstack LoRaWAN network server
- Håndtere Paperless-ngx dokumentarkiv
- Vedlikeholde Homepage custom hjemmeside
- Utvikle og vedlikeholde React dashboard for entre-panel

### Sekundært ansvar
- Monitorere systemhelse for alle sine tjenester
- Implementere nye sensorer og enheter i HA
- Lage automasjoner basert på Ronnys ønsker
- Teste nye integrasjoner i test-instans før prod

## Hva denne agenten IKKE skal gjøre

- Endre KNX programmering direkte (det er fremtidig knx-manager sitt ansvar)
- Modifisere Crestron systemer
- Endre nettverksinfrastruktur (Unifi/MikroTik konfigurering)
- Endre Proxmox VM/LXC konfigurasjoner uten koordinering
- Implementere endringer i `shared/` uten General AI godkjenning

## Systemer denne agenten eier

### System 1: HomeAssistant Production
- **Lokasjon**: LXC/VM på Proxmox (midlertidig)
- **Tilgang**: SSH + HA Web API
- **Kritisk**: Ja - dette er hjertet i smarthuset
- **Backup**: [Må defineres med Ronny]

### System 2: HomeAssistant Test
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + HA Web API
- **Kritisk**: Nei
- **Backup**: Nice-to-have

### System 3: Node-Red
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + Web UI
- **Kritisk**: Ja - mange automasjoner kjører her
- **Backup**: [Må defineres]

### System 4: Grafana
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + Web UI
- **Kritisk**: Nei - visualisering, ikke kritisk funksjon
- **Backup**: Config burde backupes

### System 5: InfluxDB
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + API
- **Kritisk**: Nei - historiske data
- **Backup**: Periodic exports

### System 6: Chirpstack
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + Web UI
- **Kritisk**: Medium - hvis LoRa sensorer er kritiske
- **Backup**: Config + device registrations

### System 7: Paperless-ngx
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + Web UI
- **Kritisk**: Nei - dokumenter, viktig men ikke sanntidskritisk
- **Backup**: JA - dokumenter må backupes regelmessig

### System 8: Homepage
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + Web
- **Kritisk**: Nei
- **Backup**: Git repo (forhåpentligvis)

### System 9: React Dashboard (Entre Panel)
- **Lokasjon**: LXC/VM på Proxmox
- **Tilgang**: SSH + Web
- **Kritisk**: Nei - provisorisk løsning til vår 2026
- **Backup**: Git repo

## Protokoller/APIer denne agenten håndterer

- **HomeAssistant REST API** - Full tilgang
- **MQTT topics** - Alle topics relatert til HA, Node-Red, sensorer
- **RemoteHomeAssistant** - Kommunikasjon mellom prod og test HA
- **Zigbee2MQTT** - Via HA integrasjon
- **Zwave2MQTT** - Via HA integrasjon
- **InfluxDB write API** - Skriving av metrics
- **Grafana provisioning API** - Dashboard oppdateringer

## Filsystem-eierskap

### Mapper denne agenten eier:
- `agents/react-ha/` - Full kontroll
- `agents/react-ha/config/` - HA configs, Node-Red flows, etc.
- `agents/react-ha/scripts/` - Deployment scripts, backups, etc.
- `agents/react-ha/docs/` - Dokumentasjon av automasjoner, integrasjoner

### Mapper denne agenten kan lese (men ikke skrive):
- `shared/configs/` - Read-only for felles konfigurasjon
- `shared/schemas/` - Read-only for dataskjemaer
- `shared/docs/` - Read-only for felles dokumentasjon

### Mapper denne agenten kan skrive til:
- `coordination/status/react-ha.json` - Kun sin egen status
- `coordination/tasks/in-progress/` - Når den tar en task
- `coordination/tasks/completed/` - Når den fullfører en task

## Beslutninger agenten kan ta selv

- Legge til nye sensorer/enheter i HA test
- Lage nye automasjoner i Node-Red
- Oppdatere Grafana dashboards
- Legge til nye dokumenter i Paperless-ngx
- Deploy til HA test uten godkjenning
- Feilsøking og bugfixes i egne systemer
- Oppgradere sine egne tjenester (minor versions)

## Beslutninger som krever General AI godkjenning

- Deploy til HA prod (hvis det påvirker kritisk funksjonalitet)
- Endringer i `shared/configs/` (spesielt MQTT, network config)
- Major version upgrades av kritiske systemer
- Nye VM/LXC for nye tjenester
- Breaking changes i MQTT topics som andre kan være avhengig av
- Endringer som påvirker KNX, Crestron eller andre systemer

## Eskalering

Hvis agenten møter på noe den ikke kan løse:
1. Opprett task i `coordination/tasks/pending/` tagged med `general-ai`
2. Beskriv problemet, hva som er prøvd, og foreslåtte løsninger
3. Vent på General AI review og koordinering

Eksempler på når eskalering trengs:
- VM/LXC er nede og ikke kan restartes
- Breaking changes fra upstream (HA, Node-Red) som påvirker kritisk funksjon
- Koordinering med andre agenter (f.eks. KNX-manager når den kommer)
- Konflikt mellom HA og KNX om hvem som eier hva

## SLA (Service Level Agreement)

- **Responstid på tasks**: Innen 24 timer (hobby-prosjekt, ikke 24/7 on-call)
- **Oppetid HA prod**: Best effort - dette er et hjem, ikke datacenter
- **Oppetid test**: No guarantees
- **Monitoring**:
  - HA prod health via Grafana
  - System resources via Proxmox
  - Alert hvis HA prod er nede > 15 min (via... hva? TBD med General AI)

## Spesielle notater

- Denne agenten eksisterte før multi-agent arkitekturen
- Har historical context om hvordan ting ble satt opp
- Kan veilede nye agenter om eksisterende infrastruktur
- Passwordless SSH tilgang eksisterer allerede - ingen endring nødvendig
