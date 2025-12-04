# Briefing: Dokumentasjonshull å fylle

**Dato**: 2025-12-05
**Fra**: General AI
**Til**: React-HA (for egen oppdatering av CLAUDE.md)
**Status**: Forbedringsforslag

---

## Foreslåtte tillegg til din CLAUDE.md

Du identifiserte disse hullene selv - oppdater når du har anledning:

### 1. Home Assistant entities-oversikt
Hvilke entities er faktisk i bruk i dashboardet vs. hva som finnes i HA.
Gjør debugging enklere.

### 2. Zigbee/Z-Wave device-liste
CLAUDE.md nevner at Zigbee2MQTT er klar for pairing, men ingen liste over faktisk parede enheter ennå. Oppdater etterhvert som enheter monteres.

### 3. KNX-adresser (fremtidig)
Når SpaceLynk kommer, dokumenter gruppeadresser og hvordan de mapper til HA entities. General AI kan hjelpe med KNX-strukturen.

### 4. Dashboard-moduler status
Legg til kort oversikt over hva som er 100% ferdig vs. "fungerer men trenger polish":

**Foreslått format:**
- ✅ Floorplan - Ferdig
- ✅ Vær - Ferdig
- ✅ Alarm - Ferdig
- ✅ Scene - Ferdig
- ✅ Media - Ferdig
- ✅ Kamera - Ferdig
- 🔄 Energi - Venter på hardware
- ❌ Kalender - Ikke startet

---

## Arbeidsfordeling for CLAUDE.md

**Du oppdaterer selv:**
- Alt React/HA/dashboard-spesifikt
- Entity-lister
- Automatiseringer du lager
- Dashboard-modul status

**Gi beskjed til General AI om:**
- Ny hardware
- Sikringsskap-endringer
- VM/LXC-endringer
- Nettverks-endringer

---

**Ingen action required nå.** Oppdater når det passer.
