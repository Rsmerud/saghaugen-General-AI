#!/bin/bash

# Health check script for Saghaugen infrastructure
# Brukes av alle agenter for å sjekke system-status

set -e

echo "🏥 Saghaugen Health Check"
echo "========================="
echo ""

# Fargekoder
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funksjoner for health checks
check_service() {
    local service_name=$1
    local check_command=$2

    echo -n "Checking ${service_name}... "

    if eval "$check_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        return 1
    fi
}

# Check Proxmox host
check_service "Proxmox API" "ping -c 1 proxmox.local"

# Check MQTT broker
check_service "MQTT Broker" "timeout 2 bash -c '</dev/tcp/mqtt-broker/1883'"

# Check HomeAssistant
check_service "HomeAssistant Prod" "curl -s http://homeassistant:8123 > /dev/null"

# Check InfluxDB
check_service "InfluxDB" "curl -s http://influxdb:8086/health > /dev/null"

# Check Grafana
check_service "Grafana" "curl -s http://grafana:3000 > /dev/null"

echo ""
echo "========================="
echo "Health check complete"
echo ""

# TODO: Utvid med flere checks etter hvert som flere tjenester kommer til
# TODO: Legg til Chirpstack health check
# TODO: Legg til KNX IP Interface check
# TODO: Send resultat til InfluxDB for trending
