# USB/IP Gateway - RPi3 B+ Setup

**Opprettet**: 2025-12-14
**Status**: ✅ FERDIG - Alt fungerer!
**Formål**: Eksponere Zigbee og Z-Wave USB-dongler over nettverk til Proxmox LXC-er

---

## Hardware

| Komponent | Detaljer |
|-----------|----------|
| **Gateway** | Raspberry Pi 3 B+ |
| **Hostname** | usb-ip-1 |
| **WiFi IP** | 10.12.0.188 (backup) |
| **Kabel IP** | 10.12.0.132 (statisk, primær) |
| **Bruker** | ronny / 4pn44SJAg |
| **SSH** | Passwordless fra General AI ✅ |

### USB-enheter tilkoblet

| Enhet | USB ID | Bus ID | Symlink |
|-------|--------|--------|---------|
| **Nabu Casa ZBT-2** (Zigbee) | 303a:831a | 1-1.3 | `usb-Nabu_Casa_ZBT-2_9C139EACFF0C-if00` |
| **Nabu Casa ZWA-2** (Z-Wave) | 303a:4001 | 1-1.1.2 | `usb-Nabu_Casa_ZWA-2_80B54EE5AFB8-if00` |

---

## Arkitektur (IMPLEMENTERT)

```
┌─────────────────┐     USB/IP      ┌─────────────────┐
│  RPi3 B+ (usb-ip-1)   :3240      │  Proxmox Host   │
│  10.12.0.132    │ ─────────────► │  10.12.0.205    │
│                 │                 │                 │
│  ┌───────────┐  │                 │  ┌───────────┐  │
│  │ ZBT-2     │  │                 │  │ LXC 111   │  │
│  │ (Zigbee)  │──┼─────────────────┼─►│ zigbee2mqtt│  │
│  │ 1-1.3     │  │                 │  │ :8082     │  │
│  └───────────┘  │                 │  └───────────┘  │
│                 │                 │                 │
│  ┌───────────┐  │                 │  ┌───────────┐  │
│  │ ZWA-2     │  │                 │  │ LXC 113   │  │
│  │ (Z-Wave)  │──┼─────────────────┼─►│ zwave-js  │  │
│  │ 1-1.1.2   │  │                 │  │ :8092     │  │
│  └───────────┘  │                 │  └───────────┘  │
└─────────────────┘                 └───────────────┘
```

---

## Status per 2025-12-14

- [x] RPi3 reinstallert med Raspberry Pi OS Lite (Debian Trixie)
- [x] SSH passwordless konfigurert
- [x] USB-enheter tilkoblet og synlige
- [x] Symlinks fungerer
- [x] eth0 kabel-IP: 10.12.0.132 (statisk via NetworkManager)
- [x] USB/IP installert på RPi3
- [x] USB/IP server konfigurert (systemd service)
- [x] USB/IP client på Proxmox (systemd service)
- [x] Enheter synlige i LXC 111 og 113
- [x] ZBT-2 firmware flashet til 7.4.4.6
- [x] ModemManager deaktivert på RPi3
- [x] Zigbee2MQTT kjører i LXC 111 ✅
- [x] Z-Wave JS UI kjører i LXC 113 ✅

---

## VIKTIG: ZBT-2 Konfigurasjons-krav

**Nabu Casa ZBT-2 krever spesifikke serieport-innstillinger:**

```yaml
serial:
  port: /dev/ttyZigbee
  adapter: ember
  baudrate: 460800    # KRITISK! Ikke 115200!
  rtscts: true        # KRITISK! Hardware flow control
```

⚠️ **Uten disse innstillingene vil ZBT-2 IKKE respondere!**

---

## Implementert konfigurasjon

### RPi3 (Server-side)

**Kernel-modul** (persistent):
```bash
# /etc/modules-load.d/usbip.conf
usbip_host
```

**Systemd service** (`/etc/systemd/system/usbipd.service`):
```ini
[Unit]
Description=USB/IP Host Daemon
After=network.target

[Service]
Type=forking
ExecStart=/usr/sbin/usbipd -D
ExecStartPost=/bin/sleep 2
ExecStartPost=/usr/sbin/usbip bind -b 1-1.3
ExecStartPost=/usr/sbin/usbip bind -b 1-1.1.2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**ModemManager deaktivert** (forstyrrer serieporter):
```bash
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager
sudo systemctl mask ModemManager
```

**Udev-regel** (`/etc/udev/rules.d/99-zigbee.rules`):
```
ATTRS{idVendor}=="303a", ENV{ID_MM_DEVICE_IGNORE}="1"
```

### Proxmox (Client-side)

**Kernel-modul** (persistent):
```bash
# /etc/modules-load.d/usbip-client.conf
vhci-hcd
```

**Systemd service** (`/etc/systemd/system/usbip-attach.service`):
```ini
[Unit]
Description=USB/IP Client - Attach Zigbee and Z-Wave from RPi3
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/sbin/modprobe vhci-hcd
ExecStartPre=/bin/sleep 10
ExecStart=/usr/sbin/usbip attach -r 10.12.0.132 -b 1-1.3
ExecStart=/usr/sbin/usbip attach -r 10.12.0.132 -b 1-1.1.2
ExecStop=/usr/sbin/usbip detach -p 0
ExecStop=/usr/sbin/usbip detach -p 1
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### LXC Passthrough

