# Multi-Agent Arkitektur for Saghaugen

## Filosofi

General AI (CTO) koordinerer flere sub-agenter som hver har spesifikke ansvarsområder. Målet er:

1. **Autonomi**: Hver agent jobber i sitt eget domene uten å tråkke andre på tærne
2. **Transparens**: Alt er synlig for alle - ingen "black boxes"
3. **Koordinering**: General AI holder oversikten og fanger breaking changes
4. **Skalerbarhet**: Lett å legge til nye agenter når nye behov oppstår

## Filstruktur

```
GeneralAI/
├── CLAUDE.md                    # Onboarding for fremtidige Claude-instanser
├── ARCHITECTURE.md              # Dette dokumentet
├── README.md                    # Overordnet prosjektbeskrivelse
│
├── agents/                      # Hver agent har sin egen mappe
│   ├── react-ha/                # Eksisterende HomeAssistant agent
│   │   ├── README.md            # Hva denne agenten gjør
│   │   ├── responsibilities.md  # Konkrete ansvarsområder
│   │   ├── config/              # Agent-spesifikk konfigurasjon
│   │   ├── scripts/             # Agent-spesifikke scripts
│   │   └── docs/                # Agent-spesifikk dokumentasjon
│   │
│   ├── knx-manager/             # Fremtidig: KNX-spesifikk agent
│   │   └── README.md
│   │
│   ├── lora-sentinel/           # Fremtidig: LoRaWAN sensor management
│   │   └── README.md
│   │
│   └── template/                # Template for nye agenter
│       ├── README.md
│       ├── responsibilities.md
│       └── setup.md
│
├── coordination/                # General AI sitt domene
│   ├── status/                  # Status fra alle agenter
│   │   ├── react-ha.json        # Siste status fra react-ha
│   │   └── system-overview.json # Samlet oversikt
│   │
│   ├── tasks/                   # Oppgaver som skal distribueres
│   │   ├── pending/             # Ikke tildelt enda
│   │   ├── in-progress/         # Pågående
│   │   └── completed/           # Ferdig
│   │
│   └── logs/                    # Koordineringslogger
│       └── decisions.md         # Viktige beslutninger og hvorfor
│
├── shared/                      # Delt mellom alle agenter
│   ├── configs/                 # Felles konfigurasjoner
│   │   ├── mqtt.json            # MQTT broker info
│   │   ├── network.json         # Nettverksinformasjon
│   │   └── proxmox.json         # Proxmox connection info
│   │
│   ├── schemas/                 # Dataskjemaer for kommunikasjon
│   │   ├── agent-status.schema.json
│   │   └── task.schema.json
│   │
│   ├── scripts/                 # Felles verktøy
│   │   └── health-check.sh      # Sjekk status på alle systemer
│   │
│   └── docs/                    # Felles dokumentasjon
│       ├── protocols.md         # KNX, Modbus, etc. dokumentasjon
│       └── network-topology.md  # Nettverksoversikt
│
└── infrastructure/              # Infrastruktur-som-kode
    ├── proxmox/                 # Proxmox VM/LXC definisjoner
    ├── network/                 # Unifi/MikroTik konfigurasjon
    └── backup/                  # Backup-strategier og scripts
```

## Git-Strategi

### Branch-struktur

- `main` - Stabil, kjørende kode. Aldri commit direkte her.
- `dev` - Development branch. Merge hit når ting fungerer.
- `agent/<agent-name>/<feature>` - Feature branches per agent
  - Eksempel: `agent/react-ha/add-mqtt-sensor`
  - Eksempel: `agent/knx-manager/lighting-automation`

### Commit-konvensjon

```
<agent>: <type>: <beskrivelse>

Eksempler:
react-ha: feat: Legg til Zigbee2MQTT sensor
knx-manager: fix: Rett opp gruppeadresse for entre lys
general: docs: Oppdater arkitektur med ny agent
shared: config: Oppdater MQTT broker adresse
```

### Merge-prosess

