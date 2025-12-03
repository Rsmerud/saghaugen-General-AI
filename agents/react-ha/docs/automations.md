# AUTOMATIONS KATALOG

**Generert**: 2025-12-03
**Formål**: Komplett oversikt over alle automations, scripts og flows

---

## 📋 HOME ASSISTANT AUTOMATIONS

Alle automations ligger i `/config/automations.yaml` på HA Prod (10.12.0.20).

### 🌙 Gang-lys automatiseringer

#### 1. Gang 2. etg - Kveldsdimming
- **Entity ID**: `automation.gang_2_etg_dimme_til_1_kl_21_00`
- **Trigger**: Tid kl. 21:00
- **Condition**: Ingen
- **Action**:
  - Dimmer `light.gang_lys` til 1% over 60 sekunder
  - Smooth transition for å ikke blende
- **Status**: ✅ Aktiv og fungerer
- **Kritisk**: Nei (komfort)
- **Fil**: `/config/automations.yaml` (HA Prod)

```yaml
- id: 'gang_2_etg_dimme_kl_2100'
  alias: Gang 2. etg - Dimme til 1% kl 21:00
  trigger:
    - platform: time
      at: "21:00:00"
  action:
    - service: light.turn_on
      target:
        entity_id: light.gang_lys
      data:
        brightness_pct: 1
        transition: 60
```

#### 2. Gang 2. etg - Morgendimming
- **Entity ID**: `automation.gang_2_etg_sette_til_50_kl_09_00`
- **Trigger**: Tid kl. 09:00
- **Condition**: Ingen
- **Action**:
  - Setter `light.gang_lys` til 50% over 60 sekunder
  - Gradvis økning for behagelig morgenbelysning
- **Status**: ✅ Aktiv og fungerer
- **Kritisk**: Nei (komfort)
- **Fil**: `/config/automations.yaml` (HA Prod)

```yaml
- id: 'gang_2_etg_sett_50_kl_0900'
  alias: Gang 2. etg - Sette til 50% kl 09:00
  trigger:
    - platform: time
      at: "09:00:00"
  action:
    - service: light.turn_on
      target:
        entity_id: light.gang_lys
      data:
        brightness_pct: 50
        transition: 60
```

---

### 🚗 Motorvarmer-automatiseringer (May sin bil)

#### 3. Motorvarmer - Temperaturbasert varighet
- **Entity ID**: `automation.motorvarmer_temperatur_varighet`
- **Trigger**:
  - `sensor.ute_temperatur` endres (eller Yr.no temperatur?)
  - Kjøres også ved oppstart av HA
- **Condition**: Ingen
- **Action**: Setter `input_number.motorvarmer_varighet` basert på temperatur:
  - < -20°C → 60 minutter
  - < -10°C → 45 minutter
  - ≥ -10°C → 30 minutter
- **Status**: ✅ Aktiv
- **Kritisk**: Ja (brukervennlighet for May)
- **Fil**: `/config/automations.yaml` (HA Prod)

```yaml
- id: 'motorvarmer_temp_varighet'
  alias: Motorvarmer - Temperaturbasert varighet
  trigger:
    - platform: state
      entity_id: sensor.ute_temperatur  # MÅ VERIFISERES - hvilken sensor?
    - platform: homeassistant
      event: start
  action:
    - choose:
        - conditions:
            - condition: numeric_state
              entity_id: sensor.ute_temperatur
              below: -20
          sequence:
            - service: input_number.set_value
              target:
                entity_id: input_number.motorvarmer_varighet
              data:
                value: 60
        - conditions:
            - condition: numeric_state
              entity_id: sensor.ute_temperatur
              below: -10
          sequence:
            - service: input_number.set_value
              target:
                entity_id: input_number.motorvarmer_varighet
              data:
                value: 45
      default:
        - service: input_number.set_value
          target:
            entity_id: input_number.motorvarmer_varighet
          data:
            value: 30
```

#### 4. Motorvarmer - Planlagt start
- **Entity ID**: `automation.motorvarmer_planlagt_start`
- **Trigger**: `input_datetime.motorvarmer_starttid` (time trigger)
- **Condition**:
  - `input_boolean.motorvarmer_enable` er ON
  - Dagens ukedag matcher en av:
    - `input_boolean.motorvarmer_mandag` ... `*_søndag`
- **Action**:
  - Slår på `switch.motorvarmer`
  - Setter status-melding med ferdig-tid
  - Beregner `input_datetime.motorvarmer_ferdig` (nå + varighet)
- **Status**: ✅ Aktiv
- **Kritisk**: Ja (hovedfunksjon)
- **Fil**: `/config/automations.yaml` (HA Prod)

