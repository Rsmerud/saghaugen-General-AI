# Saghaugen - Nåværende Infrastruktur

**Sist oppdatert**: 2025-12-11
**Eier**: General AI (holder dette oppdatert basert på agent-rapporter og Ronny's input)

---

## Fysisk Infrastruktur

### Bygninger

#### Tømmerhus (1943)
- **Størrelse**: ~70-80 kvm grunnflate (må måles eksakt)
- **Status**: Bebodd siden august 2025
- **Hovedprosjekter fullført**:
  - Bad: 97% ferdig (mangler: siliconfuger, litt innredning, KNX gulvvarme-programmering)
  - Avløpsordning godkjent og etablert
- **Neste store prosjekt**: Kjøkken (gammelt kjøkken er nå badet)
- **Planlagte endringer**:
  - Skifte gulv i entre (vår 2026)
  - Minimere synlig teknisk infrastruktur (skal virke lite teknisk)

#### Låve/Uthus (ca. 2000, tidligere sagbruk)
- **Total størrelse**: 130 kvm
- **Isolert verksted**: 30 kvm (100mm Glava) - ~20% ferdig innredet
- **Uisolert låve**: 100 kvm
- **Plan**: Isolere ytterligere 50 kvm (totalt 80 kvm isolert på sikt)
- **Formål**:
  - Verksted (pågående)
  - Teknisk hub (mesteparten av infrastruktur skal hit)
  - Fremtidig: Starlink, UDM, switcher, server-rack

### Tomt
- **Størrelse**: 7 mål + 70 mål skog
- **Miljø**: Midt i skogen, aktivt dyreliv
- **Adresse**: Trondsbuvegen 272, 2110 SLÅSTAD, Norge

### Vann og Avløp
- **Vann**: Borehull (ca. år 2000) - IKKE kommunalt vann
- **Avløp**: Nylig godkjent ordning (tidligere utedo)

---

## Elektrisk Infrastruktur

### Sikringsskap (Hovedskap - Huset)
**Status**: ✅ Fullstendig dokumentert av React-HA agent

**Hovedsikring**: 50A 3-fas + RCD type A 30mA (Kurs 1-2)

**Kritiske kurs (I BRUK)**:
- Kurs 3: IT/SERVER (Proxmox, router) - 16A C-kurve
- Kurs 4: BRØNNPUMPE - 16A C-kurve
- Kurs 5: VARMTVANNSBEREDER - 20A C-kurve
- Kurs 6: KJØKKEN STIKKONTAKTER - 16A C-kurve
- Kurs 7: STEKEOVN - 16A C-kurve ⚠️ (viktig for fremtidige kjøkkenplaner!)
- Kurs 8: VARMEPUMPE - 16A C-kurve
- Kurs 9: LYS/VVK BAD - 10A B-kurve
- Kurs 10: LYS STUE/GANG OG STIKK GANG - 16A C-kurve
- Kurs 11: STIKKONTAKTER STUE - 16A C-kurve
- Kurs 12: STIKKONTAKTER SOVEROM/KONTOR - 16A C-kurve
- Kurs 13: STIKK VASKEMASKIN - 16A C-kurve
- Kurs 14: TEKNISK 2. ETG - 16A C-kurve
- Kurs 15: LYS OG STIKK SOVEROM - 16A C-kurve
- Kurs 16: LYS OG STIKK GJESTEROM - 16A C-kurve
- Kurs 17: LYS OG STIKK KJELLER - 16A C-kurve
- Kurs 18: STIKK TØRKETROMMEL - 16A C-kurve
- Kurs 19: UTGANG TIL UNDERFORDELING (Låve) - 32A C-kurve 3-fas
  - Underfordeling: Lys, stikk, garasjeport, WiFi AP, KNX/Crestron
- Kurs 20: UTENDØRS LYS - 10A B-kurve (HA-styrt)
- Kurs 21: ELBILLADER - 32A C-kurve 3-fas (22 kW)

**LEDIGE KURS** (Viktig for fremtidige prosjekter!):
- **Kurs 22**: RESERVE (ledig) - 16A C-kurve
- **Kurs 23**: RESERVE (solceller/batteri) - 20A C-kurve
- **Kurs 24**: RESERVE (generell utvidelse) - 16A C-kurve

**Kritisk for kjøkkenprosjektet**:
- Kurs 7 (stekeovn 16A) er allerede i bruk
- Hvis du vil ha EKSTRA stekeovn → må bruke Kurs 22/24 (16A) eller oppgradere eksisterende
- Induksjonstopp trenger typisk 32A 3-fas (ikke ledig uten oppgradering!)

**Kilde**: Dokumentert av React-HA i `saghaugen-infopanel/Kursfortegnelse_Saghaugen.html`

### KNX
- **Status**: Installert, håndterer kritiske funksjoner (lys på/av, etc.)
- **KNX Gulvvarme**: I bad, programmering gjenstår
- **Filosofi**: KNX = kritiske/viktige funksjoner

---

## Nettverk

### Internett
- **Nåværende**: Starlink
- **Fremtidig**: Fiber bestilt (leveringsdato uklar)
- **Plan**: Starlink, UDM og switcher monteres i låve når fiber kommer

### VPN/Nettverk-tunneler
- **ZeroTier VPN**: Saghaugen ↔ Jobb-servere
- **Formål**: Off-site backup, failover, ressursdeling
- **Status**: Aktivt

### Nettverksutstyr
- **Unifi UDM-Pro**: 10.12.0.1 (hovedgateway)
  - SSH: `ssh root@10.12.0.1` (passwordless for General AI)
  - Hostname: T272-Ronny-Smerud
- **Unifi Switcher**:
  - T272SW01Teknisk: 10.12.0.2
  - T272SW02-Kjkken: 10.12.0.3
  - T272SW03-Verksted: 10.12.0.200
- **Unifi AP-er**:
  - T272AP01-Utendrs: 10.12.0.127
  - T272AP02-Garasje: 10.12.0.197
  - T272AP03Kjkken: 10.12.0.181
  - AP01-Kontor: 10.12.0.196
- **MikroTik**: Også i bruk (Ronny liker begge merkene)
- **Lokasjon nå**: Provisorisk i huset
- **Fremtidig lokasjon**: Låven
- **Subnet**: 10.12.0.0/24 (lokal)

### Komplett Nettverkskart (per 2025-12-05)

| IP | Hostname | Type | Status |
|----|----------|------|--------|
| 10.12.0.1 | T272-Ronny-Smerud | UDM-Pro Gateway | ✅ Prod |
| 10.12.0.2 | T272SW01Teknisk | Unifi Switch | ✅ Prod |
| 10.12.0.3 | T272SW02-Kjkken | Unifi Switch | ✅ Prod |
| 10.12.0.6 | debian2 | ESXi VM (Docker) | ⚠️ Skal avvikles |
| 10.12.0.9 | debian1 | ESXi VM (gammel HA) | ⚠️ Backup |
| 10.12.0.20 | homeassistant | HA Prod (VM 103) | ✅ Prod |
| 10.12.0.21 | frigate | Frigate NVR | ✅ Prod |
| 10.12.0.22 | emqx | MQTT Broker | ✅ Prod |
| 10.12.0.24 | node-red | Node-RED | ✅ Prod |
| 10.12.0.35 | Chromecast | Media | ✅ Prod |
| 10.12.0.50 | docker-services | Homepage/Portainer | ✅ Prod |
| 10.12.0.51 | nas | OMV (ESXi) | ⚠️ Skal migreres |
| 10.12.0.55 | WIN10-ADMIN | Windows VM | ✅ Prod |
| 10.12.0.65 | SonosZP | Sonos | ✅ Prod |
| 10.12.0.102 | paperless-ngx | Dokumentarkiv | ✅ Prod |
| 10.12.0.114 | casaOS | Container mgmt | ❌ Ikke i bruk |
| 10.12.0.116 | wled-WLED-Gledopto | LED-controller | ✅ Prod |
| 10.12.0.120 | shellyplusplugs | Shelly plugg | ✅ Prod |
| 10.12.0.127 | T272AP01-Utendrs | Unifi AP | ✅ Prod |
| 10.12.0.128 | esphome | ESPHome | ✅ Prod |
| 10.12.0.145 | claude-agents | LXC 150 (utgått) | ❌ Migrert |
| 10.12.0.146 | grafana | Grafana | ✅ Prod |
| 10.12.0.150 | homebox | Homebox | ✅ Prod |
| 10.12.0.154 | HageSor | Reolink kamera | ✅ Prod |
| 10.12.0.155 | Garasje | Reolink kamera | ✅ Prod |
| 10.12.0.181 | T272AP03Kjkken | Unifi AP | ✅ Prod |
| 10.12.0.132 | usb-ip-1 | RPi3 B+ USB/IP | ✅ Prod |
| 10.12.0.183 | win11-admin | Windows 11 VM (General AI) | ✅ Prod |
| 10.12.0.196 | AP01-Kontor | Unifi AP | ✅ Prod |
| 10.12.0.197 | T272AP02-Garasje | Unifi AP | ✅ Prod |
| 10.12.0.200 | T272SW03-Verksted | Unifi Switch | ✅ Prod |
| 10.12.0.205 | proxmox | Proxmox Host | ✅ Prod |

### Tilganger
- **Ronny**: Full tilgang til alt (Saghaugen + jobb-servere)
- **Lasse (kollega)**: Administrerer jobb-servere sammen med Ronny
- **React-HA agent**: Passwordless SSH til Proxmox og alle VM/LXC
- **General AI**:
  - Kjører på Proxmox LXC 150 (10.12.0.145)
  - SSH-tilgang til:
    - Proxmox: `ssh root@10.12.0.205` ✅
    - UDM-Pro: `ssh root@10.12.0.1` ✅
    - debian2: `ssh ronny@10.12.0.6` ✅

---

## Virtualisering og Servere

### Proxmox (nåværende MIDLERTIDIG host)
- **Hardware**: HP mini-PC med i7 prosessor
- **IP**: 10.12.0.205
- **Eierskap**: TILHØRER JOBBEN (ikke Saghaugen permanent)
- **Rolle**: Midlertidig host under migrasjonsperiode
- **Status**: Kjører ~12 VM/LXC inkl. General AI
- **Plan**: Alle VM/LXC skal flyttes til HP EliteDesk når den får Proxmox
- **Kritisk**: Dette er en overgangsløsning, ikke permanent infrastruktur!

### HP EliteDesk 800 G3 (fremtidig PERMANENT host)
- **Tidligere**: Kjører ESXi
- **Plan**: Reinstalleres med Proxmox
- **Når**: Kommer snart
- **Hensikt**: Bli PERMANENT primær host for alle Saghaugen VM/LXC
- **Status**: Avventer reinstallasjon

### ESXi VM-er (på HP EliteDesk - skal migreres/avvikles)

#### debian1 (10.12.0.9)
- **Formål**: Gammel HomeAssistant instans
- **Status**: Beholdt for backup/referanse
- **Aksjon**: Ingen - kan slettes etter ESXi reinstall

#### debian2 (10.12.0.6) ⚠️ VIKTIG
- **OS**: Debian 11 (5.10.0-34-amd64)
- **Disk**: 97GB (31GB brukt)
- **SSH**: `ssh ronny@10.12.0.6` (passord: 4pn44SJAg)
- **Systemtjenester**:
  - Docker (container runtime)
  - ZeroTier (VPN/SDN)
  - Wazuh-agent (security monitoring)
  - VMware Tools

**Docker containers på debian2:**
| Container | Status | Vurdering |
|-----------|--------|-----------|
| **influxdb** (2.7.3) | Running | ⚠️ VIKTIG - Gammel InfluxDB med historiske data |
| **grafana** | Running | Duplikat - prod er på 10.12.0.146 |
| **node-red** | Running | Duplikat - prod er på 10.12.0.24 (Ronny sjekker flows) |
| **esphome** | Running | Duplikat - prod er på 10.12.0.128 |
| **pihole** | Running | ❌ Ikke i bruk |
| **Unifi_controller** | Running | ❌ Ikke i bruk (UDM-Pro har egen) |
| **mongodb** | Running | Støtte for gammel Unifi controller |
| **portainer** | Running | Container management |
| **homarr** | Running | Dashboard |
| **heimdall** | Running | Dashboard |

**Aksjon for debian2:**
- [ ] Ronny sjekker Node-RED flows for ting å kopiere
- [ ] Vurder å eksportere InfluxDB data (nice-to-have, ikke kritisk)
- [ ] Kan slettes etter ESXi reinstall

#### OMV/NAS (10.12.0.51)
- **Formål**: OpenMediaVault - filserver/NAS
- **Status**: Kjører på ESXi
- **Problem**: Kan ikke flyttes pga diskplass på HP mini-PC
- **Aksjon**:
  - [ ] Dokumentere shares og konfigurasjon
  - [ ] Ta backup av kritiske data
  - [ ] Reinstallere etter ESXi → Proxmox migrering

#### casaOS (10.12.0.114)
- **Formål**: Portainer-lignende med ferdige scripts
- **Status**: ❌ Ikke i bruk lenger
- **Aksjon**: Kan slettes

### Jobb-servere (eksternt tilgjengelig via ZeroTier)
**Antall**: 3 stk heavy duty servere
**Lokasjon**: Ronnys jobb
**Specs per server**:
- ~48 kjerner (CPU)
- 1TB RAM hver
- Speiling (RAID)
- UPS (backup strøm)

**Tilkobling**: ZeroTier VPN mellom Saghaugen og jobb
**Administrasjon**: Ronny + Lasse (kollega/kameraet)

**Bruksområder for Saghaugen**:
- **Backup**: Kjøre backuper av Saghaugen VM/LXC ut av huset
- **Failover**: Enkelte tjenester kan kjøres på jobb ved behov
- **Heavy lifting**: Tunge oppgaver som trenger mer ressurser

**Kritisk**: Dette gir Saghaugen redundans og off-site backup!

### VM/LXC Oversikt
**Status**: ✅ Fullstendig dokumentert av React-HA agent
**Antall**: 12+ LXC containers + VMs

#### Proxmox Infrastructure (dokumentert av React-HA):
1. **HomeAssistant Prod** - `10.12.0.20:8123` (LXC) - Forvaltes av React-HA
2. **Frigate NVR** - `10.12.0.21:5000` (LXC) - Reolink kamera recording
3. **EMQX MQTT Broker** - `10.12.0.22:18083` (LXC) - Dedikert MQTT server
4. **ESPHome** - `10.12.0.23:6052` (LXC) - Custom sensor management
5. **Node-RED** - `10.12.0.24:1880` (LXC) - Automasjoner, forvaltes av React-HA
6. **Zigbee2MQTT (Hus)** - `10.12.0.25:8080` (LXC) - Conbee II gateway
7. **Z-Wave JS UI (Hus)** - `10.12.0.27:8091` (LXC) - Aeotec Z-Stick 7
8. **ChirpStack LoRaWAN** - `10.12.0.40:8080` (LXC) - LoRa gateway server
9. **Docker Services** - `10.12.0.50` (LXC) - Homepage, Portainer
10. **PaperlessNGX** - `10.12.0.102:8000` (LXC) - Dokumentarkiv, forvaltes av React-HA
11. **Windows 10 VM** - React-HA kjører herfra (VS Code terminal)
12. **General AI** (LXC) - Dette systemet

**Nettverk**: 10.12.0.0/24 subnet

**Kilde**: Dokumentert av React-HA i `saghaugen-infopanel/README.md` (Backend/Infrastructure seksjon)

---

## Smarthus-systemer

### HomeAssistant
- **Instanser**: 2 (prod + test)
- **Kommunikasjon**: RemoteHomeAssistant mellom instansene
- **Rolle**: "Base" system, styrer scener og komplekse automasjoner
- **Forvalter**: React-HA agent

### Crestron
- **System**: Crestron + Crestron Home
- **Ronnys ekspertise**: Sterkest på Crestron SIMPL Windows
- **Status**: [Må kartlegges]

### KNX
- **Rolle**: Kritiske funksjoner (lys, gulvvarme)
- **Ronnys ekspertise**: God erfaring
- **Status**: Installert, fungerer

### Zigbee
- **Gateway**: Zigbee2MQTT
- **Status**: [Må kartlegges hvilke enheter]

### Z-wave
- **Gateway**: Zwave2MQTT
- **Status**: [Må kartlegges hvilke enheter]

### LoRaWAN
- **Gateway**: Egenbygd (RaspberryPi + Sx1202)
- **Server**: Chirpstack (egen LXC)
- **Sensorer**: Custom Sensirion-baserte sensorer
- **Ronnys ekspertise**: God erfaring med LoRaWAN og sensor-design

### RPi3 B+ USB/IP Gateway (usb-ip-1)
- **IP**: 10.12.0.132 (eth0, statisk) / 10.12.0.188 (WiFi, backup)
- **Hostname**: usb-ip-1
- **Formål**: USB/IP gateway for Zigbee/Z-Wave antenner
- **Hardware**: Raspberry Pi 3 B+ (RPi4 reservert til tale-assistent)
- **USB-enheter**:
  - Nabu Casa ZBT-2 (Zigbee) → Bus 1-1.1.3 → LXC 111 `/dev/ttyZigbee`
  - Nabu Casa ZWA-2 (Z-Wave) → Bus 1-1.1.2 → LXC 113 `/dev/ttyZwave`
- **Bruker**: ronny / 4pn44SJAg
- **SSH**: Passwordless fra General AI ✅
- **Status**: ✅ USB/IP FERDIG og verifisert!
- **Services**:
  - RPi3: `usbipd.service` (binder USB-enheter)
  - Proxmox: `usbip-attach.service` (bruker kabel-IP 10.12.0.132)
- **Plan**: Se `docs/planer/usb-ip-gateway.md` for full dokumentasjon
- **Gjenstår**:
  1. Teste full reboot av stacken
  2. Konfigurere zigbee2mqtt og zwave-js-ui i LXC-ene

### MQTT
- **Broker**: Dedikert (EMQ eller lignende)
- **Status**: [Må kartlegges hvilken LXC]

### Modbus
- **Status**: [Må kartlegges]

---

## Dashboards og Interfaces

### 10" React Dashboard
- **Lokasjon**: Entre (provisorisk montert)
- **Status**: Fungerer
- **Plan**: Kommer ned når gulv skiftes (vår 2026)
- **Forvalter**: React-HA agent

### Homepage
- **Type**: Custom hjemmeside for Saghaugen
- **Forvalter**: React-HA agent

### Grafana
- **Rolle**: Monitoring og visualisering
- **Forvalter**: React-HA agent

---

## Verksted (Låven)

### Maskiner og Verktøy
- Søylebor-maskin
- Båndsag
- Arbeidsbord 1.20 x 2.4m med motoriserte ben
- Festool skinnesag
- Flere bajonettsager
- Flere stikksager
- Feinsager
- Bordsag (finnes, ikke i orden enda)
- Kombihøvel 30cm (finnes, ikke i orden enda)

**Status**: ~20% ferdig innredet, godt utstyrt

---

## Kommende Prosjekter (Prioritert)

### 1. Kjøkken (Neste store prosjekt)
- **Status**: Planleggingsfase
- **Prioritet**: Høy
- **Notater**: Gammelt kjøkken er nå badet, nytt kjøkken må bygges
- **Materialer**: TBD (General AI kan søke når Ronny er klar)

### 2. Entre - Gulv og Bjelkelag
- **Status**: Planlagt vår 2026
- **Prioritet**: Høy
- **Notater**: 10" React dashboard panel er provisorisk montert, kommer ned ved gulvskifte
- **Materialer**: TBD

### 3. Terrasse
- **Status**: Planleggingsfase
- **Prioritet**: Medium
- **Materialer**: TBD

### 4. Uteområde
- **Status**: Planleggingsfase
- **Prioritet**: Medium
- **Notater**: Generell oppgradering/tilrettelegging

### 5. Låve - Isolering 50 kvm (Fase 2)
- **Status**: Planleggingsfase (kommer senere)
- **Prioritet**: Medium-lav
- **Omfang**:
  - Isolere ytterligere 50 kvm av låven
  - Bygge ny innevegg
  - **Resultat**: 80 kvm verksted (30+50) + 50 kvm kaldtlager
- **Materialer**: Test-søk gjennomført 2025-12-03 (se findings/)
- **Estimert kostnad**: ~5.000-5.500 kr for treverk + isolasjon

---

## Langsiktige Planer (Ingen konkret tidslinje)

### Energi
- Solceller
- Batterier
- Hybrid-invertere
- Aggregat (backup)

### Bygg
- Drivhus
- Orangerie
- Hønegård
- Carport

### Infrastruktur
- Flytte mesteparten av teknisk infrastruktur til låven
- Fiber-tilkobling når den kommer
- Nettverksutstyr i låven

### Diverse
- Ekstra musefanger-assistent til Frida

---

## Backup og Redundans-strategi

### Off-site backup (via ZeroTier til jobb)
- **Hva**: VM/LXC backuper fra Saghaugen
- **Hvor**: Jobb-servere (3x 1TB RAM, 48 kjerner, speiling, UPS)
- **Hvorfor**: Brannsikring, tyveri-sikring, redundans
- **Status**: Tilgjengelig infrastruktur, må konfigureres

### Failover muligheter
- **Kritiske tjenester** kan kjøres midlertidig på jobb-servere ved:
  - Strømbrudd på Saghaugen (utover UPS-tid)
  - Hardware-feil på Proxmox
  - Nettverk-utfall
- **Tilgjengelig kapasitet**: 3x servere med massive ressurser

### Fremtidig: Lokal backup på Saghaugen
- Når solceller + batterier + aggregat er på plass
- Lokal backup-disk/NAS
- Kombinert med off-site backup på jobb

---

## Kritiske Hull i Dokumentasjonen

**Status etter nettverksscan og research (2025-12-05):**

Dokumentert ✅:
1. ~~**Sikringsskap**~~ - ✅ Fullstendig dokumentert (24 kurs, 3 ledige)
2. ~~**VM/LXC**~~ - ✅ Fullstendig liste med IP-adresser
3. ~~**Jobb-servere**~~ - ✅ 3x heavy duty, ZeroTier, backup-kapasitet
4. ~~**Proxmox midlertidig status**~~ - ✅ Tilhører jobb, skal erstattes
5. ~~**Nettverkskart**~~ - ✅ Komplett kart over alle enheter på 10.12.0.0/24
6. ~~**ESXi VM-er**~~ - ✅ debian1, debian2, OMV, casaOS kartlagt
7. ~~**UDM-Pro tilgang**~~ - ✅ SSH passwordless for General AI
8. ~~**InfluxDB lokasjon**~~ - ✅ Funnet på debian2 (port 8086)

Gjenstår ❌:
9. **Crestron**: Hvilke enheter? Hvordan konfigurert?
10. **Zigbee/Z-wave enheter**: Spesifikke enheter (gatewayer er dokumentert)
11. **HP mini-PC (nåværende Proxmox)**: CPU, RAM, disk specs?
12. **HP EliteDesk specs**: CPU, RAM, disk?
13. **KNX**: Hvilke enheter utover gulvvarme?
14. **Jobb-servere**: Detaljerte specs, backup-konfigurasjon

**Strategi**: Fylles inn gradvis når agenter trenger informasjonen eller når Ronny gir info.

---

## Notater

- Dette dokumentet er levende og oppdateres kontinuerlig
- Når agenter finner ut noe om infrastrukturen, oppdateres dette dokumentet
- Før Ronny kjøper utstyr som påvirker infrastruktur, sjekkes dette dokumentet
- Eksempel: "Ronny vil ha ekstra stekeovn" → General AI sjekker sikringsskap-kapasitet her

---

**Vedlikeholdes av**: General AI
**Kilde**: CLAUDE.md, agent-rapporter, koordinering med React-HA, Ronnys input
