[Version francaise](USER_MANUAL-fr.md)

# ET5410 Web Controller — User Manual

## Quick Start

1. **Open** `index.html` in **Chrome** (89+) or **Edge** (89+)
2. **Connect** the ET5410 electronic load via USB cable
3. In the **Connection** tab, select the baud rate (14400 by default) and click **Connect**
4. The browser displays the list of serial ports: choose the ET5410 one
5. The device identifier is displayed (e.g. `East Tester, ET5410A+, ...`)

> **Note**: If the message "Web Serial API: NOT SUPPORTED" appears, use Chrome or Edge.

---

## Connection Tab

This tab manages communication with the device.

| Element | Description |
|---|---|
| **Baud Rate** | Communication speed (7200, 9600, 14400). Must match the device setting. |
| **Connect** | Opens the serial connection and reads the device configuration |
| **Disconnect** | Closes the connection and returns control to the front panel (`SYST:LOCA`) |
| **Identifier** | Displays the model, serial number and firmware after connection |

**Automatic keepalive**: the application sends a lightweight command (`*IDN?`) every 30 seconds to prevent USB idle disconnection. When a polling system (battery, measurements, MPPT, or live control) is active, its traffic serves as keepalive and no extra command is sent.

**Connection loss**: if the device becomes unreachable (USB cable unplugged, USB suspend), all active operations are stopped and the status shows `Connection lost — replug USB and click Connect`. Replug the USB cable and click **Connect** to resume.

---

## Control Tab

This is the main tab for operating the load.

### Select a load mode

12 modes available as radio buttons:

| Mode | Description |
|---|---|
| **CC** | Constant current — the load maintains a fixed current |
| **CV** | Constant voltage — the load maintains a fixed voltage |
| **CP** | Constant power |
| **CR** | Constant resistance |
| **CC+CV** | Two stages: constant current then constant voltage |
| **CR+CV** | Two stages: constant resistance then constant voltage |
| **Tran** | Dynamic test — alternating between two levels |
| **List** | Multi-step profile (up to 50 programmable steps) |
| **Scan** | Progressive sweep in current, voltage or power |
| **Short** | Short-circuit mode |
| **Battery** | Battery discharge test (see dedicated section) |
| **LED** | LED test with coefficient |

### Configure parameters

Depending on the selected mode, the corresponding parameter fields appear:

- **CC**: current value (A)
- **CV**: voltage value (V)
- **CP**: power value (W)
- **CR**: resistance value (Ohm)
- **CC+CV**: current (A) + voltage (V)
- **CR+CV**: resistance (Ohm) + voltage (V)
- **LED**: current (A), voltage (V), coefficient

Protection limits (Vmax, Imax, Pmax) and the off delay are also configurable.

### Enable / Disable the load

- Click **ON** to enable the load
- Click **OFF** to disable it

> **Important**: Changing mode automatically disables the load.

### Live measurements

When the load is enabled (ON), measurements are displayed in real time:

- **VOLTAGE** (yellow) — in Volts
- **CURRENT** (blue) — in Amps
- **POWER** (orange) — in Watts
- **RESISTANCE** (purple) — in Ohms (only for CR, CR+CV, List, LED modes)

A **graph** is drawn in real time below the values. You can:

- **Display**: choose the channel to plot (Voltage, Current, Power, Resistance)
- **Interval**: adjust the refresh rate (100 to 10000 ms)
- **Max points**: limit the number of displayed points (50 to 2000)
- **Clear**: reset the graph

---

## Save / Load a Configuration

### Save

1. Configure the desired mode and parameters
2. Click **Save config** (top right of the "Load Mode" card)
3. The file explorer opens with a suggested name: `-ET5410-2026-02-27-CC.ET5410`
4. **Add your name** before the dash (e.g. `MyTest-ET5410-2026-02-27-CC.ET5410`)
5. Choose the location and click Save

The saved file contains:
- The selected load mode
- System parameters (limits, ranges, trigger)
- Mode-specific parameters

### Load

1. Click **Load config**
2. Select a `.ET5410` file
3. The mode and all parameters are restored automatically

> **Note**: The file only contains the parameters of the mode that was selected at the time of saving.

---

## Battery Test

Battery mode allows running a complete battery discharge test with real-time monitoring.

### Configuration

1. Select the **Battery** mode in the Control tab
2. Choose the **discharge mode**:
   - **CC** (Constant Current) — discharge at fixed current
   - **CR** (Constant Resistance) — discharge at fixed resistance
