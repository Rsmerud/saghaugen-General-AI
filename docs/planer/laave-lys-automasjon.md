# Låve Lys-automasjon

**Opprettet**: 2025-12-14
**Status**: ✅ FERDIG
**Formål**: Automatisk lysstyring i låven med bevegelsessensor

---

## Oversikt

Provisorisk lysoppsett i låven med skjøteledninger. For å unngå slitasje på stikkontakter brukes Fibaro Wall Plugs styrt av Aqara bevegelsessensor.

---

## Hardware

### Z-Wave - Fibaro Wall Plugs

| Navn | Modell | Formål | Node ID |
|------|--------|--------|---------|
| WP01 | FGWPE/F-102 ZW5 | Lys Lager | 2 |
| WP02 | FGWPE/F-102 ZW5 | Bay lights | 3 |
| WP03 | FGWPE/F-102 ZW5 | Lysarmaturer | 4 |
| WP04 | FGWPE/F-102 ZW5 | For future use | 5 |

**Inkludering**: Trykk knappen 3 ganger raskt

### Zigbee - Aqara Bevegelsessensor

| Navn | Modell | Formål | IEEE Address |
|------|--------|--------|--------------|
| MS01 | RTCGQ11LM | Trigger lys | 0x00158d0007e3186f |

**Pairing**: Hold reset-knappen i 5 sek til LED blinker

---

## Nettverk

| Protokoll | Controller | LXC | Frontend |
|-----------|------------|-----|----------|
| Z-Wave | ZWA-2 (via USB/IP) | 113 | http://10.12.0.28:8092 |
| Zigbee | ZBT-2 (via USB/IP) | 111 | http://10.12.0.26:8082 |

---

## Automasjon

### Logikk

```
HVIS bevegelse detektert (MS01)
  SÅ slå på alle wall-plugs (WP01-04)

HVIS ingen bevegelse på X minutter
  SÅ slå av alle wall-plugs
```

### Home Assistant Automation (Implementert)

**Entity IDs:**
- Bevegelsessensor: `binary_sensor.0x00158d0007e3186f_occupancy`
- Wall plugs: `switch.wp01`, `switch.wp02`, `switch.wp03`, `switch.wp04`

**Automasjoner i HA:**
- `automation.laave_lys_pa_ved_bevegelse` - Slår på alle plugs ved bevegelse
- `automation.laave_lys_av_etter_10_min` - Slår av etter 10 min uten bevegelse

```yaml
# Lys PÅ ved bevegelse
alias: "Laave - Lys pa ved bevegelse"
trigger:
  - platform: state
    entity_id: binary_sensor.0x00158d0007e3186f_occupancy
    to: "on"
action:
  - service: switch.turn_on
    target:
      entity_id:
        - switch.wp01
        - switch.wp02
        - switch.wp03
        - switch.wp04

---

# Lys AV etter 10 min inaktivitet
alias: "Laave - Lys av etter 10 min"
trigger:
  - platform: state
    entity_id: binary_sensor.0x00158d0007e3186f_occupancy
    to: "off"
    for:
      minutes: 10
action:
  - service: switch.turn_off
    target:
      entity_id:
        - switch.wp01
        - switch.wp02
        - switch.wp03
        - switch.wp04
```

---

## Status

- [x] Fibaro WP01 inkludert (Node 2)
- [x] Fibaro WP02 inkludert (Node 3)
- [x] Fibaro WP03 inkludert (Node 4)
- [x] Fibaro WP04 inkludert (Node 5)
- [x] Aqara MS01 pairet (0x00158d0007e3186f)
- [x] Automasjon opprettet i HA
- [x] Testet og verifisert i låven ✅

---

## Notater

- Wall-plugs kan flyttes rundt etter behov (generiske navn)
- Timeout på lys-av kan justeres
- Vurder å legge til manuell overstyring via bryter

---

## Oppdateringslogg

| Dato | Endring |
|------|---------|
| 2025-12-14 17:00 | Opprettet plan. Inkludering startet. |
| 2025-12-14 17:30 | Alle 4 Fibaro Wall Plugs inkludert (Node 2-5). |
| 2025-12-14 17:45 | Aqara MS01 (RTCGQ11LM) pairet og navngitt. |
| 2025-12-14 18:00 | Automasjoner opprettet i HA via API. Alt ferdig! |
| 2025-12-14 18:15 | Testet i låven - fungerer perfekt! |
