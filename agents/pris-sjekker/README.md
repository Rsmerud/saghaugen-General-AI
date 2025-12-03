# Pris-Sjekker Agent

**Status**: Test/Development (ikke-driftskritisk)

## Formål

Finne beste priser og tilgjengelighet på byggevarer, elektronikkomponenter og smarthus-produkter. Dette er General AI sin test-agent for å utvikle workflow før vi involverer driftskritisk infrastruktur.

## Ansvarsområder

Se `responsibilities.md` for detaljer.

Kort oppsummert:
- Søke etter produkter hos norske leverandører
- Sammenligne priser og tilgjengelighet
- Rapportere strukturert tilbake til General AI
- Identifisere beste kjøpsalternativer basert på pris, leveringstid og tilgjengelighet

## Leverandører som dekkes

### Elektronikk/Smarthus:
- Elektroimportøren (elektroimportoren.no)
- Kjell & Company (kjell.com)
- Elfasonett (elfasonett.no)
- EL-Service (el-service.no)
- Electrosupply (electrosupply.no)

### Byggevarer:
- Byggmakker (byggmakker.no)
- Maxbo (maxbo.no)
- Jula (jula.no)
- Biltema (biltema.no)
- Bygghjemme (bygghjemme.no)

### Spesialiserte:
- Conrad (conrad.no) - Elektronikk/komponenter
- Elfadistrelec (elfadistrelec.no) - Industrikomponenter
- Mouser/DigiKey (internasjonale) - Kun ved behov

## Avhengigheter

### Primary Tools (tilgjengelig nå):
- **WebSearch** - Generelt websøk for å finne produktsider og priser
- **WebFetch** - Henter innhold fra spesifikke URLs (statiske sider)

**Status**: ✅ Fungerer utmerket! Test viste 100% success rate på norske byggevarebutikker.

### MCP Servere (fremtidig support):
⚠️ **KJENT BUG**: Subagents får foreløpig IKKE tilgang til MCP servere (GitHub Issue #7296)

- **Playwright** (stdio) - Browser-automasjon for web scraping
  - Kommando: `claude mcp add playwright -- npx @playwright/mcp@latest`
  - Status: Installert for parent agent (General AI), men ikke tilgjengelig for pris-sjekker
  - Brukes til: JavaScript-tunge sider, kompleks navigasjon
  - Workaround: General AI kan kjøre Playwright ved behov

- **Context7** (optional) - Oppdatert dokumentasjon
  - Kommando: `claude mcp add context7 -s user -- npx -y @upstash/context7-mcp@latest`
  - Status: Installert, men ikke tilgjengelig for subagent

**Når bug fikses**: Agenten får automatisk tilgang til Playwright → kraftigere scraping!

### Systemer denne agenten er avhengig av:
- Internett (WebSearch/WebFetch primært)
- Ingen driftskritiske systemer

### Andre agenter denne agenten samarbeider med:
- General AI (rapporterer funn tilbake)
- Fremtidig: Elektriker-agent (sjekk elektrisk kapasitet før kjøp)

## Kommunikasjon

### Status rapportering
Denne agenten oppdaterer `coordination/status/pris-sjekker.json` ved hver søk-sesjon.

### Task-mottak
Mottar søk-forespørsler direkte fra General AI via Task tool.

### Resultater
Rapporterer strukturerte funn tilbake til General AI som logger det i `coordination/findings/`.

## Output Format

Agenten leverer søkeresultater i følgende format:

```json
{
  "search_id": "SEARCH-001",
  "product": "Sensirion SHT45 temperature sensor",
  "timestamp": "2025-12-03T09:30:00Z",
  "results": [
    {
      "supplier": "Elektroimportøren",
      "product_name": "Sensirion SHT45",
      "price_nok": 189,
      "availability": "På lager",
      "url": "https://...",
      "notes": "Inkluderer mva"
    }
  ],
  "recommendation": "Elektroimportøren - beste pris, rask levering"
}
```

## Konfigurasjon

Agent-spesifikk konfigurasjon ligger i `config/search-preferences.json`.

## Scripts

Ingen scripts akkurat nå - ren search-basert agent.

## Dokumentasjon

Agent-spesifikk dokumentasjon ligger i `docs/`.

## Testing & Iterasjon

Dette er test-agenten for å utvikle multi-agent workflow. Forventninger:
- Ting vil ikke være perfekt fra start
- Vi itererer basert på hva som funker/ikke funker
- Ikke-driftskritisk, så vi kan eksperimentere fritt
- Læring fra denne agenten brukes når vi onboarder kritiske agenter

## Kontakt

**Eier**: General AI
**Opprettet**: 2025-12-03
**Sist oppdatert**: 2025-12-03