```yaml
- id: 'motorvarmer_planlagt_start'
  alias: Motorvarmer - Planlagt start
  trigger:
    - platform: time
      at: input_datetime.motorvarmer_starttid
  condition:
    - condition: state
      entity_id: input_boolean.motorvarmer_enable
      state: 'on'
    - condition: or
      conditions:
        - condition: and
          conditions:
            - condition: time
              weekday: mon
            - condition: state
              entity_id: input_boolean.motorvarmer_mandag
              state: 'on'
        # (Repeat for alle dager: tirsdag, onsdag, etc.)
  action:
    - service: switch.turn_on
      target:
        entity_id: switch.motorvarmer
    - service: input_text.set_value
      target:
        entity_id: input_text.motorvarmer_status
      data:
        value: "Varmer... Klar kl {{ (now() + timedelta(minutes=states('input_number.motorvarmer_varighet')|int)).strftime('%H:%M') }}"
    # Setter også input_datetime.motorvarmer_ferdig (kompleks template)
```

#### 5. Motorvarmer - Auto-av
- **Entity ID**: `automation.motorvarmer_auto_av`
- **Trigger**: `input_datetime.motorvarmer_ferdig` tid nådd
- **Condition**: `switch.motorvarmer` er ON
- **Action**:
  - Slår av `switch.motorvarmer`
  - Setter status: "Bilen er klar! 🚗"
- **Status**: ✅ Aktiv
- **Kritisk**: Ja (sikkerhet - ikke la motorvarmer stå på evig)
- **Fil**: `/config/automations.yaml` (HA Prod)

```yaml
- id: 'motorvarmer_auto_av'
  alias: Motorvarmer - Auto-av
  trigger:
    - platform: time
      at: input_datetime.motorvarmer_ferdig
  condition:
    - condition: state
      entity_id: switch.motorvarmer
      state: 'on'
  action:
    - service: switch.turn_off
      target:
        entity_id: switch.motorvarmer
    - service: input_text.set_value
      target:
        entity_id: input_text.motorvarmer_status
      data:
        value: "Bilen er klar! 🚗"
```

---

### 💡 Utelys automatisering

#### 6. Utelys - Soloppgang/nedgang
- **Entity ID**: `automation.utelys_soloppgang_nedgang` (ANTATT - må verifiseres)
- **Trigger**:
  - `sun.sun` state endres (sunrise/sunset)
  - Offset: +/- 30 minutter
- **Condition**: `input_boolean.utelys_auto` er ON
- **Action**:
  - Slår på/av utelys basert på soloppgang/nedgang
- **Status**: ❓ Må verifiseres (kan være i Node-RED i stedet)
- **Kritisk**: Nei (komfort)
- **Fil**: `/config/automations.yaml` (HA Prod) ELLER Node-RED

```yaml
# EKSEMPEL - må verifiseres
- id: 'utelys_auto'
  alias: Utelys - Soloppgang/nedgang
  trigger:
    - platform: sun
      event: sunset
      offset: "-00:30:00"
    - platform: sun
      event: sunrise
      offset: "00:30:00"
  condition:
    - condition: state
      entity_id: input_boolean.utelys_auto
      state: 'on'
  action:
    - service: light.turn_{{ 'on' if trigger.event == 'sunset' else 'off' }}
      target:
        entity_id: light.utelys  # MÅ VERIFISERES
```

---

## 🔧 HOME ASSISTANT SCRIPTS

Alle scripts ligger i `/config/scripts.yaml` på HA Prod (10.12.0.20).

### Script 1: Motorvarmer - Start nå

- **Entity ID**: `script.motorvarmer_start_na`
- **Beskrivelse**: Starter motorvarmer umiddelbart med smart feedback
- **Input**: Ingen
- **Action**:
  1. Slår på `switch.motorvarmer`
  2. Beregner ferdig-tid (nå + varighet)
  3. Setter status: "Varmer... Bilen er klar om XX minutter"
  4. Setter `input_datetime.motorvarmer_ferdig`
- **Brukt fra**: Dashboard-knapp (Lovelace)
- **Status**: ✅ Aktiv
- **Kritisk**: Nei (nice-to-have manuell trigger)

```yaml
motorvarmer_start_na:
  alias: "Motorvarmer - Start nå"
  sequence:
    - service: switch.turn_on
      target:
        entity_id: switch.motorvarmer
    - service: input_text.set_value
      target:
        entity_id: input_text.motorvarmer_status
      data:
        value: "Varmer... Bilen er klar om {{ states('input_number.motorvarmer_varighet')|int }} minutter"
    - service: input_datetime.set_datetime
      target:
        entity_id: input_datetime.motorvarmer_ferdig
      data:
        datetime: "{{ (now() + timedelta(minutes=states('input_number.motorvarmer_varighet')|int)).strftime('%Y-%m-%d %H:%M:%S') }}"
```

---

## 🔀 NODE-RED FLOWS

Node-RED kjører på 10.12.0.24:1880. Flows lagres i `/home/ronny/.node-red/flows.json` (eller `/opt/node-red/`?).

### Flow 1: Utelys automatikk (ANTATT)

- **Navn**: "Utelys soloppgang/nedgang"
- **Trigger**: HA `sun.sun` entity state change
- **Nodes**:
  1. HA events: in node (sun.sun state change)
  2. Switch node (sunrise vs. sunset)
  3. Function node (30 min offset beregning?)
  4. HA call service node (light.turn_on/off)
