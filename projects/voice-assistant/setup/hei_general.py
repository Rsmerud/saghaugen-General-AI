#!/usr/bin/env python3
"""
🎖️ HEI GENERAL - Voice Assistant PoC
=====================================

En taleassistent for Saghaugen som:
1. Lytter på tale via mikrofon
2. Konverterer tale til tekst (Whisper)
3. Sjekker for nødsituasjoner (MAYDAY-system)
4. Sender til Claude med full Saghaugen-kontekst
5. Konverterer svar til tale (Piper)
6. Spiller av svaret

Bruk: python3 hei_general.py
"""

import os
import sys
import wave
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from anthropic import Anthropic
from dotenv import load_dotenv

# Emergency system
from emergency import EmergencySystem, is_emergency_request, is_confirmation

# Last miljøvariabler
load_dotenv()

# ============================================================================
# KONFIGURASJON
# ============================================================================

# Audio settings
SAMPLE_RATE = 16000  # Whisper forventer 16kHz
CHANNELS = 1
DTYPE = np.int16

# Whisper modell (bruk "tiny" eller "base" for raskere, "small"/"medium" for bedre)
WHISPER_MODEL = "base"  # Balanse mellom hastighet og kvalitet på RPi4

# Piper TTS
PIPER_MODEL = Path("/home/pi/hei-general/models/piper/norwegian.onnx")

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Silence detection
SILENCE_THRESHOLD = 500  # Juster basert på mikrofon
SILENCE_DURATION = 1.5   # Sekunder stillhet før vi stopper opptak
MAX_RECORDING_DURATION = 30  # Maks sekunder opptak

# ============================================================================
# SAGHAUGEN KONTEKST
# ============================================================================

SAGHAUGEN_CONTEXT = """
Du er General AI, den personlige assistenten for Saghaugen - Ronny Smeruds smarthus.

## Om Saghaugen
- Adresse: Trondsbuvegen 272, 2110 SLÅSTAD, Norge
- Tømmerhus fra 1943, ~70-80 kvm
- Låve/verksted: 130 kvm (30 kvm isolert)
- Beboere: Ronny, May, og katten Frida

## Teknisk infrastruktur
- HomeAssistant på 10.12.0.20:8123
- Proxmox med 12+ LXC/VM-er
- Unifi nettverk med UDM-Pro på 10.12.0.1
- KNX for kritiske funksjoner (lys, gulvvarme)
- Zigbee2MQTT og Z-Wave for sensorer/brytere

## Sikringsskap
- 24 kurser totalt
- 3 ledige: Kurs 22 (16A), Kurs 23 (20A solceller), Kurs 24 (16A)
- Induksjonstopp krever 32A 3-fas (IKKE ledig!)

## Dine evner
- Du kan svare på spørsmål om huset og infrastrukturen
- Du har IKKE direkte tilgang til å styre enheter i denne PoC-versjonen
- Vær vennlig, direkte, og litt nerdete (Ronny liker det)
- Svar på norsk med mindre bruker snakker engelsk

## Viktig
- Hold svarene korte og konsise (skal leses opp!)
- Maksimalt 2-3 setninger for enkle spørsmål
- Bekreft handlinger kort: "Gjort", "Forstått", etc.
"""

# ============================================================================
# KLASSER OG FUNKSJONER
# ============================================================================

