# USB/IP Gateway - RPi3 B+ Setup

**Opprettet**: 2025-12-14
**Status**: ✅ FERDIG (kun eth0 kabel-IP gjenstår)
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
| **Nabu Casa ZBT-2** (Zigbee) | 303a:831a | 1-1.1.3 | `usb-Nabu_Casa_ZBT-2_9C139EACFF0C-if00` |
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
│  │ 1-1.1.3   │  │                 │  │ /dev/ttyZigbee│
│  └───────────┘  │                 │  └───────────┘  │
│                 │                 │                 │
│  ┌───────────┐  │                 │  ┌───────────┐  │
│  │ ZWA-2     │  │                 │  │ LXC 113   │  │
│  │ (Z-Wave)  │──┼─────────────────┼─►│ zwave-js  │  │
│  │ 1-1.1.2   │  │                 │  │ /dev/ttyZwave │
│  └───────────┘  │                 │  └───────────┘  │
└─────────────────┘                 └───────────────┘
```

---

## Status per 2025-12-14

- [x] RPi3 reinstallert med Raspberry Pi OS Lite
- [x] SSH passwordless konfigurert
- [x] USB-enheter tilkoblet og synlige
- [x] Symlinks fungerer
- [x] eth0 kabel-IP: 10.12.0.132 (statisk)
- [x] USB/IP installert på RPi3
- [x] USB/IP server konfigurert (systemd service)
- [x] USB/IP client på Proxmox (systemd service)
- [x] Enheter synlige i LXC 111 og 113

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
ExecStartPost=/usr/sbin/usbip bind -b 1-1.1.3
ExecStartPost=/usr/sbin/usbip bind -b 1-1.1.2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
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
Description=USB/IP Client - Attach remote devices
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/sbin/modprobe vhci-hcd
ExecStartPre=/bin/sleep 5
ExecStart=/usr/sbin/usbip attach -r 10.12.0.132 -b 1-1.1.3
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

---

## Verifisert funksjonalitet

```bash
# På LXC 111:
ls -la /dev/ttyZigbee
# crw-rw---- 1 nobody nogroup 166, 1 Dec 14 11:51 /dev/ttyZigbee

# På LXC 113:
ls -la /dev/ttyZwave
# crw-rw---- 1 root dialout 166, 2 Dec 14 11:51 /dev/ttyZwave
```

---

## Notater

- **RPi4 er reservert** til tale-assistent prosjekt
- **Ingen failover** - garasje-automatisering er nice-to-have
- **Kabel er primær** (10.12.0.132), WiFi (10.12.0.188) er backup
- **Reboot-test gjenstår** - verifiser at alt starter automatisk

---

## Gjenstående oppgaver

1. [x] ~~Fikse eth0 kabel-IP på RPi3~~ → 10.12.0.132 (statisk)
2. [ ] Teste reboot av hele stacken (RPi3 → Proxmox → LXC)
3. [ ] Konfigurere zigbee2mqtt i LXC 111
4. [ ] Konfigurere zwave-js-ui i LXC 113
5. [ ] Sette `onboot: 1` på LXC 111 og 113 når alt fungerer

---

## Oppdateringslogg

| Dato | Endring |
|------|---------|
| 2025-12-14 09:30 | Opprettet plan. USB-enheter bekreftet. |
| 2025-12-14 12:50 | USB/IP server ferdig på RPi3 (systemd service) |
| 2025-12-14 12:51 | USB/IP client ferdig på Proxmox (systemd service) |
| 2025-12-14 12:52 | LXC passthrough konfigurert og verifisert |
| 2025-12-14 13:05 | Kabel-IP fikset: 10.12.0.132 (statisk). Proxmox service oppdatert. |
