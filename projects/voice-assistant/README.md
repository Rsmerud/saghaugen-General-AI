# 🎙️ General AI Voice Assistant

**Prosjektnavn:** "Hei General"
**Status:** Planlegging
**Prioritet:** 🔥 HØYT (Ronny er HYPED!)
**Opprettet:** 2025-12-05

---

## Visjon

En taleassistent som faktisk FORSTÅR Saghaugen. Ikke en generisk Siri/Alexa som ikke vet forskjell på en sikringskurs og en yogakurs - men en assistent med full kontekst om huset, infrastrukturen, og familiens behov.

**Wake word:** "Hei General" 🎖️

---

## Hvorfor dette blir bedre enn alt annet

| Feature | Siri/Alexa/Google | General AI Voice |
|---------|-------------------|------------------|
| Kjenner huset | ❌ Generisk | ✅ Full CLAUDE.md |
| Sikringsskap-kunnskap | ❌ | ✅ 24 kurs, 3 ledige |
| Kan finne tilbud | ❌ | ✅ Pris-sjekker agent |
| Husker samtaler | ❌ | ✅ Persistent minne |
| Forstår norsk kontekst | Begrenset | ✅ Nerdete og direkte |
| Kan styre HA | Via skill/cloud | ✅ Direkte API |
| Privat | ❌ Alt til cloud | ✅ Kan være 100% lokal |
| Utfører handlinger | Begrenset | ✅ Full systemtilgang |

---

## Arkitektur

```
┌─────────────────────────────────────────────────────────────────────┐
│                         BRUKER-INTERAKSJON                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐    "Hei General"     ┌─────────────────────┐     │
│   │  Mikrofon   │ ──────────────────▶  │  Wake Word Engine   │     │
│   │  (Array)    │                      │  (OpenWakeWord/     │     │
│   └─────────────┘                      │   Porcupine)        │     │
│                                        └──────────┬──────────┘     │
│                                                   │ AKTIVERT       │
│                                                   ▼                │
│   ┌─────────────┐                      ┌─────────────────────┐     │
│   │  Høyttaler  │ ◀────────────────────│  Text-to-Speech     │     │
│   │             │                      │  (Piper - Norsk)    │     │
│   └─────────────┘                      └──────────▲──────────┘     │
│                                                   │                │
├───────────────────────────────────────────────────┼────────────────┤
│                         PROSESSERING              │                │
├───────────────────────────────────────────────────┼────────────────┤
│                                                   │                │
│   ┌─────────────────────┐              ┌─────────┴─────────┐       │
│   │  Speech-to-Text     │              │                   │       │
│   │  (Faster-Whisper)   │ ──────────▶  │   GENERAL AI      │       │
│   │                     │    tekst     │   VOICE AGENT     │       │
│   └─────────────────────┘              │                   │       │
│                                        │  - Full kontekst  │       │
│                                        │  - HA-tilgang     │       │
│                                        │  - Handlinger     │       │
│                                        │                   │       │
│                                        └─────────┬─────────┘       │
│                                                  │                 │
├──────────────────────────────────────────────────┼─────────────────┤
│                         INTEGRASJONER            │                 │
├──────────────────────────────────────────────────┼─────────────────┤
│                                                  │                 │
│   ┌──────────────┐  ┌──────────────┐  ┌─────────▼────────┐        │
│   │ HomeAssistant│  │   Proxmox    │  │  Claude API      │        │
│   │ REST API     │  │   API        │  │  (eller lokal    │        │
│   │              │  │              │  │   LLM fremtid)   │        │
│   └──────────────┘  └──────────────┘  └──────────────────┘        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Komponenter

### 1. Hardware

**Mikrofon-alternativer:**
| Enhet | Pris | Fordeler | Ulemper |
|-------|------|----------|---------|
| ReSpeaker 2-Mic HAT | ~200 kr | Enkel, RPi-kompatibel | 2 mics, begrenset |
| ReSpeaker 4-Mic Array | ~400 kr | God beamforming | Trenger mer prosessering |
| ReSpeaker USB 4-Mic | ~500 kr | USB, fleksibel | Ekstern strøm |
| Matrix Voice | ~600 kr | 8 mics, ESP32 | Kompleks oppsett |

**Anbefaling:** Start med **ReSpeaker 2-Mic HAT** på en RPi4.

**Høyttaler:**
- Hvilken som helst 3.5mm eller Bluetooth-høyttaler
- Eventuelt Sonos via HA (allerede på plass!)

### 2. Wake Word Engine

**Alternativer:**
| Engine | Lisens | Latency | Custom wake word |
|--------|--------|---------|------------------|
| OpenWakeWord | MIT (gratis) | ~100ms | ✅ Kan trenes |
| Porcupine | Freemium | ~50ms | ✅ (betalt for custom) |
| Snowboy | Apache 2.0 | ~100ms | ✅ Men discontinued |

**Anbefaling:** **OpenWakeWord** - gratis, open source, kan trene "Hei General".

### 3. Speech-to-Text (STT)

**Alternativer:**
| Engine | Kvalitet | Hastighet | Lokalt | Norsk |
|--------|----------|-----------|--------|-------|
| Whisper Large v3 | ⭐⭐⭐⭐⭐ | Treg | ✅ | ✅ |
| Faster-Whisper | ⭐⭐⭐⭐⭐ | 4x raskere | ✅ | ✅ |
| Whisper.cpp | ⭐⭐⭐⭐ | Rask | ✅ | ✅ |
| Vosk | ⭐⭐⭐ | Veldig rask | ✅ | ✅ |
| Google STT | ⭐⭐⭐⭐⭐ | Rask | ❌ | ✅ |

**Anbefaling:** **Faster-Whisper** med `medium` eller `large-v3` modell.

### 4. Text-to-Speech (TTS)

**Alternativer:**
| Engine | Kvalitet | Norsk | Lokalt | Naturlighet |
|--------|----------|-------|--------|-------------|
| Piper | ⭐⭐⭐⭐ | ✅ | ✅ | Bra |
| Coqui TTS | ⭐⭐⭐⭐ | ⚠️ | ✅ | Veldig bra |
| ElevenLabs | ⭐⭐⭐⭐⭐ | ✅ | ❌ | Fantastisk |
| Google TTS | ⭐⭐⭐⭐ | ✅ | ❌ | Bra |

**Anbefaling:** **Piper** med norsk stemme for lokal. ElevenLabs som premium-alternativ.

### 5. Hjerne - General AI Voice Agent

Dette blir en **dedikert sub-agent** under General AI:

```
General AI (CTO)
├── React-HA (dashboard/HA)
├── Pris-sjekker (tilbud)
└── Voice Agent (NY!) 🎙️
    ├── Mottar tekst fra STT
    ├── Full kontekst fra CLAUDE.md
    ├── Kan kalle HA API
    ├── Kan spawne sub-agenter
    └── Returnerer svar til TTS
