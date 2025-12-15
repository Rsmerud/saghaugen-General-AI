# Voice Assistant Hardware

**Oppdatert:** 2025-12-15
**Status:** Konfigurert og klar

---

## Raspberry Pi Compute Module 4

| Egenskap | Verdi |
|----------|-------|
| **Modell** | Raspberry Pi CM4 Rev 1.1 |
| **RAM** | 8 GB |
| **Storage** | 32 GB eMMC |
| **OS** | Debian GNU/Linux 12 (Bookworm) 64-bit |
| **Kernel** | 6.12.47+rpt-rpi-v8 aarch64 |
| **Hostname** | hei-general |
| **IP** | 10.12.0.198 (eth0), 10.12.0.199 (WiFi) |
| **Bruker** | ronny |
| **SSH** | Passwordless fra General AI ✅ |

---

## Waveshare Compute Module 4 PoE 4G Board

**Produkt:** [Waveshare CM4 PoE 4G Board](https://www.waveshare.com/compute-module-4-poe-4g-board.htm)
**Wiki:** [Dokumentasjon](https://www.waveshare.com/wiki/Compute_Module_4_PoE_4G_Board)

### Hovedfunksjoner

| Feature | Spesifikasjon |
|---------|---------------|
| **PoE** | 802.3af standard, Gigabit Ethernet |
| **4G/5G** | M.2 B KEY slot for mobilmoduler |
| **Video** | Dual HDMI (4K@30fps hver) |
| **USB** | 2x USB 2.0 (deaktivert default!) |
| **Driftstemperatur** | -25°C til 80°C |

### Industrielle Grensesnitt

| Interface | Detaljer | Bruksområde |
|-----------|----------|-------------|
| **RS485** | Isolert, half-duplex | Industrielle sensorer |
| **RS232** | Isolert | Seriell kommunikasjon |
| **CAN** | Isolert, MCP2515 | Bilsystemer, industri |
| **GPIO** | Isolert (17, 27 ut / 23, 24 inn) | Digital I/O |
| **I2C** | Isolert (I2C1, GPIO2/3) | Sensorer |
| **ADC** | 12-bit ADS1113, ±2.048V | Analog inngang |

### Hjelpefunksjoner

| Funksjon | GPIO/Detaljer |
|----------|---------------|
| **Buzzer** | GPIO22 (aktiv lav) |
| **LED Grønn** | GPIO20 (aktiv lav) |
| **LED Rød** | GPIO21 (aktiv lav) |
| **RTC** | PCF85063A på I2C10 |
| **SIM-kort** | Nano-SIM slot |

---

## Strømforsyning

⚠️ **VIKTIG:** CM4 trenger minimum 12V 2A for stabil drift!

| Kilde | Spenning | Notat |
|-------|----------|-------|
| **DC-inngang** | 7-36V | Bred spenningsrange |
| **PoE** | 802.3af | Må aktiveres med jumper |
| **USB-C** | KUN for flashing | Ikke strømforsyning! |

---

## Konfigurasjon påkrevd

### Aktivere USB 2.0
USB er deaktivert som standard. Legg til i `/boot/firmware/config.txt`:
```
dtoverlay=dwc2,dr_mode=host
```

### Aktivere RS485 (UART3)
```
dtoverlay=uart3
```

### Aktivere RS232 (UART5)
```
dtoverlay=uart5
```

### Aktivere CAN
```
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
```

---

## Tilkoblinger for Voice Assistant

### Yealink MSpeech (USB)
- Kobles til USB 2.0 port
- Krever `dtoverlay=dwc2,dr_mode=host` aktivert
- Fungerer som standard USB lydkort

### Fremtidige muligheter

Med dette boardet har vi mulighet for:
- **4G backup** - Internett via mobilnett hvis fiber/WiFi feiler
- **RS485 sensorer** - Industrielle sensorer i låve/garasje
- **CAN-bus** - Hvis vi noen gang får elbil med V2H
- **Buzzer** - Lydlig feedback uten ekstern høyttaler
- **LED** - Visuell status-indikator

---

## Nettverkskonfigurasjon

```
eth0:  10.12.0.198 (PoE, primær)
wlan0: 10.12.0.199 (WiFi, backup)
```

### Statisk IP (anbefalt)
Sett statisk IP i `/etc/dhcpcd.conf`:
```
interface eth0
static ip_address=10.12.0.198/24
static routers=10.12.0.1
static domain_name_servers=10.12.0.1
```

---

## Referanser

- [Waveshare Wiki](https://www.waveshare.com/wiki/Compute_Module_4_PoE_4G_Board)
- [Waveshare Manual](https://www.waveshare.com/wiki/Compute_Module_PoE_4G_Board_manual)
- [Raspberry Pi CM4 Datasheet](https://datasheets.raspberrypi.com/cm4/cm4-datasheet.pdf)