1. Agent lager feature branch: `agent/<name>/<feature>`
2. Agent committer til sin branch
3. Agent ber General AI om review (via task system)
4. General AI sjekker for breaking changes
5. General AI merger til `dev` hvis OK
6. General AI merger til `main` når testet

### Konflikt-håndtering

- Hver agent eier sin mappe under `agents/`
- `shared/` og `coordination/` eies av General AI
- Hvis agent trenger å endre `shared/`, må det gå via General AI

## Kommunikasjonsprotokoll

### Agent Status Rapportering

Hver agent rapporterer status ved å oppdatere `coordination/status/<agent-name>.json`:

```json
{
  "agent": "react-ha",
  "timestamp": "2025-12-02T12:34:56Z",
  "status": "operational",
  "current_tasks": [
    "Monitoring HA prod instance",
    "Testing new Zigbee sensor integration"
  ],
  "issues": [],
  "dependencies": [
    "mqtt-broker",
    "homeassistant-prod",
    "homeassistant-test"
  ],
  "last_deployment": "2025-12-01T09:15:00Z"
}
```

### Task Assignment

General AI lager oppgaver i `coordination/tasks/pending/<task-id>.json`:

```json
{
  "task_id": "TASK-001",
  "title": "Legg til temperatur sensor i verksted",
  "assigned_to": "react-ha",
  "priority": "medium",
  "description": "Integrer Sensirion sensor i verksted med HA",
  "dependencies": ["lora-sentinel"],
  "created": "2025-12-02T10:00:00Z",
  "deadline": null,
  "status": "pending"
}
```

Agent flytter filen til `in-progress/` når den starter, `completed/` når ferdig.

### Inter-Agent Communication

Hvis en agent trenger noe fra en annen agent:

1. Lag en task i `coordination/tasks/pending/`
2. Tag den med relevant agent
3. General AI ser det og koordinerer
4. Unngå direkte agent-til-agent avhengigheter

## Dokumentasjonsstandard

### Hver agent MÅ ha:

1. **README.md** - Hva gjør denne agenten?
2. **responsibilities.md** - Konkrete ansvarsområder
   - Hvilke systemer eier den?
   - Hvilke protokoller/APIer håndterer den?
   - Hva skal den IKKE røre?
3. **CHANGELOG.md** - Hva har endret seg over tid?

### General AI ansvar:

- Holde `ARCHITECTURE.md` oppdatert
- Godkjenne nye agenter før de får commit-rettigheter
- Review alle endringer i `shared/` og `coordination/`
- Fange breaking changes før de deployes

## Onboarding nye agenter

1. Kopier `agents/template/` til `agents/<ny-agent>/`
2. Fyll ut README.md og responsibilities.md
3. Lag PR til General AI for godkjenning
4. General AI reviewer og merger
5. Ny agent kan starte arbeid i sin egen mappe

## Sikkerhet og Tilganger

### SSH/Proxmox tilganger

- **React-HA**: Har passwordless SSH til alle VM/LXC (eksisterende)
- **Nye agenter**: Får tilgang basert på behov (least privilege)
- **General AI**: Har oversikt, men ikke nødvendigvis direkte tilgang til alt

### Secrets Management

- Aldri commit secrets til Git
- Bruk environment variables eller Proxmox secrets store
- Dokumenter HVA som trengs, ikke selve secret-verdiene

## Skalerbarhet

Når flere agenter kommer:

- **5-10 agenter**: Denne strukturen fungerer fint
- **10+ agenter**: Vurder agent-grupper (f.eks. `agents/infrastructure/`, `agents/monitoring/`)
- **20+ agenter**: Trenger sannsynligvis automatisert orchestration (Ansible, etc.)

Per nå er vi på 1-2 agenter, så vi starter enkelt og utvider etter behov.

## Neste Steg

1. ✅ Dokumentere arkitekturen (dette dokumentet)
2. ⏳ Sette opp initial filstruktur
3. ⏳ Onboarde react-ha inn i denne strukturen
4. ⏳ Teste workflow med første task
5. ⏳ Iterere basert på hva som funker / ikke funker
