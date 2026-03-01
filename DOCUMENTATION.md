[Version francaise](DOCUMENTATION-fr.md)

# ET5410 Web Controller — Technical Documentation

## Overview

Web control interface for the **ET5410** programmable DC electronic load (Hangzhou Zhongchuang Electronics). Single-file application (`index.html`) communicating via the SCPI protocol over USB serial port.

**Supported hardware:**
- ET5410 (150V / 40A / 400W)
- ET5411 (150V / 15A / 150W)
- ET5420 (150V / 20A / 200W)

**Main features:**
- 12 load modes (CC, CV, CP, CR, CC+CV, CR+CV, Tran, List, Scan, Short, Battery, LED)
- Real-time measurements with graph (V, A, W, R)
- Battery discharge test with graph, statistics, auto-stop on cutoff and exports
- MPPT search (linear scan + dichotomy) with graph and exports
- Configuration save/load (.ET5410)
- Direct SCPI console (Terminal)
- Qualification, protections, device file management

## Architecture

```
index.html          Single file: embedded HTML + CSS + JS
                    Zero external dependencies
                    Open directly via file:// or local server
```

The application relies on the **Web Serial API** (Chrome 89+ / Edge 89+) to communicate with the device via a virtual USB serial port.

### Design principles

- **Single file**: all code is in `index.html` (~2700 lines)
- **Sticky header**: header and tab navigation stay fixed at the top while content scrolls
- **Dark theme**: suited for measurement instruments
- **Sequential polling**: `while` loops with `await` (no `setInterval` to avoid serial command overlap)
- **SYST:LOCA guard**: prevents sending the local return command during active tests

## Prerequisites

| Prerequisite | Detail |
|---|---|
| Browser | Chrome 89+ or Edge 89+ (Web Serial API) |
| Cable | USB to the ET5410 device |
| Driver | USB serial driver (auto-installed on Windows 10/11) |

## File Structure

```
ET5410A-electronique-load/
  index.html                    Web application (single file)
  CLAUDE.md                     Project instructions for Claude Code
  DOCUMENTATION.md              This file (EN)
  DOCUMENTATION-fr.md           Technical documentation (FR)
  USER_MANUAL.md                User manual (EN)
  USER_MANUAL-fr.md             User manual (FR)
  datasheet/
    ET5410SCPI.pdf              Manufacturer SCPI documentation (45 pages)
    ET5410SCPI.txt              Corrected and augmented SCPI reference
  data/
    *.ET5410                    Saved configuration files
  scpi_scan.py                  SCPI brute-force scan script
  scan_batt_curr.py             Battery command search script
  scan_cutoff_mode.py           Cutoff mode search script
  scan_cutoff_type.py           Cutoff type search script
```

## SCPI Protocol

### Serial parameters

| Parameter | Value |
|---|---|
| Interface | USB (virtual serial port) |
| Baud rates | 7200, 9600, 14400 (depending on model) |
| Data bits | 8 |
| Stop bits | 1 |
| Parity | None |
| Terminator | `0x0A` (LF) |

### Response format

- **Numeric values**: `R` prefix followed by the value
  - Examples: `R0.60`, `R 2.307`, `R155.00`
- **Text/enum values**: no prefix
  - Examples: `CC`, `ON`, `HIGH`, `NONE`, `PASS`
- **MEAS:ALL?**: `R <current> <voltage> <power> <resistance>` (space-separated)
  - Example: `R 1.234 12.345 15.23 10.00`
- **Errors**: `cmd err` or `Rcmd err` (unknown command)

### Code parsing

```javascript
// Strip R prefix
function stripPrefix(r) {
  const s = r.trim();
  if (/^R\s*[-.\d]/.test(s)) return s.substring(1).trim();
  return s;
}

// Parse MEAS:ALL?
const cleaned = r.replace(/^[A-Za-z]\s+/, '');
const parts = cleaned.trim().split(/\s+/).map(s => parseFloat(s));
const [current, voltage, power, resistance] = parts;
```

## Load Modes

| Mode | SCPI Value | Value Command | Description |
|---|---|---|---|
| CC | `CC` | `CURR:CC <n>` | Constant current |
| CV | `CV` | `VOLT:CV <n>` | Constant voltage |
| CP | `CP` | `POWE:CP <n>` | Constant power |
| CR | `CR` | `RESI:CR <n>` | Constant resistance |
| CC+CV | `CCCV` | `CURR:CCCV`, `VOLT:CCCV` | 2-stage current then voltage |
| CR+CV | `CRCV` | `RESI:CRCV`, `VOLT:CRCV` | 2-stage resistance then voltage |
| Tran | `TRAN` | `TRAN:MODE`, `CURR:TA/TB`, etc. | Dynamic/transient test |
| List | `LIST` | `LIST:MODE`, `LIST:NUM`, etc. | Multi-step profile (50 max) |
| Scan | `SCAN` | `SCAN:TYPE`, `CURR:STARt/END`, etc. | Current/voltage/power sweep |
| Short | `SHOR` | — | Short circuit |
| Battery | `BATT` | `BATT:MODE`, `VOLT:BCC1`, etc. | Battery discharge test |
| LED | `LED` | `CURR:LED`, `VOLT:LED`, `LED:COEFf` | LED test |

