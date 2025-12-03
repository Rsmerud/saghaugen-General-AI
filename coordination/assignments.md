# Aktive Assignments

Dette dokumentet holder oversikt over hvilke agenter som jobber med hva AKKURAT NÅ.

**Format:**
```
## [Agent Navn]
**Status**: [Idle/Working/Blocked]
**Nåværende oppgave**: [Kort beskrivelse]
**Startet**: [Timestamp]
**Forventet ferdig**: [Timestamp eller "ukjent"]
**Avhengigheter**: [Hva venter agenten på, hvis blocked]
```

---

## Pris-Sjekker
**Status**: Idle
**Nåværende oppgave**: Ingen
**Siste oppgave**: Låve-vegg materialer (fullført 2025-12-03 10:30)
**Resultat**: Se coordination/findings/pris-sjekker/2025-12-03-laave-vegg-materialer.md
**Avhengigheter**: N/A

---

## React-HA
**Status**: Operational (ikke tilgjengelig for General AI enda)
**Nåværende oppgave**: Vedlikeholder eksisterende infrastruktur
**Startet**: N/A (løpende)
**Forventet ferdig**: N/A (løpende)
**Avhengigheter**: Møte med General AI for koordinering kommer snart

---

## General AI (meg)
**Status**: Idle
**Nåværende oppgave**: Ingen - venter på neste oppgave fra Ronny
**Siste oppgave**: Koordinert pris-sjekk for låve-vegg (fullført 2025-12-03 10:30)
**Resultat**: Presentert anbefaling til Ronny
**Avhengigheter**: N/A

---

## Template for nye assignments

Når en ny agent får en oppgave, legg til:

```
## [Agent Navn]
**Status**: Working
**Nåværende oppgave**: [Konkret oppgave]
**Startet**: [Timestamp]
**Forventet ferdig**: [Estimat eller "ukjent"]
**Avhengigheter**: [Blokkerende faktorer, hvis noen]
```

Når oppgaven er ferdig, flytt informasjonen til `coordination/findings/` og sett agenten tilbake til Idle.
