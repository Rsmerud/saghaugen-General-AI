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

## [2025-12-05] Koordineringsmodell mellom General AI og React-HA

**Kontekst**: Forsøkte å etablere direkte kommunikasjon mellom General AI og React-HA. Oppdaget at React-HA ikke har persistent hukommelse mellom samtaler - starter fra scratch hver gang og leser CLAUDE.md for kontekst.

**Beslutning**: Etablere asynkron koordinering via filer med Ronny som formidler:
- **General AI** = CTO/koordinator med persistent minne (via filer)
- **React-HA** = Implementør uten persistent minne (leser CLAUDE.md)
- **Ronny** = Formidler mellom agenter + beslutningstaker

**Arbeidsfordeling CLAUDE.md:**
- React-HA oppdaterer sin egen CLAUDE.md med React/HA/dashboard-spesifikk info
- General AI oppdaterer `infrastructure/current-setup.md` med Saghaugen-wide info
- Briefings til React-HA legges i `agents/react-ha/briefings/`

**Begrunnelse**:
- React-HA har ikke persistent tilstand - kan ikke huske mellom samtaler
- Filbasert koordinering fungerer med denne begrensningen
- Ronny slipper å være "RAM" - General AI tar den rollen
- Klart skille mellom ansvar reduserer forvirring

**Alternativer vurdert**:
1. **Direkte agent-til-agent kommunikasjon**: Ikke mulig uten persistent minne
2. **General AI oppdaterer alt**: For sentralisert, React-HA kjenner sine detaljer best
3. **Hybrid (valgt)**: Hver agent eier sin dokumentasjon, General AI koordinerer

**Konsekvenser**:
- React-HA må lese briefings-mappen for oppdateringer fra General AI
- Ronny formidler verbale beskjeder mellom agenter
- Git-historikk viser hvem som endret hva
- Skalerer til flere agenter med samme modell

**Status**: Aktiv

---

## [2025-12-03] GitHub integration for General AI

**Kontekst**: General AI trengte tilgang til GitHub for å kunne pushe/pulle, opprette issues, bygge wiki, og generelt fungere som en ordentlig CTO-agent.

**Beslutning**: Sette opp SSH keys for General AI og gi tilgang til GitHub repo.

**Implementasjon**:
- Generert ed25519 SSH key pair for `general-ai@saghaugen.no`
- Public key lagt til på GitHub under Ronny's account
- GitHub repo opprettet: `github.com/Rsmerud/saghaugen-General-AI`
- Remote konfigurert og første push fullført

**Begrunnelse**:
- General AI må kunne committe/pushe autonomt
- Issues og wiki på GitHub gir bedre oversikt enn bare lokale filer
- GitHub blir single source of truth for alle agenter
- PR workflow muliggjør review av agent-endringer

**Alternativer vurdert**:
1. **Lokal Git kun**: Fungerer, men ingen remote backup eller synk mellom agenter
2. **Self-hosted GitLab/Gitea**: Overkill for hobbyprosjekt, krever vedlikehold
3. **GitHub (valgt)**: Gratis, pålitelig, alle kjenner det

**Konsekvenser**:
- General AI kan nå pushe endringer direkte til GitHub
- Historikk bevares og er tilgjengelig fra hvor som helst
- React-HA og fremtidige agenter kan også få GitHub-tilgang
- Wiki kan brukes for mer omfattende dokumentasjon

**Neste steg**:
- Sette opp GitHub Issues templates
- Bygge Wiki for detaljert dokumentasjon
- Vurdere GitHub Projects for task tracking
- Gi React-HA tilgang når han migreres

**Status**: Aktiv

---

## [2025-12-03] MCP Servere installert for General AI

**Kontekst**: General AI trengte MCP (Model Context Protocol) servere for utvidede capabilities som browser-automasjon, oppdatert dokumentasjon og filesystem-tilgang.

**Beslutning**: Installere Context7, Playwright og Filesystem MCP servere med user scope.

