# 🎖️ Hei General - Quickstart Guide

## Forutsetninger

- Raspberry Pi 4 med Raspberry Pi OS Lite (64-bit)
- USB konferansemikrofon (eller annen USB-mic)
- Internett-tilkobling
- Anthropic API-nøkkel

---

## Steg 1: Flash SD-kort

1. Last ned [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Velg: **Raspberry Pi OS Lite (64-bit)**
3. Klikk tannhjulet ⚙️ for avanserte innstillinger:
   - Hostname: `hei-general`
   - Enable SSH: ✅
   - Set username/password: `pi` / `ditt-passord`
   - Configure WiFi (hvis ikke ethernet)
4. Flash!

---

## Steg 2: Første oppstart

1. Sett inn SD-kort i RPi4
2. Koble til USB-mikrofon
3. Koble til strøm
4. Finn IP-adressen (sjekk router eller `ping hei-general.local`)

---

## Steg 3: SSH inn og kjør setup

```bash
# SSH til RPi
ssh pi@hei-general.local
# (eller ssh pi@<IP-adresse>)

# Last ned setup-filene
mkdir -p ~/hei-general/setup
cd ~/hei-general/setup

# Kopier filene fra GeneralAI-repoet, eller last ned direkte:
# (Ronny: Du kan scp-e filene fra LXC 150)
scp ronny@10.12.0.145:/home/ronny/ClaudeCodeProjects/GeneralAI/projects/voice-assistant/setup/* .

# Kjør del 1 (som root)
sudo bash 01-rpi-setup.sh

# Reboot
sudo reboot
```

---

## Steg 4: Installer voice software

```bash
ssh pi@hei-general.local
cd ~/hei-general/setup

# Kjør del 2
sudo bash 02-voice-software.sh
```

Dette tar 10-20 minutter på RPi4 (laster ned modeller).

---

## Steg 5: Sett opp API-nøkkel

```bash
cd ~/hei-general

# Opprett .env fil
cp setup/.env.example .env
nano .env

# Fyll inn:
# ANTHROPIC_API_KEY=sk-ant-din-nøkkel-her
```

Du får API-nøkkel fra: https://console.anthropic.com/

---

## Steg 6: Test lyd

```bash
cd ~/hei-general/setup
bash 03-test-audio.sh
```

Følg instruksjonene. Du skal:
1. Høre deg selv spilt av
2. Høre TTS-stemmen si "Hei! Jeg er General AI..."

---

## Steg 7: START! 🚀

```bash
cd ~/hei-general
source venv/bin/activate
python3 setup/hei_general.py
```

Trykk ENTER og snakk! 🎤

---

## Feilsøking

### "Ingen lyd"
```bash
# Sjekk lydenheter
arecord -l
aplay -l

# Velg riktig enhet i alsamixer
alsamixer
# Trykk F6 for å velge lydkort
```

### "Whisper er treg"
Prøv å bytte til mindre modell i `hei_general.py`:
```python
WHISPER_MODEL = "tiny"  # Raskere men dårligere
```

### "TTS høres rart ut"
Installer espeak som fallback:
```bash
sudo apt-get install espeak-ng
```

---

## Neste steg (etter PoC fungerer)

1. **Wake word**: Legg til "Hei General" aktivering
2. **HA-integrasjon**: Styre lys og enheter
3. **Kontinuerlig lytting**: Slipp å trykke ENTER
4. **Bedre stemme**: ElevenLabs eller trent Piper-stemme

---

## Kommandoer å teste

- "Hva er klokka?"
- "Hvor mange ledige sikringskurser har vi?"
- "Hva er IP-adressen til HomeAssistant?"
- "Fortell meg om Saghaugen"
- "Hva trenger jeg for å installere induksjonstopp?"

---

**Lykke til! 🎖️**
