#!/bin/bash
#===============================================================================
# HEI GENERAL - Voice Assistant PoC Setup Script
# Del 3: Test lyd-inn og lyd-ut
#===============================================================================

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🎖️  HEI GENERAL - Voice Assistant Setup (Del 3)  🎖️      ║"
echo "║                   Audio Test                                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="/home/pi/hei-general"
cd $PROJECT_DIR

# Test mikrofon
echo "🎤 Test 1: Mikrofon-opptak"
echo "   Snakk i 5 sekunder..."
arecord -d 5 -f cd test_recording.wav
echo "   ✅ Opptak lagret som test_recording.wav"

echo ""
echo "🔊 Test 2: Avspilling"
echo "   Spiller av opptaket..."
aplay test_recording.wav
echo "   ✅ Avspilling ferdig"

echo ""
echo "🔊 Test 3: TTS (Text-to-Speech)"
source venv/bin/activate

# Test Piper TTS
if [ -f "models/piper/norwegian.onnx" ]; then
    echo "   Tester Piper med norsk stemme..."
    echo "Hei! Jeg er General AI, din personlige assistent for Saghaugen." | \
        piper --model models/piper/norwegian.onnx --output_file test_tts.wav
    aplay test_tts.wav
    echo "   ✅ TTS fungerer!"
else
    echo "   ⚠️ Norsk stemme ikke funnet. Tester med espeak..."
    espeak-ng -v no "Hei! Jeg er General AI." --stdout | aplay
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🎤 Hørte du deg selv og TTS-stemmen?                         ║"
echo "║                                                               ║"
echo "║  JA  → Kjør: python3 hei_general.py                          ║"
echo "║  NEI → Sjekk: alsamixer (velg riktig lydkort)                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