**Implementasjon**:
```bash
# Context7 - Up-to-date dokumentasjon
claude mcp add context7 -s user -- npx -y @upstash/context7-mcp@latest

# Playwright - Browser-automasjon
claude mcp add playwright -s user -- npx @playwright/mcp@latest

# Filesystem - Filoperasjoner
claude mcp add filesystem -s user -- npx -y @modelcontextprotocol/server-filesystem /home/ronny
```

**Installerte servere**:
1. **Context7** - Dynamisk henter oppdatert dokumentasjon
2. **Playwright** - Browser-automasjon via accessibility tree
3. **Filesystem** - Les/skriv filer i /home/ronny på tvers av prosjekter

**Scope**: User-level - tilgjengelig i alle Claude Code prosjekter

**Verifisert**: Alle servere ✓ Connected

**Begrunnelse**:
- Context7: Alltid oppdatert dokumentasjon
- Playwright: Web scraping for pris-sjekker, testing
- Filesystem: Les/skriv på tvers av prosjekter

**Konsekvenser**:
- General AI kan nå automatisere browser-oppgaver
- Får alltid oppdatert dokumentasjon
- Kan jobbe med filer utenfor CWD

**Status**: Aktiv

---

## [2025-12-03] Subagents får IKKE tilgang til MCP servere (kjent bug)

**Kontekst**: Testet om pris-sjekker subagent kunne bruke Playwright MCP server for web scraping. Installerte både user-scoped og project-scoped MCP servere.

**Funn**: Pris-sjekker rapporterte eksplisitt: "Playwright - IKKE TILGJENGELIG i min verktøyliste"

**Root cause**: GitHub Issue #7296 - Task-spawnet subagents arver IKKE MCP servere fra parent agent, hverken user-scoped eller project-scoped.

**Beslutning**: Accept current limitation - bruk WebSearch/WebFetch som primary tools for pris-sjekker.

**Begrunnelse**:
- **WebSearch + WebFetch fungerer forbløffende bra**: Test-kjøring fant priser hos 5 butikker, lagerstatus, kontaktinfo
- **Playwright trengs sjeldent**: Kun for JavaScript-tunge sider eller kompleks navigasjon
- **Parent agent kan hjelpe**: Hvis subagent feiler, kan General AI (parent) kjøre Playwright og sende data tilbake
- **Fremtidssikret**: Når Anthropic fikser buggen, får subagents automatisk tilgang

**Test-resultater** (48x198mm treverk, 15 stk x 3m):
- Fant priser hos: Obs BYGG Olrud, Byggmax, Montér Stange, Maxbo, Byggmakker
- Beste pris: ~2.002 kr (Obs BYGG Olrud ubehandlet)
- Fullstendig data: priser, lagerstatus, telefon, åpningstider, URLs

**Alternativer vurdert**:
1. **Parent agent kjører Playwright alltid**: Overkill, WebSearch/WebFetch holder
2. **Blokkere på bug-fix**: Unødvendig, fungerer godt uten
3. **Accept limitation (valgt)**: WebSearch/WebFetch primary, Playwright future

**Konsekvenser**:
- Pris-sjekker agent er fullt operativ UTEN Playwright
- Noen JavaScript-tunge sider kan feile (f.eks. Byggmax produktsider)
- Workaround: Parent agent (General AI) kan kjøre Playwright ved behov
- Når bug fikses: Automatisk upgrade til Playwright-support

**Workflow**:
1. Pris-sjekker bruker WebSearch + WebFetch (rask, fungerer 90% av tiden)
2. Hvis spesifikke sider feiler, rapporterer tilbake til General AI
3. General AI kan kjøre Playwright for problematiske sider (manuelt)
4. Fremtid: Automatisk Playwright-tilgang når Anthropic fikser bug #7296

**Status**: Aktiv - monitoring Anthropic releases for bug-fix

---

## Template for fremtidige beslutninger

Bruk formatet over når du dokumenterer nye tekniske beslutninger.

Viktige beslutninger å dokumentere:
- Infrastruktur-endringer (nye VM/LXC)
- Breaking changes i APIer/protokoller
- Endringer i agent-ansvarsområder
- Valg av teknologier (hvorfor X over Y)
- Sikkerhetsbeslutninger
