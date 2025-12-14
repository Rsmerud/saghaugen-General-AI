# USB/IP Gateway - RPi3 B+ Setup

**Opprettet**: 2025-12-14
**Status**: Under arbeid
**Formål**: Eksponere Zigbee og Z-Wave USB-dongler over nettverk til Proxmox LXC-er

---

## Hardware

| Komponent | Detaljer |
|-----------|----------|
| **Gateway** | Raspberry Pi 3 B+ |
| **Hostname** | usb-ip-1 |
| **WiFi IP** | 10.12.0.188 |
| **Kabel IP** | TBD (DHCP fungerer ikke ennå) |
| **Bruker** | ronny / 4pn44SJAg |
| **SSH** | Passwordless fra General AI ✅ |

### USB-enheter tilkoblet

| Enhet | USB ID | Symlink | Device |
|-------|--------|---------|--------|
| **Nabu Casa ZBT-2** (Zigbee) | 303a:831a | `usb-Nabu_Casa_ZBT-2_9C139EACFF0C-if00` | /dev/ttyACM0 |
| **Nabu Casa ZWA-2** (Z-Wave) | 303a:4001 | `usb-Nabu_Casa_ZWA-2_80B54EE5AFB8-if00` | /dev/ttyACM1 |

---

## Mål-arkitektur

```
┌─────────────────┐     USB/IP      ┌─────────────────┐
│  RPi3 B+ (usb-ip-1)              │  Proxmox Host   │
│  10.12.0.188    │ ─────────────► │  10.12.0.205    │
│                 │                 │                 │
│  ┌───────────┐  │                 │  ┌───────────┐  │
│  │ ZBT-2     │  │                 │  │ LXC 111   │  │
│  │ (Zigbee)  │──┼─────────────────┼─►│ zigbee2mqtt│  │
│  └───────────┘  │                 │  │ -garasje  │  │
│                 │                 │  └───────────┘  │
│  ┌───────────┐  │                 │  ┌───────────┐  │
│  │ ZWA-2     │  │                 │  │ LXC 113   │  │
│  │ (Z-Wave)  │──┼─────────────────┼─►│ zwave-js  │  │
│  └───────────┘  │                 │  │ -garasje  │  │
└─────────────────┘                 └───────────────┘
```

---

## Status per 2025-12-14

- [x] RPi3 reinstallert med Raspberry Pi OS Lite
- [x] SSH passwordless konfigurert
- [x] USB-enheter tilkoblet og synlige
- [x] Symlinks fungerer
- [ ] eth0 kabel-IP (DHCP svarer ikke - sjekk switch/port)
- [ ] USB/IP installert på RPi3
- [ ] USB/IP server konfigurert
- [ ] USB/IP client på Proxmox
- [ ] Enheter bundet til LXC 111 og 113

---

## Implementeringsplan

### Steg 1: Fikse nettverk (Ronny)
eth0 får bare link-local IP (169.254.x.x). Mulige årsaker:
- Kabel ikke i DHCP-aktivert port
- Feil VLAN
- Kabel-problem

**Anbefaling**: Bruk statisk IP på eth0 for stabilitet:
```bash
# I /etc/dhcpcd.conf:
interface eth0
static ip_address=10.12.0.188/24
static routers=10.12.0.1
static domain_name_servers=10.12.0.1
```

### Steg 2: Installere USB/IP på RPi3
```bash
sudo apt update
sudo apt install linux-tools-generic usbip hwdata
sudo modprobe usbip_host
echo "usbip_host" | sudo tee /etc/modules-load.d/usbip.conf
```

### Steg 3: Konfigurere USB/IP server
Lag systemd service for usbipd:
```bash
# /etc/systemd/system/usbipd.service
[Unit]
Description=USB/IP Host Daemon
After=network.target

[Service]
Type=forking
ExecStart=/usr/sbin/usbipd -D
ExecStartPost=/bin/sleep 1
ExecStartPost=/usr/sbin/usbip bind -b 1-1.2  # ZBT-2
ExecStartPost=/usr/sbin/usbip bind -b 1-1.4  # ZWA-2 (busid må verifiseres)

[Install]
WantedBy=multi-user.target
```

### Steg 4: USB/IP client på Proxmox
```bash
# På Proxmox host (10.12.0.205):
apt install linux-tools-$(uname -r) hwdata
modprobe vhci-hcd
echo "vhci-hcd" >> /etc/modules-load.d/usbip.conf

# Attach enheter:
usbip attach -r 10.12.0.188 -b 1-1.2  # ZBT-2
usbip attach -r 10.12.0.188 -b 1-1.4  # ZWA-2
```

### Steg 5: Passthrough til LXC
```bash
# I /etc/pve/lxc/111.conf (zigbee2mqtt-garasje):
lxc.cgroup2.devices.allow: c 166:* rwm
lxc.mount.entry: /dev/ttyACM0 dev/ttyACM0 none bind,optional,create=file

# I /etc/pve/lxc/113.conf (zwave-js-ui-garasje):
lxc.cgroup2.devices.allow: c 166:* rwm
lxc.mount.entry: /dev/ttyACM1 dev/ttyACM1 none bind,optional,create=file
```

---

## Notater

- **RPi4 er reservert** til tale-assistent prosjekt (ikke bruk den til dette)
- **Ingen failover** - garasje-automatisering er nice-to-have
- Bus IDs (`1-1.2`, `1-1.4`) må verifiseres med `usbip list -l` før binding

---

## Oppdateringslogg

| Dato | Endring |
|------|---------|
| 2025-12-14 | Opprettet plan. USB-enheter bekreftet. USB/IP ikke installert ennå. |