## Discovered SCPI Commands (undocumented)

These commands were found by brute-force scanning and are not in the manufacturer documentation:

| Command | Subsystem | Description | Example Response |
|---|---|---|---|
| `BATT:BTC <n>` / `?` | BATT | Capacity cutoff (Ah) | `R10.000` |
| `BATT:BTE <n>` / `?` | BATT | Energy cutoff (Wh) | `R50.000` |
| `TIME:BTT <n>` / `?` | TIME | Time cutoff (seconds) | `R600` |
| `BATT:ENER?` | BATT | Discharged energy (Wh, read-only) | `R136.032` |
| `CURR:BCC <n>` / `?` | CURR | CC current for non-voltage cutoff | `R1.000` |

**Naming pattern**: `BT` = **B**attery **T**est + first letter (**C**apacity, **E**nergy, **T**ime).

**Limitation**: the cutoff mode selector (Voltage/Capacity/Energy/Time) has no corresponding SCPI command. It can only be changed from the device front panel.

## JavaScript Architecture

### ET5410 Class

```
class ET5410 {
  connect(baudRate)     Opens the serial port via Web Serial API
  disconnect()          Sends SYST:LOCA then closes the port
  send(cmd)             Sends a command without waiting for a response
  query(cmd)            Sends a command and waits for the response
}
```

### Polling system

Three independent polling systems coexist:

| System | Control Variable | Loop Function | Usage |
|---|---|---|---|
| Control (live) | `ctrlLiveTimer` / `ctrlLivePollId` | `ctrlLivePollLoop()` | Live measurements when load ON |
| Battery | `battTimer` / `battPollId` | `battPollLoop()` | Battery discharge test (auto-stop via `CH:SW?`) |
| Measurements | `measTimer` | `setInterval(measPoll)` | Independent Measurements tab |
| MPPT | `mpptTimer` / `mpptPollId` | `mpptPollLoop()` / `mpptDichoLoop()` | Maximum power point search |

**Anti-duplicate pattern** (control and battery):
```javascript
async function xxxPollLoop(myId) {
  while (xxxTimer && xxxPollId === myId) {
    const t0 = Date.now();
    await xxxPoll();
    const elapsed = Date.now() - t0;
    if (xxxTimer && xxxPollId === myId) {
      await new Promise(r => setTimeout(r, Math.max(0, interval - elapsed)));
    }
  }
}
```

### pcSession management

`pcSession` prevents sending `SYST:LOCA` between each command (which would cause the device screen to flicker).

```javascript
// Guard in send() and query()
if (!pcSession && !battTimer && !ctrlLiveTimer && !cmd.startsWith('SYST:LOCA')) {
  await sendLocalReturn();
}
```

**Coordination**: each polling system sets `pcSession = true` at startup and only resets it to `false` when the other two are inactive.

### Battery auto-stop

At the end of each `battPoll()` cycle, the application queries `CH:SW?` to check whether the device has automatically turned off the load (cutoff reached). If the response is `OFF`, `battStop(false)` is called (without sending an OFF command, since the device already did it) and a green "COMPLETED" label is displayed.

### Comma decimal separator

All `<input type="number">` fields accept both period and comma as decimal separator. A `keydown` listener intercepts the comma key and inserts a period at the cursor position via `document.execCommand('insertText')`.

### Heartbeat keepalive

A heartbeat system prevents USB idle disconnection (observed after ~30 min of inactivity on Chrome Web Serial).

- `heartbeatStart()` launches a `setInterval` every **30 seconds**
- `heartbeatPoll()` checks whether a polling system is already active (`battTimer || ctrlLiveTimer || measTimer || mpptTimer`); if so, their traffic serves as keepalive and no extra command is sent
- Otherwise, sends `*IDN?` (lightweight query, no side-effect on the device)
- After 2 consecutive timeouts, triggers `onDeviceLost()`

**Device-lost detection** uses three sources:
1. **Port `disconnect` event** — Chrome detects USB removal
2. **Read-loop error** — `_startReader()` catch block when `_reading` is `true`
3. **Heartbeat double timeout** — 2 failed `*IDN?` queries in a row

`onDeviceLost()` stops all pollers and the heartbeat, closes the port, and displays `Connection lost — replug USB and click Connect`. No automatic reconnection is attempted because the COM port disappears from the OS and requires a physical USB replug.

