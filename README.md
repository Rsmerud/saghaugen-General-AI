# General AI - Saghaugen CTO Agent

Multi-agent koordineringssystem for smarthus-infrastrukturen på Saghaugen.

## Hva er dette?

General AI (ordspill på "general"/"generell") er CTO-agenten som koordinerer et dynamisk antall sub-agenter. Hver sub-agent har spesifikke ansvarsområder (HomeAssistant, KNX, LoRaWAN, etc.), mens General AI holder oversikten og sørger for at alt henger sammen teknisk.

## Arkitektur

Se [ARCHITECTURE.md](ARCHITECTURE.md) for full dokumentasjon av arkitekturen.

**Kort oppsummert:**
- **General AI**: Koordinerer alle sub-agenter, holder oversikt, fanger breaking changes
- **Sub-agenter**: Hver agent har sitt eget domene (f.eks. react-ha for HomeAssistant)
- **Kommunikasjon**: Via `coordination/` directory (status reports, tasks, logs)
- **Git**: Strukturert workflow med agent-spesifikke branches

## Prosjektstruktur

```
GeneralAI/
├── agents/              # Hver sub-agent har sin egen mappe
├── coordination/        # Status, tasks, logs for koordinering
├── shared/             # Felles konfigurasjon, schemas, dokumentasjon
├── infrastructure/     # Proxmox, nettverk, backup konfigurasjon
├── CLAUDE.md          # Onboarding for fremtidige Claude-instanser
├── ARCHITECTURE.md    # Detaljert arkitektur-dokumentasjon
└── README.md          # Dette dokumentet
```

## Aktive Agenter

### react-ha
- **Status**: Operativ
- **Ansvar**: HomeAssistant (prod + test), Node-Red, Grafana, Chirpstack, Paperless-ngx, dashboards
- **Dokumentasjon**: [agents/react-ha/README.md](agents/react-ha/README.md)

### [Fremtidige agenter kommer her]

## Kom i gang

### For nye agenter

1. Les [ARCHITECTURE.md](ARCHITECTURE.md)
2. Kopier `agents/template/` til `agents/<ditt-navn>/`
3. Fyll ut README.md og responsibilities.md
4. Lag PR til General AI for godkjenning
5. Start arbeid i din egen mappe

### For Ronny

- **Onboarding av Claude**: Se [CLAUDE.md](CLAUDE.md)
- **Arkitektur**: Se [ARCHITECTURE.md](ARCHITECTURE.md)
- **Legg til ny agent**: Bruk `agents/template/` som utgangspunkt

## Teknisk Stack

**Smarthus:**
- HomeAssistant (HA)
- KNX
- Crestron + Crestron Home
- Zigbee (via Zigbee2MQTT)
- Z-wave (via Zwave2MQTT)
- LoRaWAN (Chirpstack + custom gateway)
- Modbus
- Sensirion-baserte sensorer (custom)

**Infrastruktur:**
- Proxmox (virtualisering)
- Node-Red (automasjoner)
- Grafana + InfluxDB (monitoring)
- MQTT (EMQ eller lignende)
- Unifi + MikroTik (nettverk)
- Starlink (ISP, fiber kommer)

## Lokasjon

Saghaugen, Trondsbuvegen 272, 2110 SLÅSTAD, Norge

## Eier

Ronny Smerud

## Lisens

Privat prosjekt - ingen lisens.
