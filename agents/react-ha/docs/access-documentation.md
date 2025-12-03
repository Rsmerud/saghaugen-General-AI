# SECRETS LOCATION GUIDE

**VIKTIG**: Denne filen inneholder IKKE selve secretsene, kun HVOR de ligger og hva som må håndteres.

**Generert**: 2025-12-03
**Formål**: Guide for General AI når han trenger å håndtere credentials, tokens og passord

---

## ⚠️ GENERELL SIKKERHETSPOLICY

**ALDRI commit secrets til Git!**

Følgende filer/mapper skal være i `.gitignore`:
- `.env`
- `secrets.yaml`
- `*_cred.json`
- `*.key`
- `*.pem`

---

## 🔐 HOME ASSISTANT SECRETS

### secrets.yaml (HA Prod)

**Lokasjon**: `/config/secrets.yaml` på HA Prod (10.12.0.20)

**Innhold** (eksempel, ikke faktiske verdier):
```yaml
# Home Assistant secrets.yaml
mqtt_broker_password: "passord_her"
mqtt_broker_username: "homeassistant"
ha_external_url: "https://saghaugen.no"
# ... andre secrets
```

**Tilgang**: SSH til HA Prod, deretter `cat /config/secrets.yaml`

**Backup**: Må inkluderes i backup-rutine (ikke i Git!)

**Fornying**: Ved endring av MQTT passord, må secrets.yaml oppdateres og HA restartes

---

### Long-lived Access Tokens

**Hvor de genereres**: HA Web UI → Profile → Security → Long-Lived Access Tokens

**Aktive tokens** (må kartlegges):
- `Homepage Dashboard` (expires 2078) - brukes av Homepage widget
- `React Dashboard` (navn ukjent) - brukes i `.env` som `VITE_HA_API_KEY`
- Mulig flere tokens for integrasjoner

**Hvor de brukes**:
- React dashboard: `.env` fil i repo-root (gitignored)
- Homepage: Docker Compose env variable `HOMEPAGE_VAR_HA_TOKEN`
- Node-RED: Flow credentials (encrypted i `flows_cred.json`)
- API-calls: Bearer token i Authorization header

**Fornying**:
1. Generer ny token i HA UI
2. Oppdater alle steder som bruker den gamle
3. Restart services som trenger ny token
4. Revoke gammel token i HA UI

---

## 🔑 SSH-NØKLER

### Oversikt over SSH-nøkler

| Nøkkel | Lokasjon | Brukt for | Passphrase? |
|--------|----------|-----------|-------------|
| `id_ed25519` | `~/.ssh/id_ed25519` | Proxmox root | ❌ Nei |
| `id_ed25519_ha` | `~/.ssh/id_ed25519_ha` | Home Assistant | ❌ Nei |
| `id_ed25519.pub` | `~/.ssh/id_ed25519.pub` | Public key for Proxmox | N/A |
| `id_ed25519_ha.pub` | `~/.ssh/id_ed25519_ha.pub` | Public key for HA | N/A |

### SSH Config

**Lokasjon**: `~/.ssh/config`