```

---

## Eksempel-interaksjoner

### Smarthus-kontroll
```
👤: "Hei General, skru på lyset i gangen"
🎖️: "Gjort. Gang-lyset er nå på 50%."

👤: "Hei General, hva er temperaturen ute?"
🎖️: "Det er 3 grader ute nå, og det er ventet snø i kveld."

👤: "Hei General, sett huset i nattmodus"
🎖️: "Nattmodus aktivert. Jeg har dempet alle lys, låst dørene, og satt alarmen."
```

### Infrastruktur-spørsmål
```
👤: "Hei General, er det nok kapasitet i sikringsskapet til en induksjonstopp?"
🎖️: "Nei, Ronny. Induksjonstopp trenger typisk 32A 3-fas, og du har
     ingen ledig 3-fas kurs. Kurs 22, 23 og 24 er ledige, men de er
     enfas 16-20A. Du må oppgradere sikringsskapet."

👤: "Hei General, hvilke VM-er kjører på Proxmox?"
🎖️: "Det kjører 12 LXC-er og 2 VM-er. HomeAssistant, Frigate, og
     Node-RED er de viktigste. Skal jeg liste alle?"
```

### Handlinger
```
👤: "Hei General, finn priser på 48x198 konstruksjonstrevirke"
🎖️: "Jeg setter pris-sjekker agenten på saken. Jeg gir deg beskjed
     når jeg har funnet tilbud."

