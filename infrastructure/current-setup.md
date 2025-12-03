# Saghaugen - Nåværende Infrastruktur

**Sist oppdatert**: 2025-12-03
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
- **Unifi**: UDM + switcher (hovedsakelig)
- **MikroTik**: Også i bruk (Ronny liker begge merkene)
- **Lokasjon nå**: Provisorisk i huset
- **Fremtidig lokasjon**: Låven
- **Subnet**: 10.12.0.0/24 (lokal)

### Tilganger
- **Ronny**: Full tilgang til alt (Saghaugen + jobb-servere)
- **Lasse (kollega)**: Administrerer jobb-servere sammen med Ronny
- **React-HA agent**: Passwordless SSH til Proxmox og alle VM/LXC
- **General AI**:
  - Kjører på Proxmox (10.12.0.205)
  - SSH-tilgang: Under oppsett (root@10.12.0.205)

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

**Status etter React-HA integrasjon + jobb-server info (2025-12-03):**

Dokumentert ✅:
1. ~~**Sikringsskap**~~ - ✅ Fullstendig dokumentert (24 kurs, 3 ledige)
2. ~~**VM/LXC**~~ - ✅ Fullstendig liste med IP-adresser
3. ~~**Jobb-servere**~~ - ✅ 3x heavy duty, ZeroTier, backup-kapasitet
4. ~~**Proxmox midlertidig status**~~ - ✅ Tilhører jobb, skal erstattes

Gjenstår ❌:
5. **Crestron**: Hvilke enheter? Hvordan konfigurert?
6. **Zigbee/Z-wave**: Hvilke spesifikke enheter? (vet at Conbee II + Aeotec Z-Stick 7 er gatewayer)
7. **HP mini-PC (nåværende Proxmox)**: CPU, RAM, disk specs?
8. **HP EliteDesk specs**: CPU, RAM, disk?
9. **KNX**: Hvilke enheter utover gulvvarme?
10. **Jobb-servere**: Detaljerte specs, backup-konfigurasjon

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
