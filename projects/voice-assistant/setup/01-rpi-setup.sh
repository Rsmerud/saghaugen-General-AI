#!/bin/bash
#===============================================================================
# HEI GENERAL - Voice Assistant PoC Setup Script
# Del 1: Grunnleggende RPi4 oppsett
#
# Kjør dette ETTER at du har:
# 1. Installert Raspberry Pi OS Lite (64-bit) på microSD
# 2. Aktivert SSH i Raspberry Pi Imager (eller touch /boot/ssh)
# 3. Satt opp WiFi/Ethernet
# 4. Koblet til USB konferansemikrofon
#
# Bruk: ssh pi@<IP> "curl -sSL <url> | bash"
#       eller kopier til RPi og kjør: sudo bash 01-rpi-setup.sh
#===============================================================================

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🎖️  HEI GENERAL - Voice Assistant Setup (Del 1)  🎖️      ║"
echo "║                   Grunnleggende oppsett                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Sjekk at vi kjører som root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Kjør dette scriptet som root: sudo bash $0"
    exit 1
fi

# Sett hostname
HOSTNAME="hei-general"
echo "📛 Setter hostname til: $HOSTNAME"
hostnamectl set-hostname $HOSTNAME
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts

# Oppdater systemet
echo ""
echo "📦 Oppdaterer systemet..."
apt-get update && apt-get upgrade -y

# Installer grunnleggende pakker
echo ""
echo "📦 Installerer grunnleggende pakker..."
apt-get install -y \
    git \
    python3-pip \
    python3-venv \
    python3-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    alsa-utils \
    pulseaudio \
    curl \
    wget \
    htop \
    vim

# Legg til bruker i audio-gruppe
echo ""
echo "🔊 Legger til bruker i audio-gruppe..."
usermod -a -G audio pi 2>/dev/null || usermod -a -G audio $SUDO_USER 2>/dev/null || true

# Test lydenheter
echo ""
echo "🎤 Sjekker lydenheter..."
echo "--- Opptak (mikrofoner) ---"
arecord -l
echo ""
echo "--- Avspilling (høyttalere) ---"
aplay -l

# Opprett prosjektmappe
PROJECT_DIR="/home/pi/hei-general"
echo ""
echo "📁 Oppretter prosjektmappe: $PROJECT_DIR"
mkdir -p $PROJECT_DIR
chown -R pi:pi $PROJECT_DIR 2>/dev/null || chown -R $SUDO_USER:$SUDO_USER $PROJECT_DIR 2>/dev/null || true

# Legg til General AI sin SSH-nøkkel
echo ""
echo "🔑 Legger til General AI sin SSH-nøkkel..."
mkdir -p /home/pi/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMJC6psHByR5D24yc6Nw8b2OOkbOX4QMVZ0tHahzTeAt general-ai@saghaugen.no" >> /home/pi/.ssh/authorized_keys
chmod 700 /home/pi/.ssh
chmod 600 /home/pi/.ssh/authorized_keys
chown -R pi:pi /home/pi/.ssh 2>/dev/null || true

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  ✅ Del 1 fullført!                                           ║"
echo "║                                                               ║"
echo "║  Neste steg:                                                  ║"
echo "║  1. Reboot: sudo reboot                                       ║"
echo "║  2. Kjør del 2: sudo bash 02-voice-software.sh                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
