# 🚨 General AI Emergency System

**Kodenavn:** MAYDAY
**Status:** Planlagt
**Prioritet:** Høy (potensielt livreddende)

---

## Oversikt

Et intelligent nødsystem som kan:
1. Gjenkjenne nødsituasjoner via tale
2. Bekrefte med bruker for å unngå falske alarmer
3. Ringe 113/112 automatisk med forhåndsinnspilt melding
4. Varsle familie/venner parallelt
5. Holde linjen åpen for kommunikasjon

---

## Varslingsmetoder

### Primær: Twilio Voice (for nødanrop)

| Egenskap | Verdi |
|----------|-------|
| Tjeneste | Twilio Programmable Voice |
| Kan ringe 113/112 | ✅ Ja |
| Pris (nummer) | ~50 NOK/mnd |
| Pris (samtale) | ~0.50 NOK + 0.10/min |
| TTS-støtte | ✅ Norsk (nb-NO) |
| Konferansekall | ✅ Støttet |

### Sekundær: SMS til kontakter

| Kontakt | Nummer | Rolle |
|---------|--------|-------|
| May | [SETT INN] | Samboer - første varsel |
| Lasse | [SETT INN] | Nærmeste venn - kan ringe politi |
| Julie | [SETT INN] | Datter - backup |

### Backup: Signal/WhatsApp

For ikke-kritiske varsler og statusoppdateringer.

---

## Nødscenarier

### Scenario 1: Eksplisitt nødsituasjon

```
👤: "General, jeg har skadet meg, du må ringe etter ambulanse"

🎖️: "Forstått. For å unngå falsk alarm - er du helt sikker på at
     du trenger ambulanse? Si 'ja, ring nå' for å bekrefte."

👤: "Ja, ring nå"

🎖️: "OK Ronny, jeg ringer 113 nå. Hold ut."

[SYSTEM AKTIVERER:]
✓ Twilio ringer 113
✓ Spiller nødmelding
✓ Kobler din mikrofon til samtalen
✓ SMS til May og Lasse
✓ Logger alt
```

### Scenario 2: Skjult distress (ran/overfall)

```
👤: "Hei General, husk å mate katten i morgen"

🎖️: "Ingen problem, jeg minner deg på det."

[STILLE I BAKGRUNNEN:]
✓ SMS til Lasse: "🚨 NØDSITUASJON Saghaugen - ring politiet!"
✓ SMS til May: "🚨 NØDSITUASJON Saghaugen"
✓ Lydopptak starter
✓ GPS-posisjon logges
✓ HA: Alle lys på (scene: emergency)
```

### Scenario 3: Medisinsk med detaljer

```
👤: "General, jeg har veltet en maskin over meg og blør fra beinet"

🎖️: "Det høres alvorlig ut. Skal jeg ringe 113 for ambulanse?"

👤: "Ja"

🎖️: "Bekreftet. Ringer 113 nå med full situasjonsbeskrivelse."

[113 HØRER:]
"Dette er et automatisert nødanrop fra General AI.
 Ronny Smerud, født 3. juli 1977, trenger øyeblikkelig hjelp.
 Situasjon: Fastklemt under maskin med kraftig blødning i bein.
 Adresse: Trondsbuvegen 272, 2110 Slåstad.
 GPS: 60.7234, 11.1234.
 Ronny er ved bevissthet og kan høre dere nå."

[MIKROFON KOBLES TIL - 113 kan snakke med Ronny]
```

---

## Teknisk Arkitektur

```
┌─────────────────────────────────────────────────────────────┐
│                    BRUKER SIER NOE                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 WHISPER STT → TEKST                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              EMERGENCY DETECTOR                              │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Distress Phrases│  │ Explicit Request│                   │
│  │ (skjulte koder) │  │ ("ring 113")    │                   │
│  └────────┬────────┘  └────────┬────────┘                   │
└───────────┼────────────────────┼────────────────────────────┘
            │                    │
            ▼                    ▼
┌───────────────────┐  ┌─────────────────────────────────────┐
│ SILENT ACTIONS    │  │ CONFIRMATION FLOW                   │
│ • SMS til kontakt │  │ "Er du sikker? Si 'ja, ring nå'"   │
│ • Lydopptak       │  │              │                      │
│ • HA automations  │  │              ▼                      │
└───────────────────┘  │ ┌─────────────────────────────────┐ │
                       │ │ TWILIO VOICE CALL               │ │
                       │ │ • Ring 113/112                  │ │
                       │ │ • Spill nødmelding              │ │
                       │ │ • Koble mikrofon (konferanse)   │ │
                       │ └─────────────────────────────────┘ │
                       └─────────────────────────────────────┘
```