**Innhold**:
```bash
# Home Assistant passwordless SSH
Host homeassistant 10.12.0.20
    HostName 10.12.0.20
    User homeassistant
    IdentityFile ~/.ssh/id_ed25519_ha
    IdentitiesOnly yes

# Proxmox passwordless SSH
Host proxmox 10.12.0.205
    HostName 10.12.0.205
    User root
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

### Hvor public keys er installert

**Proxmox (10.12.0.205)**:
- `/root/.ssh/authorized_keys`
- Key: `id_ed25519.pub`

**Home Assistant (10.12.0.20)**:
- `/home/homeassistant/.ssh/authorized_keys`
- Key: `id_ed25519_ha.pub`

**Fornying** (hvis nødvendig):
1. Generer ny nøkkel: `ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new`
2. Kopier til server: `ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@host`
3. Test: `ssh -i ~/.ssh/id_ed25519_new user@host`
4. Oppdater `~/.ssh/config`
5. Slett gammel nøkkel

---

## 📡 MQTT CREDENTIALS

### EMQX Broker (10.12.0.22)

**Web GUI**: http://10.12.0.22:18083
**Default admin**: admin/public (MÅ ENDRES!)

**Brukere** (må verifiseres via EMQX GUI):

| User | Passord | Superuser | Brukes av |
|------|---------|-----------|-----------|
| `homeassistant` | ❓ Ukjent | Ja? | Home Assistant |
| `Zigbee2MQTT_hus` | Zigbee2024! | Ja? | Zigbee2MQTT (Hus) |
| `Zigbee2MQTT_garasje` | Zigbee2024! | Ja? | Zigbee2MQTT (Garasje) |
| `ZWave_hus` | Zigbee2024! | Ja? | Z-Wave JS UI (Hus) |
| `ZWave_garasje` | ❓ Må opprettes | Nei | Z-Wave JS UI (Garasje) |

**Hvor de er konfigurert**:
- **Home Assistant**: `/config/configuration.yaml` (mqtt section) eller secrets.yaml
- **Zigbee2MQTT**: `/opt/zigbee2mqtt/data/configuration.yaml` (LXC 110)
- **Z-Wave JS UI**: Docker Compose env variables (LXC 112)
- **Node-RED**: MQTT node credentials (encrypted)

**Fornying**:
1. Endre passord i EMQX Web GUI
2. Oppdater konfig på alle services som bruker den brukeren
3. Restart services

---

## 🐘 PROXMOX CREDENTIALS

### Root login

**User**: root
**Passord**: `4pn44SJAg`

**⚠️ PROBLEM**: Dette passordet er hardkodet mange steder!
- SSH manuell login (hvis ikke bruker nøkkel)
- Mulig i scripts?

**ANBEFALING**: Roter passord og bruk KUN SSH-nøkler!

### Proxmox API Token

**Token ID**: `root@pam!homepage`
**Secret**: Lagret i Homepage Docker Compose env variable

**Generering** (hvis ny trengs):
1. Proxmox GUI → Datacenter → Permissions → API Tokens
2. Add → root@pam → Token ID (f.eks. "homepage")
3. Copy secret (vises kun én gang!)
4. Oppdater `HOMEPAGE_VAR_PROXMOX_PASS` i Docker Compose

---

## 📄 PAPERLESS-NGX CREDENTIALS

### Web UI

**URL**: http://10.12.0.102:8000
**Admin user**: ❓ Ukjent (må sjekkes)
**Passord**: ❓ Ukjent

**Lokasjon**: Lagret i Paperless database (SQLite eller PostgreSQL?)

### Email IMAP

**Email**: paperless@saghaugen.no
**IMAP Server**: imap.domeneshop.no:993 (SSL)
**User**: saghaugen3
**Passord**: ❓ Ukjent (Domeneshop mailbox passord)

**Konfigurasjon**: `/opt/paperless/docker-compose.yml` eller environment file

**Fornying**:
1. Endre passord i Domeneshop mailbox UI
2. Oppdater Paperless config
3. Restart paperless-consumer service

---

## 🔧 CHIRPSTACK CREDENTIALS

### Web GUI

**URL**: http://10.12.0.40:8080
**Default admin**: admin / admin

**⚠️ ANBEFALING**: Endre default passord!

### PostgreSQL Database

**Database**: chirpstack
**User**: chirpstack
**Passord**: ❓ Ukjent (satt ved installasjon)

**Konfigurasjon**: `/etc/chirpstack/chirpstack.toml`

```toml
[database]
dsn = "postgres://chirpstack:PASSORD_HER@localhost/chirpstack?sslmode=disable"
```

### API Secret

**Hvor**: `/etc/chirpstack/chirpstack.toml`

```toml
[api]
secret = "BASE64_GENERERT_SECRET"
```

**Generering**: `openssl rand -base64 32`

---

## 📊 GRAFANA CREDENTIALS

### Web UI

**URL**: http://10.12.0.108:3000
**Default admin**: admin / admin

**⚠️ MÅ VERIFISERES**: Passord endret ved første login?

### InfluxDB Connection

**URL**: http://UKJENT_IP:8086
**Database**: ❓ (f.eks. "homeassistant")
**User**: ❓
**Passord**: ❓

**Konfigurasjon**: Grafana datasource settings (UI eller provisioning YAML)

---

## 🐳 DOCKER/PORTAINER CREDENTIALS

### Portainer Web UI

**URL**: https://10.12.0.50:9443
**Admin user**: ❓ (opprettet ved første setup)
**Passord**: ❓

**Fornying**: Via Portainer UI → Users → admin → Change password

---

## 🌐 CLOUDFLARE TUNNEL

**Domene**: saghaugen.no
**Cloudflare Account**: Ronnys Cloudflare-konto (epost ukjent)

**Tunnel credentials**: Lagret på server som kjører Cloudflare Tunnel (hvor?)

**Fornying**: Via Cloudflare Zero Trust dashboard

---

## 📱 HOME ASSISTANT MOBILE APP

**OAuth Tokens**: Generert automatisk ved login i HA mobile app

**Revoke**: HA Web UI → Profile → Security → Refresh Tokens (scroll ned)

---

## 🔄 CREDENTIALS SOM MÅ FORNYES PERIODISK

| Credential | Frekvens | Sist fornyet | Neste forny |
|------------|----------|--------------|-------------|
| HA Long-lived tokens | ❌ Aldri (expire langt frem) | Ukjent | N/A |
| EMQX admin passord | 🟡 Årlig | Aldri? | ASAP |
| Proxmox root passord | 🟡 Årlig | Ukjent | ASAP |
| ChirpStack admin passord | 🟡 Årlig | Aldri? | ASAP |
| Grafana admin passord | 🟡 Årlig | Ukjent | ASAP |
| Paperless admin passord | 🟡 Årlig | Ukjent | ASAP |
| SSH-nøkler | 🟢 Kun ved kompromittering | 2025 | N/A |

---

## 🚨 HVIS SECRETS BLIR KOMPROMITTERT

### Umiddelbare tiltak

1. **Identifiser hva som er lekket**
   - Passord? Token? SSH-nøkkel?
   - Hvilket system?

2. **Revoke/endre umiddelbart**
   - HA tokens: Revoke i HA UI
   - MQTT passord: Endre i EMQX
   - SSH-nøkler: Fjern fra authorized_keys, generer nye
   - Proxmox passord: `passwd` kommando

3. **Oppdater alle steder som bruker secretet**
   - Sjekk denne filen for hvor secretet brukes
   - Oppdater config-filer
   - Restart services

4. **Audit logs**
   - Sjekk HA logs: `/config/home-assistant.log`
   - Sjekk Proxmox audit log
   - Sjekk EMQX connection logs

5. **Dokumenter incident**
   - Hva skjedde?
   - Hva ble gjort?
   - Hvordan forhindre i fremtiden?

---

## 📝 SECRETS CHECKLIST FOR NYE SYSTEMER

Når General AI setter opp nye systemer:

- [ ] Generer sterke passord (ikke hardcode!)
- [ ] Dokumenter hvor credentials ligger (ikke verdiene!)
- [ ] Legg secrets i `.gitignore`
- [ ] Bruk environment variables eller secrets manager
- [ ] Endre default passord (admin/admin, root/root, etc.)
- [ ] Sett opp backup av credentials (encrypted!)
- [ ] Dokumenter fornying-prosedyre

---

**Sluttnot**: Denne filen må oppdateres hver gang nye credentials opprettes eller endres. Selve verdiene skal ALDRI committes til Git!

**Ved behov for faktiske passord**: Spør Ronny eller sjekk fysisk server/konfig-filer.

**Sist oppdatert**: 2025-12-03
