# Kstar Inverter (RS485 Modbus) for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A native custom integration for **Home Assistant** to monitor and control **Kstar KSG / BluE series solar inverters** (`1 kW – 250 kW`) over **RS485 Modbus RTU**, built strictly to the *Kstar KSG1-250K Inverter Modbus Communications Protocol V3.5*.

---

## Features

* **UI Configuration (`ConfigFlow`)**: Easy setup via **Settings > Devices & Services** with live connection validation.
* **Home Assistant Energy Dashboard Ready**: High-resolution (`0.1 kWh`) daily and total energy yield sensors with proper `total_increasing` state classes.
* **Real-Time Telemetry (`04H` Input Registers)**:
  * PV1, PV2, and PV3 Voltage (`V`), Current (`A`), and Power (`W`)
  * Single-phase & Three-phase Grid Voltage (`V`), Current (`A`), and Frequency (`Hz`)
  * Active Power (`W`), Apparent Power (`VA`), Reactive Power (`var`), and Power Factor
  * Radiator & Module Temperatures (`°C`), Bus Voltages (`V`), Fan Speeds (`RPM`), and DC Insulation Resistance (`kΩ`)
* **Human-Readable Diagnostics**: Automatically decodes bitmasked DSP Alarm Codes (`W00–W07`), DSP Error Codes (`F00–F29`), Operating Modes, and Inverter Models.
* **Active Power & Export Control (`06H` Write Registers)**:
  * Remote Control Enable switch (Register `4029`)
  * Active Power Limit `%` control (Register `4004`)
  * Back-Current / Zero-Export Power Limit `W` control (Register `4020`)
  * Remote Power Off / Revoke Power Off & I/V Curve Scan triggers

---

## Hardware & Inverter Prerequisites

1. **RS485 Wiring**:
   * Connect **A+ (D+)** on your USB-to-RS485 adapter to **RS485 A+** on the Kstar inverter communication terminal.
   * Connect **B- (D-)** on your USB-to-RS485 adapter to **RS485 B-** on the inverter.
2. **Inverter Menu Settings**:
   * On the inverter's LCD menu, set **485 Protocol / Agreement** to **`MODBUS`** (value `1`, not `KSTAR`).
   * Verify the **Baud Rate** (default `9600 bps`) and **RS485 Address** (default `1`, range `1–32`).

---

## Installation via HACS (Recommended)

1. Open **HACS** in your Home Assistant instance.
2. Click the three dots (`⋮`) in the top-right corner and select **Custom repositories**.
3. Paste the URL of this GitHub repository and select **Integration** as the category.
4. Click **Add**, search for **Kstar Inverter (RS485 Modbus)**, and click **Download**.
5. **Restart Home Assistant**.

### Manual Installation

1. Download the latest release or clone this repository.
2. Copy the `custom_components/kstar_inverter` folder into your Home Assistant `<config>/custom_components/` directory.
3. **Restart Home Assistant**.

---

## Configuration

1. In Home Assistant, go to **Settings > Devices & Services**.
2. Click **+ Add Integration** in the bottom-right corner.
3. Search for **Kstar Inverter (RS485 Modbus)**.
4. Enter your RS485 parameters:
   * **Serial Port Path**: e.g. `/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0` or `/dev/ttyUSB0`
   * **Baud Rate**: `9600` (default)
   * **Inverter Modbus Address**: `1` (default)
   * **Polling Interval**: `10` seconds (default)

> **Note:** Many string inverters power down their communication board at night when PV voltage drops to zero. During nighttime or `System Initialization`, sensors may report `Unavailable` until sunrise.

---

## Repository Structure

```text
ha-kstar-inverter/
├── hacs.json
├── README.md
└── custom_components/
    └── kstar_inverter/
        ├── __init__.py
        ├── button.py
        ├── config_flow.py
        ├── const.py
        ├── coordinator.py
        ├── entity.py
        ├── manifest.json
        ├── modbus_client.py
        ├── number.py
        ├── sensor.py
        ├── strings.json
        ├── switch.py
        └── translations/
            └── en.json
```
