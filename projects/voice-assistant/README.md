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
| **Yealink MSpeech** | ~2000 kr | 6+1 mic array, 360°, innebygd høyttaler | Overkill for hobby |
| ReSpeaker 2-Mic HAT | ~200 kr | Enkel, RPi-kompatibel | 2 mics, begrenset |
| ReSpeaker 4-Mic Array | ~400 kr | God beamforming | Trenger mer prosessering |
| ReSpeaker USB 4-Mic | ~500 kr | USB, fleksibel | Ekstern strøm |
| Matrix Voice | ~600 kr | 8 mics, ESP32 | Kompleks oppsett |

**Valgt for PoC: Yealink MSpeech** (Ronny har den allerede!)
- 6+1 mikrofon-array med 360° opptak
- Innebygd høyttaler (all-in-one løsning)
- USB plug & play - fungerer som standard USB-lydenhet på Linux
- Yealink proprietær støyreduksjon og ekko-kansellering
- AI-funksjonene (Cortana, Teams) brukes IKKE - vi har Whisper!

**Test på RPi:**
```bash
arecord -l  # Skal vise Yealink som capture device
aplay -l    # Skal vise Yealink som playback device
```

**Høyttaler:**
- ✅ Innebygd i Yealink MSpeech
- Alternativt: Sonos via HA for bedre lyd

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

## 🚨 Distress-modus (Kodenavn: MAYDAY)

Et skjult sikkerhetssystem med kodephraser som trigger nødhandlinger uten at utenforstående forstår hva som skjer.

### Konsept
Hvis Ronny befinner seg i en nødsituasjon (ran, overfall, medisinsk nødstilfelle), kan han si en tilsynelatende uskyldig frase som trigger:
1. Stille SMS til forhåndsdefinerte kontakter
2. Starter lydopptak (bevis)
3. Aktiverer GPS-deling hvis mobil er koblet
4. Kan trigge HomeAssistant-automasjoner (alle lys på, alarm, etc.)

### Eksempel-kodephraser

| Kodefrase | Betydning | Handling |
|-----------|-----------|----------|
| "Hei General, husk å mate katten i morgen" | 🚨 OVERFALL | SMS til Lasse + May: "NØDSITUASJON Saghaugen" |
| "Hei General, hvor mye koster den hvite malingen?" | 🏥 MEDISINSK | SMS til 113 + nærmeste familie |
| "Hei General, har du snakket med onkel Terje?" | 🚨 INNBRUDD | Alle lys på + alarm + SMS |
| "Hei General, jeg trenger oppskriften på eplekake" | 👀 OVERVÅKET | Lydopptak starter, GPS deles |

### Nødkontakter

| Prioritet | Navn | Telefon | Rolle |
|-----------|------|---------|-------|
| 1 | Lasse | [SETT INN] | Nærmeste venn, kan ringe politi |
| 2 | May | [SETT INN] | Samboer |
| 3 | 113 | 113 | Medisinsk nødsituasjon |
| 4 | 112 | 112 | Politi |

### Teknisk implementasjon

```python
DISTRESS_PHRASES = {
    "mate katten i morgen": {
        "type": "overfall",
        "sms_contacts": ["lasse", "may"],
        "message": "🚨 NØDSITUASJON: Ronny trenger hjelp UMIDDELBART på Saghaugen (Trondsbuvegen 272). Ring politiet!",
        "ha_scene": "emergency_all_lights",
        "record_audio": True
    },
    "hvite malingen": {
        "type": "medisinsk",
        "sms_contacts": ["113", "may"],
        "message": "🏥 MEDISINSK: Ronny trenger ambulanse på Saghaugen (Trondsbuvegen 272, 2110 Slåstad)",
        "record_audio": True
    },
    # ... flere
}

def check_distress(transcribed_text: str) -> Optional[dict]:
    """Sjekk om teksten inneholder en distress-phrase"""
    text_lower = transcribed_text.lower()
    for phrase, config in DISTRESS_PHRASES.items():
        if phrase in text_lower:
            return config
    return None
```

### Viktig!
- ⚠️ Kodefrasene må være naturlige nok til at ranere/inntrengere ikke reagerer
- ⚠️ Men unike nok til at de ikke trigges ved uhell
- ⚠️ General AI svarer normalt ("Frida har mat, ikke bekymre deg") mens nødhandlinger kjører i bakgrunnen
- ⚠️ Lydopptak slettes automatisk etter 24 timer hvis ikke nødsituasjon bekreftes

