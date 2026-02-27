# ET5410 Web Controller

Web-based controller for the **ET5410 / ET5411 / ET5420** programmable DC electronic load (Hangzhou Zhongchuang Electronics / East Tester). Single HTML file, zero dependencies — just open in Chrome and connect via USB.

## Features

- **12 load modes** — CC, CV, CP, CR, CC+CV, CR+CV, Dynamic, List (50 steps), Scan, Short, Battery, LED
- **Real-time measurements** — Voltage, Current, Power, Resistance with live graph
- **Battery discharge test** — Full test with voltage curve, statistics (min/max/avg), pause/resume, and multiple export formats (TXT, CSV, SVG, PNG, PDF report)
- **Save/Load configurations** — Export and import settings to `.ET5410` files
- **Qualification testing** — Pass/fail limit checking for V, I, P
- **SCPI terminal** — Direct command console for advanced use
- **System management** — Protections (OV/OC/OP), ranges, device file storage
- **Dark theme** — Designed for lab/bench use

## Supported Hardware

| Model | Voltage | Current | Power |
|-------|---------|---------|-------|
| ET5410 | 150V | 40A | 400W |
| ET5411 | 150V | 15A | 150W |
| ET5420 | 150V | 20A | 200W |

## Quick Start

### Requirements

- **Browser**: Chrome 89+ or Edge 89+ (Web Serial API required)
- **Cable**: USB to the ET5410 device
- **Driver**: USB serial driver (auto-installed on Windows 10/11)

### Usage

1. Open `index.html` in Chrome or Edge (double-click — no server needed)
2. Select the baud rate (default: 14400) and click **Connect**
3. Choose the serial port corresponding to the ET5410
4. The device identifier is displayed (e.g. `East Tester, ET5410A+, ...`)

> The application uses the [Web Serial API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API) and runs entirely in the browser via `file://` — no server, no install, no dependencies.

## Documentation

- **[User Manual](USER_MANUAL.md)** — Step-by-step usage guide (French)
- **[Technical Documentation](DOCUMENTATION.md)** — Architecture, SCPI protocol, JavaScript internals (French)
- **[SCPI Reference](datasheet/ET5410SCPI.txt)** — Complete command reference (corrected and augmented)

## SCPI Protocol

Communication uses SCPI commands over a virtual USB serial port.

| Parameter | Value |
|-----------|-------|
| Baud rates | 7200, 9600, 14400 |
| Data bits | 8 |
| Stop bits | 1 |
| Parity | None |
| Terminator | `0x0A` (LF) |

**Undocumented commands discovered** via brute-force scanning (see `scan_*.py` scripts):

| Command | Description |
|---------|-------------|
| `BATT:BTC` | Battery cutoff capacity (Ah) |
| `BATT:BTE` | Battery cutoff energy (Wh) |
| `TIME:BTT` | Battery cutoff time (seconds) |
| `BATT:ENER?` | Discharged energy readback (Wh) |
| `CURR:BCC` | Battery current for non-voltage cutoff (A) |

## Project Structure

```
index.html                  Single-file web application (HTML + CSS + JS)
DOCUMENTATION.md            Technical documentation
USER_MANUAL.md              User manual
datasheet/
  ET5410SCPI.pdf            Manufacturer SCPI documentation (45 pages)
  ET5410SCPI.txt            Corrected and augmented SCPI reference
data/
  *.ET5410                  Sample configuration files
scan_*.py                   SCPI brute-force discovery scripts
```

## License

This project is provided as-is for educational and personal use.
