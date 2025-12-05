# Migrering fra LXC150 til Windows VM

## Hvorfor migrere?
- Playwright funker ikke i upriviligert LXC
- GUI-apps (Sweet Home 3D etc.) krever hacks for å fungere
- Windows VM gir enklere fildeling, RDP, og alt "bare funker"

## Agenter som skal migreres

### 1. General AI (denne instansen)
- **Repo:** `/home/ronny/ClaudeCodeProjects/GeneralAI`
- **GitHub:** Sørg for alt er pushet før migrering

### 2. React-HA (kollega)
- **Repo:** Finn lokasjon og sørg for alt er pushet
- **Notater:** Sjekk om det er noe som ikke er i git

## Tjenester som kjører på LXC150

### Saghaugen Filserver
- **Service:** `saghaugen-fileserver.service`
- **Port:** 8888
- **Beslutning:** Trenger vi denne på Windows? Sannsynligvis ikke - kan bruke delt mappe i stedet

## Før migrering - SJEKKLISTE

### Git status for begge repoer:
- [ ] `GeneralAI`: Commit og push alle endringer
- [ ] `React-HA`: Commit og push alle endringer

### Filer som IKKE er i git:
- [ ] `/home/ronny/ClaudeCodeProjects/GeneralAI/fildeling/` - Kopier viktige filer
- [ ] Sjekk for andre lokale filer

### SSH-nøkler:
- [ ] Dokumenter hvilke nøkler som brukes
- [ ] Sett opp på nytt i Windows VM (eller kopier)

### Tjenester å stoppe:
- [ ] `sudo systemctl stop saghaugen-fileserver`
- [ ] `sudo systemctl disable saghaugen-fileserver`

## På Windows VM - OPPSETT

### 1. Installer nødvendig programvare:
- [ ] VS Code
- [ ] Node.js (for Claude Code)
- [ ] Git
- [ ] Claude Code (`npm install -g @anthropic-ai/claude-code` eller tilsvarende)

### 2. Clone repoer:
```powershell
cd C:\Users\<bruker>\ClaudeCodeProjects
git clone <GeneralAI-repo-url>
git clone <React-HA-repo-url>
```

### 3. SSH-oppsett:
- [ ] Generer eller kopier SSH-nøkler
- [ ] Sett opp `~/.ssh/config` for enkel tilgang til Proxmox og LXC-er

### 4. Test Playwright:
```powershell
npx playwright install
npx playwright test  # eller bare test at browseren starter
```

### 5. Verifiser tilgang:
- [ ] SSH til Proxmox
- [ ] SSH til HomeAssistant LXC
- [ ] SSH til andre relevante VM/LXC

## Etter migrering

### Oppdater CLAUDE.md:
- Endre info om at vi kjører på Windows VM, ikke LXC150
- Fjern LXC150-problemseksjonen
- Oppdater filserver-info (eller fjern hvis vi bruker delt mappe)

### Vurder hva som skal skje med LXC150:
- [ ] Beholde som backup?
- [ ] Slette?
- [ ] Bruke til noe annet?

## Notater
- Filserveren (`http://10.12.0.145:8888`) blir borte når LXC150 stoppes
- Husk å laste ned eventuelle filer fra `/fildeling/` først!