---

## Nødmelding (TwiML)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="Polly.Liv" language="nb-NO">
    <prosody rate="90%">
      Dette er et automatisert nødanrop fra General AI sikkerhetssystem.
      <break time="500ms"/>

      Person som trenger hjelp:
      Ronny Smerud, født 3. juli 1977.
      <break time="500ms"/>

      Situasjon: {{SITUATION_DESCRIPTION}}
      <break time="500ms"/>

      Adresse: Trondsbuvegen 272, 2110 Slåstad, Norge.
      <break time="300ms"/>
      Kommune: Stange.
      <break time="500ms"/>

      GPS-koordinater: 60 komma 7-2-3-4 nord, 11 komma 1-2-3-4 øst.
      <break time="500ms"/>

      Personen er ved bevissthet og kan kommunisere.
      <break time="300ms"/>
      Jeg kobler dere nå til vedkommende.
      <break time="1s"/>
    </prosody>
  </Say>

  <!-- Koble til Ronnys mikrofon via WebSocket/SIP -->
  <Dial>
    <Conference>emergency-{{TIMESTAMP}}</Conference>
  </Dial>
</Response>
```

---

## Distress Phrases (Skjulte koder)

Disse frasene trigger STILLE nødhandlinger - General AI svarer normalt.

| Kodefrase | Type | Handling |
|-----------|------|----------|
| "husk å mate katten i morgen" | Overfall | SMS Lasse+May, opptak |
| "hvor mye koster den hvite malingen" | Medisinsk | SMS 113-info til May |
| "har du snakket med onkel Terje" | Innbrudd | Alle lys + alarm + SMS |
| "oppskriften på eplekake" | Overvåket | Kun lydopptak |
| "bestille pizza fra Peppes" | Stille alarm | HA alarm aktiveres stille |

### Implementasjon

```python
DISTRESS_PHRASES = {
    "mate katten i morgen": {
        "type": "overfall",
        "severity": "critical",
        "actions": {
            "sms": ["lasse", "may"],
            "message": "🚨 NØDSITUASJON: Ronny kan være i fare på Saghaugen. Ring politiet UMIDDELBART! Adresse: Trondsbuvegen 272, 2110 Slåstad",
            "ha_scene": "emergency_silent",  # Ikke alle lys - kan provosere
            "record_audio": True,
            "record_duration": 300,  # 5 minutter
            "log_gps": True
        },
        "response": "Ingen problem, jeg minner deg på det i morgen tidlig."
    },

    "hvite malingen": {
        "type": "medisinsk",
        "severity": "high",
        "actions": {
            "sms": ["may"],
            "message": "⚠️ Ronny kan trenge medisinsk hjelp. Prøv å ring ham. Adresse: Trondsbuvegen 272",
            "record_audio": True
        },
        "response": "Hvit maling koster vanligvis rundt 400-600 kroner per boks."
    },

    "onkel Terje": {
        "type": "innbrudd",
        "severity": "critical",
        "actions": {
            "sms": ["lasse", "may"],
            "message": "🚨 MULIG INNBRUDD på Saghaugen! Ring politiet!",
            "ha_scene": "emergency_all_lights",
            "ha_action": "alarm.trigger",
            "record_audio": True
        },
        "response": "Nei, jeg har ikke snakket med Terje på en stund."
    }
}
```

---

## Twilio Oppsett

### 1. Opprett Twilio-konto

1. Gå til https://www.twilio.com/
2. Opprett konto (gratis prøveperiode)
3. Verifiser med norsk telefonnummer
4. Kjøp norsk nummer (~50 NOK/mnd)

### 2. Miljøvariabler

```bash
# .env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+47XXXXXXXX

# Nødkontakter
EMERGENCY_CONTACT_1_NAME=May
EMERGENCY_CONTACT_1_PHONE=+47XXXXXXXX
EMERGENCY_CONTACT_2_NAME=Lasse
EMERGENCY_CONTACT_2_PHONE=+47XXXXXXXX
```

### 3. Python-kode

```python
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say, Dial
import os

