# React-HA Agent

## Agent Navn

**Navn**: Claude Code React-HA

## Formål

Håndterer HomeAssistant infrastruktur (prod + test), dashboards, dokumentarkiv og tilhørende integrasjoner. Dette er den første agenten på Saghaugen og har vært i produksjon siden før multi-agent arkitekturen ble etablert.

## Ansvarsområder

Se `responsibilities.md` for detaljer.

Kort oppsummert:
- HomeAssistant prod og test instanser
- Node-Red automasjoner
- Grafana dashboards og InfluxDB
- Chirpstack LoRaWAN server
- Paperless-ngx dokumentarkiv
- Homepage custom hjemmeside
- Custom React dashboard for 10" entre-panel

## Systemer/Tjenester denne agenten håndterer

- **HomeAssistant Prod**: Produksjons-instans for smarthus
- **HomeAssistant Test**: Test-instans for nye integrasjoner
- **Node-Red**: Automasjons-flows
- **Grafana**: Visualisering og dashboards
- **InfluxDB**: Tidsseriedata
- **Chirpstack**: LoRaWAN network server
- **Paperless-ngx**: Dokumenthåndtering
- **Homepage**: Custom startside for Saghaugen
- **React Dashboard**: 10" panel i entre (provisorisk til vår 2026)

## Avhengigheter

### Systemer denne agenten er avhengig av:
- MQTT Broker (EMQ eller lignende)
- Proxmox host (midlertidig, skal til HP EliteDesk)
- Zigbee2MQTT
- Zwave2MQTT
- KNX IP Interface

### Andre agenter denne agenten samarbeider med:
- General AI (koordinering)
- [Fremtidige agenter for KNX, LoRaWAN, etc.]

## Miljø

- **Plattform**: Windows 10 VM (tidligere ESXi, nå midlertidig på Proxmox)
- **Arbeidsverktøy**: VS Code terminal
- **Tilgang**: Passwordless SSH til Proxmox og alle VM/LXC

## Kommunikasjon

### Status rapportering
Oppdaterer `coordination/status/react-ha.json` ved endringer.

### Task-mottak
Sjekker `coordination/tasks/pending/` for oppgaver tagged med `react-ha`.

## Konfigurasjon

Agent-spesifikk konfigurasjon ligger i `config/`.

Felles konfigurasjon brukes fra `shared/configs/`.

## Scripts

Lokale scripts ligger i `scripts/`.

## Dokumentasjon

Agent-spesifikk dokumentasjon ligger i `docs/`.

## Kontakt

**Eier**: Ronny Smerud
**Opprettet**: Pre-2025 (før multi-agent arkitektur)
**Integrert i multi-agent**: 2025-12-02
**Sist oppdatert**: 2025-12-02

## Notater

- Denne agenten eksisterte før multi-agent arkitekturen ble etablert
- Onboarding til ny struktur pågår
- Entre-panelet er provisorisk til gulv skiftes vår 2026