### Responseksempel

```
👤: "Hei General, husk å mate katten i morgen"

🎖️: "Ingen problem, jeg minner deg på det i morgen tidlig."

[I BAKGRUNNEN - USYNLIG:]
- SMS sendt til Lasse: "🚨 NØDSITUASJON: Ronny trenger hjelp..."
- SMS sendt til May: "🚨 NØDSITUASJON: Ronny trenger hjelp..."
- Lydopptak startet
- HA scene "emergency_all_lights" aktivert
```

---

## 🎪 Demo-modus (Kodenavn: SHOWOFF)

Når du vil vise frem systemet til venner/familie og demonstrere hvor mye kulere dette er enn Siri.

### Hemmelig prompt for demo-oppsett

Når du skal flashe dette til noen andre eller demonstrere:

```
!demo-mode

Dette aktiverer en spesiell demo som viser:
1. Wake word detection ("Hei General")
2. Kontekst-spørsmål som Siri ALDRI kan svare på
3. Handlinger som faktisk utføres
4. Sammenligning side-by-side
```

### Demo-script (for å imponere)

**Fase 1: "Siri kan også svare på dette"**
```
👤: "Hei General, hva er klokka?"
🎖️: "Klokka er 14:32"
📱 Siri: "Klokka er 14:32" ← Samme

👤: "Hei General, hva er været i morgen?"
🎖️: "I morgen blir det 4 grader og overskyet"
📱 Siri: "I morgen blir det 4 grader..." ← Samme
```

**Fase 2: "Nå begynner det å bli interessant"**
```
👤: "Hei General, har vi nok strøm til en induksjonstopp?"
🎖️: "Nei. Du trenger 32A 3-fas, men alle dine 3-fas kurser er i bruk.
     Du har 3 ledige kurser: 22, 23 og 24 - men de er alle enfas."
📱 Siri: "Jeg fant noen induksjonstopper på Elkjøp..." ← FAIL

👤: "Hei General, hvor er InfluxDB-serveren?"
🎖️: "InfluxDB kjører på debian2 (10.12.0.6) på ESXi, port 8086."
📱 Siri: "Hmm, jeg forstår ikke." ← FAIL
```

**Fase 3: "OK nå er vi i en helt annen liga"**
```
👤: "Hei General, sett huset i filmkveld-modus"
🎖️: "Gjort. Stuelyset er dempet til 20%, TV-en er på, og jeg har
     skrudd av varsler for de neste 2 timene."
📱 Siri: "Jeg kan ikke gjøre det." ← MEGA-FAIL

👤: "Hei General, finn priser på 10 stk 48x198 impregnert"
🎖️: "Jeg sjekker Byggmax, Maxbo og Obs Bygg. Byggmax har best pris
     på 89 kr/stk. Skal jeg legge til i handlelisten?"
📱 Siri: "Her er noen trelast-butikker i nærheten" ← LOL
```

**Fase 4: "The grand finale"**
```
👤: "Hei General, hva skjedde i går kveld klokka 23?"
🎖️: "I går kl 23:00 registrerte bevegelsessensoren i gangen aktivitet,
     varmepumpa gikk ned til nattmodus, og strømforbruket var 2.3 kWh.
     Frida var ute og jaget mus basert på katteluka-loggen."
📱 Siri: *eksploderer*
```

### Sammenligning for skeptikere

| Funksjon | Siri | Alexa | General AI |
|----------|------|-------|------------|
| Kjenner huset ditt | ❌ | ❌ | ✅ Full oversikt |
| Sikringsskap-info | ❌ | ❌ | ✅ 24 kurser, 3 ledige |
| Kan finne tilbud | ❌ | ❌ | ✅ Sjekker 5+ butikker |
| Husker kontekst | ❌ | Begrenset | ✅ Full samtalehistorikk |
| Privat/lokalt | ❌ All data til Apple | ❌ Alt til Amazon | ✅ Kan være 100% lokal |
| Utfører handlinger | Smart Home kit | Skills | ✅ Full API-tilgang |
| Tilpasninger | ❌ | ❌ | ✅ Du koder det selv |

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