- **Status**: ❓ Må verifiseres
- **Kritisk**: Nei
- **Notater**: Kan være i HA automations i stedet - må sjekkes

### Flow 2: MQTT → HA Forwarding (ANTATT)

- **Navn**: Ukjent
- **Trigger**: MQTT message på spesifikke topics
- **Action**: Forwarding eller transformasjon til HA entities
- **Status**: ❓ Må verifiseres ved å logge på Node-RED
- **Notater**: Kan være flere flows for forskjellige sensorer

### Flow X: Andre flows

**MÅ KARTLEGGES ved å logge på Node-RED og eksportere alle flows til JSON.**

Mulige flows basert på antakelser:
- ChirpStack LoRa → HA integration
- Custom MQTT-baserte automations
- Komplekse scener med flere steg
- Notifikasjoner/alerts

---

## 🎬 HOME ASSISTANT SCENES

Scenes kan være definert i:
- `/config/scenes.yaml`
- UI-generert i `/config/.storage/`

### Scene 1-4: Hovedscener (antatt)

Basert på React dashboard `SceneModule.tsx` filter:
- **Borte** - Alt av og alarm på
- **Hjemme** - Normal belysning
- **Stemning** - Dimmet lys, musikk?
- **Ferie** - Simulering av tilstedeværelse?

**MÅ VERIFISERES** ved å logge på HA og se faktiske scenes.

---

## 📊 SAMMENLIGNINGSTABELL

| Type | Antall | Kritisk | Status |
|------|--------|---------|--------|
| **HA Automations** | ~6 | 3 stk | ✅ Verifisert |
| **HA Scripts** | ~1 | 0 stk | ✅ Verifisert |
| **HA Scenes** | ? | ? | ❓ Må kartlegges |
| **Node-RED Flows** | ? | ? | ❓ Må kartlegges |
| **Lovelace Dashboards** | ? | 1 (motorvarmer) | ❓ Må kartlegges |

---

## 🚨 KRITISKE AUTOMATIONS (MÅ ALLTID VIRKE)

1. **Motorvarmer planlagt start** - May er avhengig av dette
2. **Motorvarmer auto-av** - Sikkerhet (ikke la motorvarmer stå på evig)
3. **Motorvarmer temperaturbasert varighet** - Brukervennlighet

**Nice-to-have (ikke kritisk):**
- Gang-lys dimming
- Utelys automatikk
- Motorvarmer "start nå" script

---

## 📝 MANGLENDE DOKUMENTASJON

**Hva jeg MÅ kartlegge når jeg får tilgang:**

### Home Assistant
- [ ] Alle scenes i `/config/scenes.yaml`
- [ ] Lovelace dashboards (motorvarmer card, andre?)
- [ ] HACS custom integrations (hvilke er installert?)
- [ ] Helpers (input_boolean, input_number, etc.) - full liste
- [ ] Alle entities (lys, brytere, sensorer) - komplett oversikt

### Node-RED
- [ ] Eksportere alle flows til JSON
- [ ] Dokumentere hver flow (formål, trigger, action)
- [ ] Sjekke HA WebSocket connection status
- [ ] Verifisere MQTT connections

### Grafana
- [ ] Liste over alle dashboards
- [ ] InfluxDB queries som brukes
- [ ] Alerts/notifications som er satt opp

### Generelt
- [ ] Backup-strategi for automations
- [ ] Testing-prosedyre før deploy til prod
- [ ] Rollback-plan hvis noe går galt

---

## 🔄 DEPLOYMENT-PROSEDYRE

### Nye automations (til prod)

1. **Test først i HA Test (10.12.0.9)**
   - Rediger `/config/automations.yaml` på test-instans
   - Reload via UI eller `automation.reload` service
   - Verifiser at automation fungerer som forventet

2. **Deploy til prod**
   - SSH til HA Prod: `ssh homeassistant@10.12.0.20`
   - Backup: `cp /config/automations.yaml /config/automations.yaml.bak`
   - Rediger `/config/automations.yaml`
   - Reload: `curl -X POST http://localhost:8123/api/services/automation/reload -H "Authorization: Bearer TOKEN"`
   - Verifiser i HA UI

3. **Rollback hvis noe går galt**
   - `cp /config/automations.yaml.bak /config/automations.yaml`
   - Reload igjen

### Node-RED flows

1. **Utvikle/test i Node-RED UI** (10.12.0.24:1880)
2. **Deploy** via Node-RED UI (Deploy-knapp)
3. **Backup**: Eksporter flow til JSON via UI
4. **Verifiser** at flow kjører

---

**Sluttnot**: Denne filen må oppdateres etter at jeg har logget på Node-RED og fått full oversikt over flows. Mye er basert på antakelser fra CLAUDE.md og kodebase-scanning.

**Neste steg**:
- Logge på Node-RED og eksportere flows
- Kartlegge alle HA entities og scenes
- Dokumentere Lovelace dashboards

**Sist oppdatert**: 2025-12-03
