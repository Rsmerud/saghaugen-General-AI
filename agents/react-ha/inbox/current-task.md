# Oppgave fra General AI

**Dato**: 2025-12-05
**Prioritet**: Normal
**Status**: UTFØRT

---

## Oppgave

General AI vil teste React dashboardet med Playwright. Trenger tilkoblingsdetaljer:

1. **URL til dashboardet** - Kjører det på dev-server? Hvilken port?
2. **Er det noe autentisering?** - Trenger jeg token/passord?
3. **Kjører dashboardet nå?** - Hvis ikke, hvordan starter jeg det?
4. **Noen spesielle ting å teste?** - Moduler som er ferdig vs. under utvikling?

---

## Når du er ferdig

Oppdater denne filen:
- Sett **Status**: UTFØRT
- Fyll ut svarene under "Resultat"

---

## Resultat

### 1. URL til dashboardet
- **Dev-server**: `http://localhost:5173` (Vite default)
- **Prosjektmappe**: `/home/ronny/ClaudeCodeProjects/saghaugen-infopanel/ha-dashboard/`

### 2. Autentisering
- **Dashboard selv**: Ingen autentisering (åpent)
- **Home Assistant API**: Krever `VITE_HA_API_KEY` i `.env`-fil
- **MERK**: `.env`-fil mangler! Må opprettes med HA token for at API-kall skal fungere
- Token genereres i HA: Profil → Long-Lived Access Tokens → CREATE TOKEN

### 3. Hvordan starte dashboardet
```bash
cd /home/ronny/ClaudeCodeProjects/saghaugen-infopanel/ha-dashboard
npm install  # Første gang
npm run dev  # Starter på http://localhost:5173
```

**OBS**: Trenger `.env`-fil i ha-dashboard/:
```
VITE_HA_API_KEY=ditt_home_assistant_token_her
```

### 4. Hva kan testes

**Ferdig (✅) - Bør teste:**
| Modul | Test-fokus |
|-------|-----------|
| 2D Floorplan | SVG-rendering, klikk på lyskilder |
| Vær | Forecast-popup, temperaturvisning |
| Alarm | Keypad-input, status-visning |
| Scene | Scene-aktivering |
| Media | Play/pause, volum-slider |
| Kamera | Live stream, fullscreen |

**Venter (🔄) - Begrenset testing:**
| Modul | Notater |
|-------|---------|
| Energi | Mangler hardware - vil vise placeholder/feil |

**Ikke startet (❌):**
| Modul | Notater |
|-------|---------|
| Kalender | Ikke implementert |

### 5. Viktige filer for testing
- `src/components/FloorPlan.tsx` - Hovedkomponent
- `src/components/*Module.tsx` - Alle moduler
- `src/services/homeAssistant.ts` - API-lag

### 6. Kjente begrensninger
- **Uten HA-tilkobling**: Moduler vil vise loading/error states
- **Mock-data**: Finnes ikke - ekte HA kreves for full testing
- **3D-modus**: Fungerer ikke over RDP (WebGL-limitasjon)