class HeiGeneral:
    def __init__(self):
        print("🎖️  Starter Hei General...")

        # Sjekk API-nøkkel
        if not ANTHROPIC_API_KEY:
            print("❌ ANTHROPIC_API_KEY ikke satt!")
            print("   Opprett .env fil med: ANTHROPIC_API_KEY=din_nøkkel")
            sys.exit(1)

        # Initialiser Whisper
        print("🎤 Laster Whisper modell...")
        self.whisper = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")

        # Initialiser Claude
        print("🧠 Kobler til Claude...")
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

        # Initialiser Emergency System
        print("🚨 Aktiverer MAYDAY-system...")
        self.emergency = EmergencySystem()

        # Samtalehistorikk
        self.conversation_history = []

        # Emergency state
        self.awaiting_emergency_confirmation = False
        self.pending_emergency_situation = None

        print("✅ Klar!")
        print("")

    def record_audio(self):
        """Ta opp lyd fra mikrofon til bruker slutter å snakke"""
        print("🎤 Lytter... (snakk nå)")

        frames = []
        silence_frames = 0
        silence_threshold_frames = int(SILENCE_DURATION * SAMPLE_RATE / 1024)
        max_frames = int(MAX_RECORDING_DURATION * SAMPLE_RATE / 1024)

        def callback(indata, frame_count, time_info, status):
            nonlocal silence_frames
            frames.append(indata.copy())

            # Sjekk for stillhet
            volume = np.abs(indata).mean()
            if volume < SILENCE_THRESHOLD:
                silence_frames += 1
            else:
                silence_frames = 0

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS,
                           dtype=DTYPE, callback=callback, blocksize=1024):
            while silence_frames < silence_threshold_frames and len(frames) < max_frames:
                sd.sleep(100)

        print("   ✅ Opptak ferdig")

        # Konverter til numpy array
        audio_data = np.concatenate(frames, axis=0)
        return audio_data

    def save_audio(self, audio_data, filename):
        """Lagre audio til WAV-fil"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data.tobytes())

    def transcribe(self, audio_data):
        """Konverter tale til tekst med Whisper"""
        print("📝 Transkriberer...")

        # Lagre til temp-fil
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            self.save_audio(audio_data, f.name)
            temp_path = f.name

        try:
            # Kjør Whisper
            segments, info = self.whisper.transcribe(temp_path, language="no")
            text = " ".join([segment.text for segment in segments]).strip()
            print(f"   Du sa: \"{text}\"")
            return text
        finally:
            os.unlink(temp_path)

    def ask_claude(self, user_message):
        """Send melding til Claude og få svar"""
        print("🧠 Tenker...")

        # Legg til i historikk
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Send til Claude
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,  # Korte svar for tale
            system=SAGHAUGEN_CONTEXT,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text

        # Legg til svar i historikk
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Behold bare siste 10 meldinger for kontekst
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        print(f"   General AI: \"{assistant_message}\"")
        return assistant_message

    def speak(self, text):
        """Konverter tekst til tale og spill av"""
        print("🔊 Snakker...")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name

        try:
            if PIPER_MODEL.exists():
                # Bruk Piper
                process = subprocess.run(
                    ["piper", "--model", str(PIPER_MODEL), "--output_file", temp_path],
                    input=text.encode(),
                    capture_output=True
                )
                subprocess.run(["aplay", temp_path], capture_output=True)
            else:
                # Fallback til espeak
                subprocess.run(
                    ["espeak-ng", "-v", "no", text, "--stdout"],
                    stdout=subprocess.PIPE
                )
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def run(self):
        """Hovedløkke"""
        print("")
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║     🎖️  HEI GENERAL er klar!                                  ║")
        print("║                                                               ║")
        print("║  Trykk ENTER for å snakke, eller skriv 'quit' for å avslutte  ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print("")

        # Si hei
        self.speak("Hei! Jeg er General AI, klar til å hjelpe deg med Saghaugen.")

        while True:
            try:
                user_input = input("\n[ENTER for å snakke, 'quit' for å avslutte] > ")

                if user_input.lower() == 'quit':
                    self.speak("Ha det bra!")
                    break

                # Ta opp lyd
                audio = self.record_audio()

                # Sjekk at vi fikk noe lyd
                if len(audio) < SAMPLE_RATE:  # Mindre enn 1 sekund
                    print("   ⚠️ For kort opptak, prøv igjen")
                    continue

                # Transkriber
                text = self.transcribe(audio)

                if not text or len(text) < 2:
                    print("   ⚠️ Kunne ikke forstå, prøv igjen")
                    continue

                # ============================================================
                # EMERGENCY CHECK - Sjekk for nødsituasjoner FØR Claude
                # ============================================================

                # Sjekk om vi venter på bekreftelse for nødanrop
                if self.awaiting_emergency_confirmation:
                    if is_confirmation(text):
                        response = self.emergency.confirm_and_call_113(
                            self.pending_emergency_situation
                        )
                        self.awaiting_emergency_confirmation = False
                        self.pending_emergency_situation = None
                    else:
                        response = "OK, avbryter nødanrop. Si beskjed hvis du trenger hjelp."
                        self.awaiting_emergency_confirmation = False
                        self.pending_emergency_situation = None
                    self.speak(response)
                    continue

                # Sjekk for distress phrases (skjulte koder)
                distress = self.emergency.check_distress_phrase(text)
                if distress:
                    # Håndter distress STILLE - returner fake response
                    response = self.emergency.handle_distress(distress)
                    self.speak(response)
                    continue

                # Sjekk for eksplisitt nødanrop
                if is_emergency_request(text):
                    self.pending_emergency_situation = text
                    self.awaiting_emergency_confirmation = True
                    response = self.emergency.request_emergency_call(text)
                    self.speak(response)
                    continue

                # ============================================================
                # NORMAL FLOW - Spør Claude
                # ============================================================

                response = self.ask_claude(text)

                # Si svaret
                self.speak(response)

            except KeyboardInterrupt:
                print("\n\n👋 Avslutter...")
                break
            except Exception as e:
                print(f"❌ Feil: {e}")
                continue


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    assistant = HeiGeneral()
    assistant.run()