3. Choose the **cutoff type**:
   - **Voltage** — stop when voltage reaches the threshold
   - **Capacity** — stop when discharged capacity reaches the threshold (Ah)
   - **Energy** — stop when discharged energy reaches the threshold (Wh)
   - **Time** — stop after a defined duration (hours, minutes, seconds)
4. Configure the **values**: cutoff voltage, current/resistance, thresholds

> **Warning**: The cutoff type (Voltage/Capacity/Energy/Time) must also be selected on the device front panel via the SET button. The application cannot change this setting via SCPI command.

### Test progress

| Button | Action |
|---|---|
| **Start** | Starts the test, enables the load, begins monitoring |
| **Pause** | Pauses the test (load OFF), preserves data. The "PAUSE" label blinks. |
| **Resume** | Resumes the test from where it stopped |
| **Stop** | Permanently stops the test, disables the load |
| **Reset** | Clears all data and the graph |

> **Auto-stop**: When the device reaches a cutoff condition (voltage, capacity, energy or time), the load turns off automatically. The application detects this and stops the test, displaying a green **COMPLETED** label. No manual Stop is needed.

### Displayed statistics

During the test, 6 indicators are updated in real time:

| Indicator | Description |
|---|---|
| **VOLTAGE** | Instantaneous battery voltage (V) |
| **SETPOINT** | Programmed current (A) or resistance (Ohm) |
| **POWER** | Instantaneous power (W) |
| **CAPACITY** | Cumulative discharged capacity (Ah) |
| **ENERGY** | Cumulative discharged energy (Wh) |
| **DURATION** | Elapsed time (HH:MM:SS) |

### Discharge graph

The graph displays the **voltage curve** over time. Each data point is the average of 3 consecutive readings (50 ms apart) to reduce measurement noise.

**Navigation:**
- **Zoom +** / **Zoom -**: zoom in (less time visible, more detail) or zoom out (more time visible)
- **Auto**: automatically adjusts the zoom to fit all data
- **Theme**: toggle between dark and light background

When zooming out, the curve is automatically smoothed using an adaptive moving average proportional to the zoom level. This prevents visual noise amplification when many data points are compressed into fewer pixels.

**Interactive tooltip**: hover over the graph with the mouse to see exact values (voltage + time) at the cursor position.

### Exports

| Button | Format | Content |
|---|---|---|
| **TXT** | Tab-separated text | Time (s) and Voltage (V) |
| **Excel** | Semicolon CSV | Time (s) and Voltage (V) — opens in Excel |
| **SVG** | Vector image | Full graph (grid, curve, labels) |
| **Image** | PNG | Statistics + graph |
| **PDF** | Printable report | Parameters, results, min/max/avg statistics, graph in light theme, data table |

---

## Measurements Tab

This tab provides independent measurement monitoring, unrelated to the load mode.

### Usage

1. Click **Start** to begin polling
2. The 4 values update continuously: Voltage, Current, Power, Resistance
3. Adjust the **interval** (ms) for the refresh rate
4. Click **Stop** to stop polling

### Graph

- **Display**: choose the channel to plot (Voltage, Current, Power, Resistance)
- **Max points**: maximum number of displayed points
- **Clear**: reset the graph

> **Note**: The Measurements tab can run simultaneously with the battery test or the Control live measurements.

---

## MPPT Tab

The MPPT tab allows finding the **Maximum Power Point** of a DC source (solar panel, generator) by sweeping the load current.

### Mode selection

Two search modes are available via radio buttons at the top of the configuration:

| Mode | Description |
|---|---|
| **Linear scan** | Sweeps current from start to max by fixed increments (step). Plots voltage and power curves. Exhaustive but slower. |
| **Dichotomy** | Ternary search that divides the interval into 3, compares power at the two thirds, and eliminates the least performing third. Converges in ~10-15 measurements. Displays points as scatter plot. |

### Configuration

The displayed fields depend on the selected mode:

**Linear scan mode:**

| Parameter | Description |
|---|---|
| **Start current (A)** | Initial sweep current |
| **Max current (A)** | End sweep current |
| **Step (A)** | Increment between each measurement |
| **Min voltage (V)** | Stop threshold if voltage drops below |
| **Delay between steps (ms)** | Wait time between each measurement |

**Dichotomy mode:**

| Parameter | Description |
|---|---|
| **Start current (A)** | Lower bound of the search interval |
| **Max current (A)** | Upper bound of the search interval |
| **Delay (ms)** | Wait time between each measurement (500 ms recommended) |

