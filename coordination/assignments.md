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
**Startet**: N/A
**Forventet ferdig**: N/A
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
**Status**: Working
**Nåværende oppgave**: Sette opp multi-agent strukturen, teste pris-sjekker
**Startet**: 2025-12-03 09:00
**Forventet ferdig**: 2025-12-03 12:00 (første test kjørt)
**Avhengigheter**: Ronny må be om et faktisk produktsøk for testing

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
