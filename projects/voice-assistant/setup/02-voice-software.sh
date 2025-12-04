#!/bin/bash
#===============================================================================
# HEI GENERAL - Voice Assistant PoC Setup Script
# Del 2: Voice software (Whisper, Piper, Python deps)
#
# Kjør ETTER del 1 og reboot
#===============================================================================

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🎖️  HEI GENERAL - Voice Assistant Setup (Del 2)  🎖️      ║"
echo "║                   Voice Software                              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="/home/pi/hei-general"
cd $PROJECT_DIR

# Opprett Python virtual environment
echo "🐍 Oppretter Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Oppgrader pip
pip install --upgrade pip wheel setuptools

# Installer Python-pakker
echo ""
echo "📦 Installerer Python-pakker (dette tar litt tid på RPi4)..."

# Audio
pip install pyaudio sounddevice numpy

# Whisper (faster-whisper for bedre ytelse)
echo "🎤 Installerer Faster-Whisper (STT)..."
pip install faster-whisper

# Piper TTS
echo "🔊 Installerer Piper TTS..."
pip install piper-tts

# Claude/Anthropic API
echo "🧠 Installerer Anthropic SDK..."
pip install anthropic

# Ekstra nyttige pakker
pip install python-dotenv requests

echo ""
echo "📥 Laster ned Piper norsk stemme..."
mkdir -p $PROJECT_DIR/models/piper
cd $PROJECT_DIR/models/piper

# Last ned norsk stemme (talesyntansen)
# Bruker "no_NO-talesyntansen-medium" - en god norsk stemme
PIPER_VOICE_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main/no/no_NO/talesyntansen/medium"
wget -q "${PIPER_VOICE_URL}/no_NO-talesyntansen-medium.onnx" -O norwegian.onnx || echo "⚠️ Kunne ikke laste ned stemme automatisk"
wget -q "${PIPER_VOICE_URL}/no_NO-talesyntansen-medium.onnx.json" -O norwegian.onnx.json || echo "⚠️ Kunne ikke laste ned config automatisk"

cd $PROJECT_DIR

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ Del 2 fullført!                                           ║"
echo "║                                                               ║"
echo "║  Neste steg:                                                  ║"
echo "║  1. Sett opp API-nøkkel: nano .env                            ║"
echo "║  2. Kjør del 3: bash 03-test-audio.sh                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
