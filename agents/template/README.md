# Agent Template

Bruk denne malen når du lager en ny agent.

## Setup

1. Kopier hele `template/` mappen til `agents/<din-agent-navn>/`
2. Fyll ut alle seksjoner i denne README
3. Fyll ut `responsibilities.md`
4. Lag en PR til General AI for godkjenning

## Agent Navn

**Navn**: [Ditt agent-navn, f.eks. "KNX Manager", "LoRa Sentinel"]

## Formål

[1-2 setninger om hva denne agenten skal gjøre]

## Ansvarsområder

Se `responsibilities.md` for detaljer.

Kort oppsummert:
- [Ansvarsområde 1]
- [Ansvarsområde 2]
- [Ansvarsområde 3]

## Systemer/Tjenester denne agenten håndterer

- [System 1, f.eks. "HomeAssistant Prod"]
- [System 2, f.eks. "Chirpstack Server"]

## Avhengigheter

### Systemer denne agenten er avhengig av:
- [System 1, f.eks. "MQTT Broker"]
- [System 2, f.eks. "InfluxDB"]

### Andre agenter denne agenten samarbeider med:
- [Agent 1, f.eks. "react-ha"]

## Kommunikasjon

### Status rapportering
Denne agenten oppdaterer `coordination/status/<agent-navn>.json` hver [tidsinterval, f.eks "time", "dag", "ved endringer"].

### Task-mottak
Sjekker `coordination/tasks/pending/` for oppgaver tagged med `<agent-navn>`.

## Konfigurasjon

Agent-spesifikk konfigurasjon ligger i `config/`.

Felles konfigurasjon brukes fra `shared/configs/`.

## Scripts

Lokale scripts ligger i `scripts/`.

## Dokumentasjon

Agent-spesifikk dokumentasjon ligger i `docs/`.

## Kontakt

**Eier**: [Hvem som har satt opp denne agenten]
**Opprettet**: [Dato]
**Sist oppdatert**: [Dato]