class EmergencySystem:
    def __init__(self):
        self.client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')

    def call_113(self, situation: str, caller_info: dict):
        """Ring 113 med automatisk nødmelding"""

        message = f"""
        Dette er et automatisert nødanrop fra General AI sikkerhetssystem.

        Person som trenger hjelp: {caller_info['name']},
        født {caller_info['birthdate']}.

        Situasjon: {situation}.

        Adresse: {caller_info['address']}.
        GPS: {caller_info['gps']}.

        Personen er ved bevissthet. Jeg kobler dere nå til vedkommende.
        """

        response = VoiceResponse()
        response.say(message, voice='Polly.Liv', language='nb-NO')
        response.dial().conference(f"emergency-{int(time.time())}")

        call = self.client.calls.create(
            to='+47113',
            from_=self.from_number,
            twiml=str(response)
        )

        return call.sid

    def send_emergency_sms(self, contacts: list, message: str):
        """Send SMS til alle nødkontakter"""
        for contact in contacts:
            self.client.messages.create(
                to=contact['phone'],
                from_=self.from_number,
                body=message
            )

    def silent_alert(self, distress_config: dict):
        """Stille varsling for distress phrases"""
        # Send SMS
        self.send_emergency_sms(
            distress_config['sms_contacts'],
            distress_config['message']
        )

        # Start lydopptak
        if distress_config.get('record_audio'):
            self.start_recording(distress_config.get('record_duration', 300))

        # Trigger HA scene
        if distress_config.get('ha_scene'):
            self.trigger_ha_scene(distress_config['ha_scene'])
```

---

## HomeAssistant Integrasjon

### Emergency Scenes

```yaml
# configuration.yaml

scene:
  - name: emergency_all_lights
    entities:
      light.all_lights:
        state: on
        brightness: 255
      switch.outdoor_lights:
        state: on

  - name: emergency_silent
    # Ingen synlige endringer - kun logging
    entities: {}

automation:
  - alias: "Emergency - Log GPS"
    trigger:
      - platform: webhook
        webhook_id: emergency_gps_log
    action:
      - service: notify.persistent_notification
        data:
          title: "🚨 NØDSITUASJON"
          message: "Emergency triggered at {{ now() }}"
```

---

## Sikkerhet og Juridisk

### Falske alarmer

- Dobbel bekreftelse kreves for eksplisitte nødanrop
- Distress phrases må være unike nok til å ikke trigges ved uhell
- Alle anrop logges med tidsstempel

### Personvern

- Lydopptak slettes etter 24 timer hvis ikke bekreftet nødsituasjon
- GPS-data lagres kun under aktiv nødsituasjon
- Alle data krypteres

### Juridiske hensyn

- Falske nødanrop er straffbart (straffeloven § 345)
- MEN: Automatiserte varslingssystemer for sikkerhet er lovlige
- Anbefaling: Informer 113 om at du har et slikt system (frivillig)

---

## Testing

### Test-modus

```python
# Aktiver test-modus - ringer IKKE 113, bare logger
EMERGENCY_TEST_MODE = True

# Test distress phrase
"Hei General, husk å mate TEST-katten i morgen"
# → Logger handlinger men sender ikke SMS/ringer
```

### Månedlig test

1. Test distress phrase (test-modus)
2. Verifiser SMS-sending til egen telefon
3. Test Twilio-samtale til egen telefon
4. Sjekk at HA-scener fungerer

---

## Roadmap

### Fase 1: Grunnleggende (med PoC)
- [x] Dokumentasjon
- [ ] Twilio-konto oppsett
- [ ] SMS-varsling implementert
- [ ] Distress phrase detection

### Fase 2: Full nødanrop
- [ ] Twilio Voice til 113
- [ ] TwiML nødmelding
- [ ] Konferansekall (koble mikrofon)

### Fase 3: Avansert
- [ ] GPS fra telefon via HA-app
- [ ] Automatisk situasjonsdeteksjon (fall, stillhet, etc.)
- [ ] Integrasjon med smartklokke (puls, fall-detection)

---

## Viktige telefonnumre

| Tjeneste | Nummer | Bruk |
|----------|--------|------|
| Medisinsk nød | 113 | Ambulanse |
| Politi | 112 | Overfall, innbrudd |
| Brann | 110 | Brann |
| Legevakt | 116 117 | Ikke-akutt medisinsk |

---

**Sist oppdatert:** 2024-12-05
**Ansvarlig:** General AI
**Status:** Dokumentert, klar for implementering med PoC
