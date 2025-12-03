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

### Sikringsskap
- **Status**: Må kartlegges i detalj
- **Kritisk**: Må dokumenteres hvilke kurs som finnes og kapasitet
- **Eksempel behov**: Hvis Ronny vil ha ekstra stekeovn, må vi vite om det er kapasitet

**TODO for General AI**: Be Ronny om å ta bilde av sikringsskap og dokumentere alle kurs.

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

### Nettverksutstyr
- **Unifi**: UDM + switcher (hovedsakelig)
- **MikroTik**: Også i bruk (Ronny liker begge merkene)
- **Lokasjon nå**: Provisorisk i huset
- **Fremtidig lokasjon**: Låven

### Tilganger
- **Ronny**: Full tilgang til alt
- **React-HA agent**: Passwordless SSH til Proxmox og alle VM/LXC
- **General AI**: Kjører på Proxmox, ingen SSH-tilganger enda

---

## Virtualisering og Servere

### Proxmox (nåværende host)
- **Hardware**: [Må dokumenteres]
- **Rolle**: Midlertidig host for nesten alle VM/LXC
- **Status**: General AI kjører her
- **Plan**: Flytte alle VM/LXC til HP EliteDesk når den får Proxmox

### HP EliteDesk 800 G3
- **Tidligere**: ESXi maskin
- **Plan**: Reinstalleres med Proxmox
- **Når**: Snart™
- **Hensikt**: Bli primær host for alle VM/LXC

### VM/LXC Oversikt
**Antall**: ~11 (og økende)

#### Kjente VM/LXC:
1. **HomeAssistant Prod** (LXC?) - Forvaltes av React-HA
2. **HomeAssistant Test** (LXC?) - Forvaltes av React-HA
3. **Node-Red** (LXC?) - Forvaltes av React-HA
4. **Grafana** (LXC?) - Forvaltes av React-HA
5. **InfluxDB** (LXC?) - Forvaltes av React-HA
6. **Chirpstack** (LXC?) - Forvaltes av React-HA
7. **Paperless-ngx** (LXC?) - Forvaltes av React-HA
8. **MQTT Broker** (EMQ eller lignende) (LXC?) - Status?
9. **Windows 10 VM** - React-HA kjører herfra (VS Code terminal)
10. **Homepage** (LXC?) - Custom hjemmeside, forvaltes av React-HA
11. **General AI** (LXC?) - Dette systemet

**TODO for General AI**: Få fullstendig liste fra React-HA ved koordineringsmøte.

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

## Fremtidige Planer

### Energi
- Solceller
- Batterier
- Hybrid-invertere
- Aggregat (backup)

### Bygg
- Isolere ytterligere 50 kvm av låven
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

## Kritiske Hull i Dokumentasjonen

Disse må fylles inn:

1. **Sikringsskap**: Hvilke kurs finnes? Kapasitet?
2. **VM/LXC**: Fullstendig liste med spesifikasjoner
3. **Crestron**: Hvilke enheter? Hvordan konfigurert?
4. **Zigbee/Z-wave**: Hvilke enheter?
5. **Proxmox hardware**: CPU, RAM, disk?
6. **HP EliteDesk specs**: CPU, RAM, disk?

**Strategi**: Fylles inn gradvis når agenter trenger informasjonen eller ved koordinering med React-HA.

---

## Notater

- Dette dokumentet er levende og oppdateres kontinuerlig
- Når agenter finner ut noe om infrastrukturen, oppdateres dette dokumentet
- Før Ronny kjøper utstyr som påvirker infrastruktur, sjekkes dette dokumentet
- Eksempel: "Ronny vil ha ekstra stekeovn" → General AI sjekker sikringsskap-kapasitet her

---

**Vedlikeholdes av**: General AI
**Kilde**: CLAUDE.md, agent-rapporter, koordinering med React-HA, Ronnys input