**LXC 111** (`/etc/pve/lxc/111.conf`):
```
# USB/IP passthrough for Zigbee (ZBT-2)
lxc.cgroup2.devices.allow: c 166:* rwm
lxc.mount.entry: /dev/serial/by-id/usb-Nabu_Casa_ZBT-2_9C139EACFF0C-if00 dev/ttyZigbee none bind,optional,create=file
```

**LXC 113** (`/etc/pve/lxc/113.conf`):
```
# USB/IP passthrough for Z-Wave (ZWA-2)
lxc.cgroup2.devices.allow: c 166:* rwm
lxc.mount.entry: /dev/serial/by-id/usb-Nabu_Casa_ZWA-2_80B54EE5AFB8-if00 dev/ttyZwave none bind,optional,create=file
```

### Zigbee2MQTT konfigurasjon (LXC 111)

`/opt/zigbee2mqtt/data/configuration.yaml`:
```yaml
homeassistant:
  enabled: true
mqtt:
  base_topic: zigbee2mqtt/garasje
  server: mqtt://10.12.0.22:1883
  user: Zigbee2MQTT_garasje
  password: Zigbee2024!
serial:
  port: /dev/ttyZigbee
  adapter: ember
  baudrate: 460800
  rtscts: true
frontend:
  enabled: true
  port: 8082
  host: 0.0.0.0
advanced:
  log_level: info
  channel: 20
```

---

## Verifisert funksjonalitet

```bash
# På LXC 111 (Zigbee):
journalctl -u zigbee2mqtt -n 5
# zh:ember:uart:ash: ======== ASH connected ========
# zh:ember:uart:ash: ======== ASH started ========
# z2m: Zigbee2MQTT started!

# På LXC 113 (Z-Wave):
docker logs zwave-js-ui-garasje --tail 5
# Z-WAVE: Driver is READY
# Z-WAVE: Controller status: Scan completed
```

---

## Feilsøking

### ZBT-2 svarer ikke (ASH timeout)

1. **Sjekk baudrate** - MÅ være 460800
2. **Sjekk rtscts** - MÅ være true
3. **ModemManager** - MÅ være deaktivert
4. **Firmware** - Flash med https://toolbox.openhomefoundation.org/home-assistant-connect-zbt-2/install/

### USB power-problemer på RPi3

- RPi3 USB-porter har begrenset strøm
- **Anbefalt**: Bruk powered USB hub
- Symptom: `device descriptor read/64, error -32` i dmesg

---

## Notater

- **RPi4 er reservert** til tale-assistent prosjekt
- **Ingen failover** - garasje-automatisering er nice-to-have
- **Kabel er primær** (10.12.0.132), WiFi (10.12.0.188) er backup
- **Powered USB hub anbefales** for stabilitet

---

## Gjenstående oppgaver

1. [x] ~~Fikse eth0 kabel-IP på RPi3~~ → 10.12.0.132 (statisk)
2. [ ] Teste reboot av hele stacken (RPi3 → Proxmox → LXC)
3. [x] ~~Konfigurere zigbee2mqtt i LXC 111~~ ✅
4. [x] ~~Konfigurere zwave-js-ui i LXC 113~~ ✅
5. [ ] Sette `onboot: 1` på LXC 111 og 113
6. [ ] Skaffe powered USB hub for stabilitet

---

## Oppdateringslogg

| Dato | Endring |
|------|---------|
| 2025-12-14 09:30 | Opprettet plan. USB-enheter bekreftet. |
| 2025-12-14 12:50 | USB/IP server ferdig på RPi3 (systemd service) |
| 2025-12-14 12:51 | USB/IP client ferdig på Proxmox (systemd service) |
| 2025-12-14 12:52 | LXC passthrough konfigurert og verifisert |
| 2025-12-14 13:05 | Kabel-IP fikset: 10.12.0.132 (statisk). Proxmox service oppdatert. |
| 2025-12-14 16:00 | ZBT-2 firmware flashet til 7.4.4.6. ModemManager deaktivert. |
| 2025-12-14 16:30 | **LØSNING FUNNET**: ZBT-2 krever baudrate 460800 + rtscts true! |
| 2025-12-14 16:45 | Begge dongles fungerer via USB/IP! Zigbee2MQTT og Z-Wave JS UI oppe. |
