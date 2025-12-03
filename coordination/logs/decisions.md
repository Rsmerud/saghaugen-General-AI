# Tekniske Beslutninger

Dette dokumentet holder oversikt over viktige tekniske beslutninger tatt av General AI og hvorfor.

## Format

Hver beslutning dokumenteres slik:

```
## [YYYY-MM-DD] Beslutning tittel

**Kontekst**: Hva var situasjonen?
**Beslutning**: Hva ble bestemt?
**Begrunnelse**: Hvorfor?
**Alternativer vurdert**: Hva var alternativene?
**Konsekvenser**: Hva betyr dette for systemet?
**Status**: [Aktiv/Erstattet/Deprecated]
```

---

## [2025-12-02] Multi-agent arkitektur for Saghaugen

**Kontekst**: Ronny hadde én agent (react-ha) og så behov for flere agenter med spesifikke ansvarsområder. Trengte en struktur for å koordinere flere agenter uten at det blir kaos.

**Beslutning**: Implementere multi-agent arkitektur med:
- Filbasert struktur (`agents/`, `coordination/`, `shared/`, `infrastructure/`)
- JSON-basert kommunikasjon via felles filer
- Git-workflow med agent-spesifikke branches
- General AI som CTO/koordinator

**Begrunnelse**:
- Filbasert er enkelt å debugge (ingen kompleks infra nødvendig)
- Git gir versjonskontroll og sporbarhet
- JSON schemas gir struktur uten å være for rigid
- Skalerer til 10-20 agenter før det blir komplekst

**Alternativer vurdert**:
1. **Message queue (MQTT/RabbitMQ)**: For komplekst for hobby-prosjekt, krever ekstra infrastruktur
2. **Database (PostgreSQL)**: Overkill, trenger ikke transaksjonalitet
3. **API-basert**: Krever at agenter kjører som services, ikke fleksibelt nok
4. **Shared Git repo (valgt)**: Enkelt, versjonert, fungerer offline

**Konsekvenser**:
- Agenter må pulle/pushe til Git for å kommunisere
- Merge conflicts kan oppstå hvis flere agenter endrer samme fil
- Historikk bevares automatisk via Git
- Fungerer selv uten nettverkstilgang (viktig på Saghaugen med Starlink)

**Status**: Aktiv

---

## [2025-12-02] React-HA beholder Windows 10 VM (foreløpig)

**Kontekst**: React-HA kjører i VS Code terminal på Windows 10 VM. Kunne vurdert å migrere til Linux LXC.

**Beslutning**: Beholde Windows 10 VM som det er, i hvert fall til etter HP EliteDesk Proxmox migrering er ferdig.

**Begrunnelse**:
- React-HA fungerer allerede
- Har passwordless SSH til alle systemer
- Ikke noe breaking som må fikses akkurat nå
- Minimere antall samtidige endringer (HP EliteDesk migrering kommer snart)

**Alternativer vurdert**:
1. **Migrere til Linux LXC nå**: Risiko for å breake eksisterende workflow midt i annen migrering
2. **Beholde Windows (valgt)**: Trygt, fungerer
3. **Hybrid (WSL)**: Unødvendig kompleksitet

**Konsekvenser**:
- Windows VM bruker mer ressurser enn LXC ville gjort
- Men det er OK siden det er midlertidig host uansett
- Kan revurdere etter HP EliteDesk migrering

**Status**: Aktiv (revurder etter Q1 2026)

---

## Template for fremtidige beslutninger

Bruk formatet over når du dokumenterer nye tekniske beslutninger.

Viktige beslutninger å dokumentere:
- Infrastruktur-endringer (nye VM/LXC)
- Breaking changes i APIer/protokoller
- Endringer i agent-ansvarsområder
- Valg av teknologier (hvorfor X over Y)
- Sikkerhetsbeslutninger
