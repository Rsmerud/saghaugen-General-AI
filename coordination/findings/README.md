# Findings - Resultater fra Agenter

Denne mappen inneholder strukturerte resultater fra agenter som har fullført oppgaver.

## Struktur

Findings organiseres per agent og oppgave-type:

```
findings/
├── README.md (dette dokumentet)
├── pris-sjekker/
│   ├── 2025-12-03-sensirion-sht45.md
│   ├── 2025-12-04-knx-dimmer.md
│   └── ...
├── elektriker/ (fremtidig)
│   └── ...
└── react-ha/ (når integrert)
    └── ...
```

## Fil-navngivning

Format: `YYYY-MM-DD-produkt-eller-oppgave.md`

Eksempler:
- `2025-12-03-sensirion-sht45.md`
- `2025-12-10-bygg-gulvvarme-kabel.md`
- `2025-12-15-zigbee-sensor-sammenligning.md`

## Template for findings

```markdown
# [Oppgave tittel]

**Agent**: [Agent navn]
**Dato**: [YYYY-MM-DD]
**Oppgave-ID**: [TASK-XXX hvis relevant]

## Oppsummering

[1-3 setninger om hva som ble funnet]

## Resultater

[Strukturerte resultater - format avhenger av agent-type]

## Anbefaling

[Hva General AI anbefaler basert på disse funnene]

## Neste steg

[Hva bør skje nå? Venter vi på Ronny? Trengs mer research?]

## Metadata

- **Status**: [Fullført/Trenger oppfølging/Blokkert]
- **Relevant for**: [Hvilke prosjekter er dette relevant for]
- **Tags**: [søkeord for senere oppslag]
```

## Hvordan bruke findings

### For General AI:
- Når en agent rapporterer tilbake, lag en finding-fil
- Kryss-referér med decisions.md hvis det tas en beslutning
- Oppdater infrastructure/current-setup.md hvis relevant

### For Ronny:
- Findings er oppsummerte, lesbare rapporter
- Kan søke i findings/ for tidligere research
- Ser hele historikken av hva agenter har funnet

### For agenter:
- Les relevante findings før du starter en oppgave
- Unngå å gjøre samme research to ganger
- Referer til tidligere findings i dine rapporter

## Eksempler

Se `pris-sjekker/` for eksempler etter første test-kjøring er fullført.
