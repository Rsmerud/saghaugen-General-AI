# Migrering fra LXC150 til Windows VM

## STATUS: ✅ FULLFØRT (2025-12-11)

General AI kjører nå på Windows 11 VM (10.12.0.183).

---

## Hvorfor migrering var nødvendig
- Playwright funket ikke i upriviligert LXC
- GUI-apps (Sweet Home 3D etc.) krevde hacks for å fungere
- Windows VM gir enklere fildeling, RDP, og alt "bare funker"

## Hva som ble gjort

### 1. Repoer clonet ✅
```
C:\ClaudeCodeProjects\GeneralAI
C:\ClaudeCodeProjects\saghaugen-infopanel
```

### 2. Playwright installert ✅
- Chromium 143.0
- Firefox 144.0
- WebKit 26.0
- FFMPEG

### 3. SSH-nøkkel generert ✅
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKgSqskliWgmAQCaRShoiJSgpv4fcs79MKS0VHl87Anr general-ai-win11@saghaugen.no
```
Lagt til på Proxmox (10.12.0.205).

### 4. Filserver satt opp ✅
- **URL:** http://10.12.0.183:8888
- **Mapper:**
  - `C:\ClaudeCodeProjects\GeneralAI\fildeling\fra_ronny\`
  - `C:\ClaudeCodeProjects\GeneralAI\fildeling\til_ronny\`
- **Autostart:** Task Scheduler `SaghaugenFileserver`

### 5. Claude Code autostart ✅
- **Task:** `ClaudeCodeGeneralAI`
- **Trigger:** Ved brukerinnlogging
- **Working directory:** `C:\ClaudeCodeProjects\GeneralAI`

## Filer opprettet under migrering

| Fil | Formål |
|-----|--------|
| `services/autostart/setup-autostart.ps1` | PowerShell-script for Task Scheduler oppsett |
| `services/fileserver/install-service.ps1` | Alternativt script for Windows Service (krever admin) |

## Nettverksinfo

| Type | IP |
|------|-----|
| LAN | 10.12.0.183 |
| ZeroTier | 10.144.151.76 |

## Gjenstår

### React-HA agent
- Status ukjent etter migrering
- Var på LXC150 - må avklares om den skal flyttes hit eller kjøre et annet sted

### LXC150
- Kan nå slettes eller gjenbrukes til noe annet
- Alle viktige ting er migrert

---

**Migrert av:** General AI
**Dato:** 2025-12-11