👤: "Hei General, restart HomeAssistant"
🎖️: "Er du sikker? Dette vil ta ned smarthuset i ca. 2 minutter."
👤: "Ja"
🎖️: "OK, restarter HomeAssistant nå."
```

### Samtale-kontekst
```
👤: "Hei General, hvor mange ledige kurser har vi?"
🎖️: "Dere har 3 ledige kurser: 22, 23 og 24."

👤: "Hva er kurs 23 reservert for?"
🎖️: "Kurs 23 er en 20A C-kurve, reservert for solceller og batteri."
```

---

## Implementasjonsplan

### Fase 1: Proof of Concept (MVP)
- [ ] Sette opp RPi4 med mikrofon
- [ ] Installere Faster-Whisper (STT)
- [ ] Installere Piper (TTS) med norsk stemme
- [ ] Enkel Python-script som kobler til Claude API
- [ ] Test med hardkodet kontekst

### Fase 2: Wake Word
- [ ] Trene "Hei General" wake word med OpenWakeWord
- [ ] Integrere wake word detection
- [ ] Kontinuerlig lytting med lav CPU-bruk

### Fase 3: Full integrasjon
- [ ] Opprette Voice Agent som sub-agent
- [ ] Gi full CLAUDE.md kontekst
- [ ] HA API-tilgang for handlinger
- [ ] Wyoming-protokoll integrasjon (valgfritt)

### Fase 4: Polish
- [ ] Feedback-lyder (pling når aktivert)
- [ ] LED-indikator på mikrofon
- [ ] Feilhåndtering og fallbacks
- [ ] Flere rom med mikrofoner?

---

## Hardware-handleliste

| Komponent | Modell | Ca. pris | Lenke |
|-----------|--------|----------|-------|
| Mikrofon HAT | ReSpeaker 2-Mic | ~200 kr | Kjell, Electrokit |
| RPi4 | 4GB (har du?) | ~600 kr | - |
| Høyttaler | 3.5mm eller Sonos | - | Eksisterende |
| microSD | 32GB+ | ~100 kr | - |

**Total:** ~300-900 kr avhengig av hva du har.

---

## Tekniske notater

### Wyoming-protokoll
Home Assistant bruker Wyoming-protokollen for voice assistants. Vi kan enten:
1. Implementere Wyoming-server (integreres med HA Voice)
2. Eller kjøre helt standalone (mer fleksibelt)

**Anbefaling:** Start standalone, vurder Wyoming senere.

### Claude API vs Lokal LLM
- **Claude API:** Beste kvalitet, krever internett, koster per token
- **Lokal LLM (Llama, Mistral):** Gratis, privat, men dårligere
- **Hybrid:** Lokal for enkle kommandoer, Claude for komplekse

**Anbefaling:** Start med Claude API, optimaliser senere.

### Latency-mål
| Steg | Mål | Typisk |
|------|-----|--------|
| Wake word → STT start | <100ms | ~50ms |
| STT (tale → tekst) | <2s | 1-3s |
| LLM (tenking) | <3s | 1-5s |
| TTS (tekst → tale) | <1s | 0.5-1s |
| **Total** | **<6s** | 3-8s |

---

## Sikkerhet

- [ ] Lokal prosessering av wake word (ingen cloud før aktivert)
- [ ] Valgfritt: Lokal STT også
- [ ] Bekreftelse før destruktive handlinger
- [ ] Logging av alle kommandoer
- [ ] Mulighet for å deaktivere ("Hei General, ta en pause")

---

## Fremtidige utvidelser

- 🔊 Flere mikrofoner i ulike rom
- 🎵 Integrert musikk-kontroll ("spill jazz i stua")
- 📱 Mobil-app med push-to-talk
- 🚗 Bil-integrasjon ("varm opp bilen")
- 👥 Stemmegjenkjenning (hvem snakker?)
- 🌍 Multi-språk (norsk + engelsk)

---

## Referanser

- [Wyoming Protocol](https://github.com/rhasspy/wyoming)
- [OpenWakeWord](https://github.com/dscripka/openWakeWord)
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
- [Piper TTS](https://github.com/rhasspy/piper)
- [Home Assistant Voice](https://www.home-assistant.io/voice_control/)

---

**Ansvarlig:** General AI + Voice Agent (ny)
**Første milestone:** Proof of Concept med enkel tale-input
**Drømmemål:** "Hei General, gjør huset klart til fest!" 🎉