### Battery measurement averaging

Each `battPoll()` cycle performs **3 consecutive `MEAS:ALL?` queries** (50 ms apart) and averages voltage (V) and power (P) before storing the data point. This reduces measurement noise at the source while adding only ~100 ms per cycle (well within the 1-second polling interval).

### Battery graph smoothing

When zooming out, more data points map to fewer pixels, which amplifies visual noise. The graph drawing applies an **adaptive moving average** at render time (raw data is preserved):

```
smoothW = ceil(visible_points / pixel_width)
```

| Zoom | Points | smoothW | Effect |
|------|--------|---------|--------|
| 10 min | ~600 | 1 | No smoothing (raw data) |
| 2 h | ~7200 | ~10 | Moderate smoothing |
| 8 h | ~28800 | ~41 | Strong smoothing |

Combined with **pixel downsampling** (only one point drawn per pixel column), this eliminates the sub-pixel zigzag artifacts that made the curve appear increasingly noisy at wider zoom levels.

## MPPT (Maximum Power Point Tracking)

### Architecture

The MPPT system uses a shared helper `mpptMeasureAt(current)` reused by both modes:

```javascript
async function mpptMeasureAt(current) {
  // 1. Sends CURR:CC <current>
  // 2. Waits for the configured delay (mppt-delay or mppt-dicho-delay)
  // 3. Reads MEAS:ALL? → [ci, v, p, r]
  // 4. Records the point in mpptData (with measured ci)
  // 5. Updates mpptBest if p > best power
  // 6. Redraws the graph
  // 7. Returns { v, p } or { v, p, lowV: true } if v < Vmin, or null on error
}
```

### Linear scan mode

`mpptPollLoop(myId)` → `mpptPoll()` → `mpptMeasureAt(mpptCurrentI)`

Simple loop: measures at current value, increments `mpptCurrentI` by `iStep`, stops when `mpptCurrentI > iMax` or `v < vMin`.

### Dichotomy mode (ternary search)

`mpptDichoLoop(myId)` → `mpptMeasureAt(m1)`, `mpptMeasureAt(m2)`

```
Algorithm:
  lo = iStart, hi = iMax
  While (hi - lo) > tolerance:
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    Measure P at m1 and m2
    If V < Vmin at m1 → hi = m1 (current too high)
    If V < Vmin at m2 → hi = m2 (current too high)
    If P(m1) < P(m2) → lo = m1
    Else → hi = m2
  Final measurement at (lo + hi) / 2
```

Typical convergence: ~10-15 measurements (instead of hundreds for the scan).

### Graph

- **Scan mode**: linear curves connecting points (yellow voltage, orange power)
- **Dichotomy mode**: scatter plot (circles r=4), fixed X axis [iStart, iMax]
- **MPP point**: green circle (r=6) + label + dashed vertical line (common to both modes)

### V < Vmin handling in dichotomy

When `mpptMeasureAt` detects `v < vMin`, it returns `{ v, p, lowV: true }` instead of `null`. The dichotomy loop then reduces `hi` (upper bound) instead of stopping, which refocuses the search toward lower currents.

## Configuration Files (.ET5410)

### Format

Text file with `key=value` pairs, `#` comments:

```
# ET5410 Configuration
# Date: 2026-02-27 14:30:00
# Mode: CC

ctrl-mode=CC

# System
ctrl-vmax=60
ctrl-imax=40
ctrl-pmax=400
ctrl-offdelay=0
ctrl-vrange=HIGH
ctrl-crange=HIGH
ctrl-trig=MAN

# CC
ctrl-cc-val=1.500
```

### Saved content

- **Always**: mode, system parameters (limits, ranges, trigger, off delay)
- **Per mode**: only the parameters specific to the selected mode
- **MPPT**: MPPT parameters + mode (scan/dicho) + system parameters
- **Suggested name**: `-ET5410-YYYY-MM-DD-MODE.ET5410` (the leading dash lets the user prefix their name)

## Exports

### Battery test

| Format | Content | Extension |
|---|---|---|
| TXT | Tab-separated data (time, voltage) | `.txt` |
| CSV | Semicolon-separated data (European convention) | `.csv` |
| SVG | Vector graph (grid + curve + labels) | `.svg` |
| PNG | Stats + graph image | `.png` |
| PDF | Full report (parameters, results, statistics, graph, table) | via print |

### Graph theme

The battery graph supports two themes:

| Theme | Background | Grid | Voltage curve | Cursor |
|---|---|---|---|---|
| Dark | `#000000` | `#333333` | `#ff5252` | `rgba(255,255,255,0.4)` |
| Light | `#ffffff` | `#cccccc` | `#d32f2f` | `rgba(0,0,0,0.3)` |

The PDF is always generated in light theme for printing.
