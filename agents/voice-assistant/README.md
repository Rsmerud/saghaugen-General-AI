# Voice Assistant Agent

## Agent Navn

**Navn:** General AI Voice / "Hei General"

## Formål

Talebasert interaksjon med Saghaugen smarthus-systemer. Lar brukeren snakke naturlig med General AI for å styre huset, få informasjon, og utføre handlinger.

## Status

🚧 **Under planlegging** - Se `/projects/voice-assistant/README.md` for full dokumentasjon.

## Ansvarsområder

Se `responsibilities.md` for detaljer.

Kort oppsummert:
- Motta talekommandoer via wake word "Hei General"
- Konvertere tale til tekst (STT)
- Prosessere forespørsler med full Saghaugen-kontekst
- Utføre handlinger (HA-kontroll, informasjon, etc.)
- Konvertere svar til tale (TTS)

## Systemer/Tjenester denne agenten håndterer

- **Wake Word Engine:** OpenWakeWord (planlagt)
- **Speech-to-Text:** Faster-Whisper (planlagt)
- **Text-to-Speech:** Piper med norsk stemme (planlagt)
- **LLM:** Claude API med full kontekst

## Avhengigheter

### Systemer denne agenten er avhengig av:
- Claude API (eller fremtidig lokal LLM)
- HomeAssistant REST API (for handlinger)
- General AI sin kontekst (CLAUDE.md, infrastruktur-docs)

### Andre agenter denne agenten samarbeider med:
- **General AI** (parent - gir kontekst og koordinerer)
- **React-HA** (HA-ekspertise ved behov)
- **Pris-sjekker** (kan spawnes for prisforespørsler)

## Hardware-krav

- Raspberry Pi 4 (eller lignende)
- Mikrofon-array (ReSpeaker 2-Mic HAT anbefalt)
- Høyttaler (eksisterende eller 3.5mm)

## Miljø

- **Plattform:** Raspberry Pi 4 (planlagt)
- **OS:** Raspberry Pi OS Lite
- **Lokasjon:** TBD (stue? kjøkken?)

## Kommunikasjon

### Input
- Wake word detection → STT → tekst

### Output
- Tekst → TTS → høyttaler

### Status rapportering
Vil oppdatere `coordination/status/voice-assistant.json` ved endringer.

## Konfigurasjon

Agent-spesifikk konfigurasjon vil ligge i `config/`.

## Neste steg

1. [ ] Bestille hardware (ReSpeaker 2-Mic HAT)
2. [ ] Sette opp RPi4 med OS
3. [ ] Proof of Concept med Whisper + Piper
4. [ ] Trene "Hei General" wake word

---

**Eier:** Ronny Smerud
**Opprettet:** 2025-12-05
**Status:** Planlegging
