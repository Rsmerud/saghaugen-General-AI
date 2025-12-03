# Protokoller og Integrasjoner på Saghaugen

Dette dokumentet gir en oversikt over alle kommunikasjonsprotokoller og integrasjoner brukt på Saghaugen.

## KNX

**Formål**: Kritisk smarthus-funksjonalitet (lys på/av, etc.)

**Type**: Buss-system for bygningsautomatisering
**Transportlag**: KNX IP (over nettverk)
**Konfigurasjon**: ETS (Engineering Tool Software)

**Ansvarlig**: [TBD - fremtidig knx-manager agent?]

**Kritisk**: Ja - dette er backup når HomeAssistant er nede

**Dokumentasjon**:
- Gruppeadresser: [TBD - må dokumenteres fra ETS]
- IP Interface: [IP adresse TBD]

---

## MQTT

**Formål**: Message bus for alle sensorer, automations, og integrasjoner

**Type**: Publish/Subscribe message protocol
**Broker**: EMQ (eller lignende)
**Port**: 1883 (standard), 8883 (TLS)

**Ansvarlig**: [TBD - kanskje General AI selv?]

**Topic-struktur**:
```
saghaugen/
├── sensors/
│   ├── temperature/
│   ├── humidity/
│   ├── motion/
│   └── lora/
├── homeassistant/
│   └── [HA auto-discovery topics]
├── zigbee2mqtt/
│   └── [Zigbee devices]
└── zwave2mqtt/
    └── [Z-wave devices]
```

**Viktig**: Koordiner med General AI før du endrer topic-struktur!

---

## Zigbee

**Formål**: Trådløse sensorer og enheter

**Type**: Mesh network for IoT devices
**Gateway**: Zigbee2MQTT
**Protokoll**: Zigbee → MQTT bridge

**Ansvarlig**: react-ha (via HomeAssistant integrasjon)

**Enheter**: [TBD - liste over Zigbee enheter]

---

## Z-wave

**Formål**: Trådløse sensorer og enheter

**Type**: Mesh network for home automation
**Gateway**: Zwave2MQTT
**Protokoll**: Z-wave → MQTT bridge

**Ansvarlig**: react-ha (via HomeAssistant integrasjon)

**Enheter**: [TBD - liste over Z-wave enheter]

---

## LoRaWAN

**Formål**: Long-range sensorer (utendørs, skog, etc.)

**Type**: Long Range Wide Area Network
**Gateway**: Custom RaspberryPi + Sx1202
**Network Server**: Chirpstack

**Ansvarlig**: react-ha (Chirpstack), [fremtidig lora-sentinel agent?]

**Sensorer**: Egenutviklede Sensirion-baserte sensorer

**Use cases**:
- Temperatur/fuktighet i skog
- Dyreliv-tracking?
- Vann-nivå i brønn?
- [TBD - flere use cases]

---

## Modbus

**Formål**: Kommunikasjon med industrielt utstyr

**Type**: Serial/TCP kommunikasjonsprotokoll
**Variant**: Modbus TCP/IP

**Ansvarlig**: [TBD]

**Enheter**: [TBD - hvilke Modbus enheter har vi?]

---

## Crestron

**Formål**: [TBD - hva brukes Crestron til på Saghaugen?]

**Type**: Proprietær kontrollsystem for AV/smarthus
**Programvare**: SIMPL Windows

**Ansvarlig**: Ronny (manuell programmering foreløpig)

**Integrasjon med HA**: [TBD]

---

## Unifi Network

**Formål**: Nettverk (WiFi, switching, routing)

**Type**: Enterprise WiFi og nettverk
**Controller**: Unifi Network Application
**Enheter**:
- UDM (Dream Machine)
- Unifi switches

**Ansvarlig**: [TBD - infrastruktur agent?]

**VLAN-struktur**: [TBD]

---

## MikroTik

**Formål**: [TBD - hva brukes MikroTik til?]

**Type**: Routing/switching equipment
**Konfigurasjon**: RouterOS

**Ansvarlig**: [TBD]

---

## HomeAssistant API

**Formål**: Smarthus-koordinering og automation

**Type**: REST API + WebSocket
**URL**: http://homeassistant:8123
**Autentisering**: Long-lived access tokens

**Ansvarlig**: react-ha

**Viktige endpoints**:
- `/api/states` - Current state of all entities
- `/api/services` - Call services
- `/api/events` - Subscribe to events

---

## InfluxDB

**Formål**: Tidsseriedata lagring

**Type**: Time-series database
**URL**: http://influxdb:8086
**Versjon**: [1.x eller 2.x?]

**Ansvarlig**: react-ha

**Databaser**:
- `homeassistant` - HA sensor data
- [andre databaser?]

---

## Grafana API

**Formål**: Visualisering og dashboards

**Type**: REST API for dashboard management
**URL**: http://grafana:3000

**Ansvarlig**: react-ha

---

## Notater

- Alle protokoller skal ha dokumentert failover-strategi
- Secrets (API keys, tokens) ligger IKKE i Git - bruk environment variables
- Hvis du legger til ny protokoll, oppdater dette dokumentet!