> **Note**: In dichotomy mode, the **Step** field (hidden) serves as convergence tolerance. The **Min voltage** field (hidden) remains active as a safety threshold.

### Progress

| Button | Action |
|---|---|
| **Start** | Launches the search: switches to CC mode, enables the load, begins measurements |
| **Stop** | Stops the current search and disables the load |
| **Reset** | Clears data and the graph |

### MPP Result

At the end of the search, the maximum power point is displayed:

- **MPP Current** (blue) — optimal current in Amps
- **MPP Voltage** (yellow) — voltage at the optimal point in Volts
- **MPP Power** (green) — maximum power in Watts
- **MPP Resistance** (purple) — equivalent resistance in Ohms

### Graph

The graph displays measurements in real time during the search:

- **Scan mode**: continuous curves (yellow = voltage, orange = power)
- **Dichotomy mode**: scatter plot (yellow circles = voltage, orange circles = power)
- **MPP point**: green circle with power label and dashed vertical line
- **Theme**: toggle between dark and light background

### Exports

| Button | Format | Content |
|---|---|---|
| **Export CSV** | Semicolon CSV | Current (A), Voltage (V), Power (W) |
| **Export PNG** | PNG image | Statistics + graph |

### Save / Load MPPT configuration

The **Save config** / **Load config** buttons at the top of the card save all MPPT parameters (mode, currents, delays) as well as system parameters in a `.ET5410` file.

> **Tip**: For a solar panel, start with a 500 ms delay. Shorter delays (100-200 ms) may produce inaccurate measurements if the source has parasitic capacitance.

---

## Qualification Tab

Allows testing whether measurements fall within defined limits.

### Configuration

1. Define the **limits** for each quantity:
   - Voltage: V High / V Low
   - Current: I High / I Low
   - Power: P High / P Low
2. Select the voltage and current **ranges** (HIGH or LOW)
3. Enable the test: **Test = ON**
4. Click **Read** to get the result: **PASS** or **FAIL**

---

## System Tab

Device system parameter management.

### Protections

| Parameter | Description |
|---|---|
| **Vmax** | Overvoltage limit (V) |
| **Imax** | Overcurrent limit (A) |
| **Pmax** | Overpower limit (W) |
| **Von / Voff** | Voltage enable/disable thresholds |
| **Off Delay** | Delay before shutdown (s) |

### Settings

| Parameter | Description |
|---|---|
| **Startup mode** | Startup behavior (ON/OFF) |
| **Language** | Device language |
| **Baud Rate** | Serial communication speed |

### Device file management

The device can store configurations in internal memory:

| Button | Action |
|---|---|
| **Store** | Saves the config to a device slot |
| **Recall** | Loads a config from a slot |
| **Delete** | Erases a slot |
| **Verify** | Checks if a slot contains data |

---

## Terminal Tab

SCPI console for direct communication with the device.

### Usage

1. Type a command in the input field (e.g. `*IDN?`, `MEAS:ALL?`, `CH:MODE CC`)
2. Press **Enter** or click **Send**
3. The response is displayed in the log below

### Quick buttons

- **MEAS:ALL?** — Read all measurements
- **CH:MODE?** — Read the current mode
- **CRANge?** — Read the current range

### Command examples

```
*IDN?                  Device identification
CH:MODE?               Current mode (CC, CV, CR, etc.)
CH:MODE CC             Switch to CC mode
CH:SW ON               Enable the load
CH:SW OFF              Disable the load
MEAS:ALL?              All measurements (I V P R)
CURR:CC 1.5            Set CC current to 1.5A
VOLT:CV 12.0           Set CV voltage to 12V
SYST:LOCA              Return control to the front panel
```

---

## Tips

- **Quick open**: open `index.html` directly from the file explorer (double-click) — no web server needed
- **Config name**: the suggested name starts with `-` so you can type your name before it (e.g. `BattLiPo4S-ET5410-2026-02-27-CC.ET5410`)
- **Excel export**: the CSV format uses semicolons as separator — Excel opens it correctly in Europe
- **USB stability**: if the USB port locks up, unplug and replug the cable, then reconnect
- **Multiple tabs**: live measurements (Control), polling (Measurements) and battery test can coexist simultaneously
- **Mode change**: changing mode automatically disables the load — this is a device behavior, not an application behavior
- **Decimal separator**: you can type either a period (`.`) or a comma (`,`) as decimal separator in all number fields — both are accepted
