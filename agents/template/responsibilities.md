# Agent Responsibilities

## Hva denne agenten SKAL gjøre

### Primært ansvar
- [Konkret ansvar 1]
- [Konkret ansvar 2]

### Sekundært ansvar
- [Mindre kritiske oppgaver]

## Hva denne agenten IKKE skal gjøre

- [Ting som er andre agenters ansvar]
- [Ting som krever General AI godkjenning]

## Systemer denne agenten eier

### System 1: [Navn]
- **Lokasjon**: [VM/LXC/fysisk server]
- **Tilgang**: [SSH/API/annet]
- **Kritisk**: [Ja/Nei]
- **Backup**: [Hvordan/hvor ofte]

### System 2: [Navn]
[samme som over]

## Protokoller/APIer denne agenten håndterer

- [Protokoll 1, f.eks. "KNX IP Interface"]
- [Protokoll 2, f.eks. "MQTT topics under homeassistant/*"]

## Filsystem-eierskap

### Mapper denne agenten eier:
- `agents/<agent-navn>/` - Full kontroll
- [Andre mapper hvis relevant]

### Mapper denne agenten kan lese (men ikke skrive):
- `shared/configs/` - Read-only
- `shared/schemas/` - Read-only

### Mapper denne agenten kan skrive til:
- `coordination/status/<agent-navn>.json` - Kun sin egen status
- `coordination/tasks/in-progress/` - Når den tar en task
- `coordination/tasks/completed/` - Når den fullfører en task

## Beslutninger agenten kan ta selv

- [Type beslutning 1 som ikke trenger godkjenning]
- [Type beslutning 2 som ikke trenger godkjenning]

## Beslutninger som krever General AI godkjenning

- Endringer i `shared/`
- Endringer som påvirker andre agenter
- Infrastruktur-endringer (nye VM/LXC)
- Breaking changes i APIer/protokoller

## Eskalering

Hvis agenten møter på noe den ikke kan løse:
1. Opprett task i `coordination/tasks/pending/` tagged med `general-ai`
2. Beskriv problemet og foreslåtte løsninger
3. Vent på General AI review

## SLA (Service Level Agreement)

- **Responstid**: [Hvor fort agenten skal reagere på tasks]
- **Oppetid**: [Forventet oppetid for systemer agenten eier]
- **Monitoring**: [Hva som monitoreres og hvor]
