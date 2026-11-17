"""Modbus RTU / TCP client wrapper for Kstar KSG1-250K Inverter (Protocol V3.5)."""
from __future__ import annotations

import asyncio
import logging
import struct
from typing import Any

from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from .const import (
    CONN_TYPE_TCP,
    DEFAULT_BAUDRATE,
    DEFAULT_SERIAL_PORT,
    DEFAULT_TCP_PORT,
    DSP_ALARM_CODES,
    DSP_ERROR_CODES,
    INVERTER_MODELS,
    OPERATING_MODES,
)

_LOGGER = logging.getLogger(__name__)


def _decode_bits(value: int, mapping: dict[int, str]) -> str:
    """Decode bitmask into human-readable comma-separated string."""
    if value == 0:
        return "None"
    active = [desc for bit, desc in mapping.items() if value & (1 << bit)]
    return ", ".join(active) if active else f"Code 0x{value:X}"


def _to_s16(val: int) -> int:
    """Convert unsigned 16-bit integer to signed 16-bit integer."""
    return val - 0x10000 if val >= 0x8000 else val


def _to_u32(high: int, low: int) -> int:
    """Combine two big-endian 16-bit registers into unsigned 32-bit integer."""
    return (high << 16) | low


def _to_s32(high: int, low: int) -> int:
    """Combine two big-endian 16-bit registers into signed 32-bit integer."""
    val = (high << 16) | low
    return val - 0x100000000 if val >= 0x80000000 else val


def _regs_to_ascii(regs: list[int]) -> str:
    """Convert big-endian 16-bit registers to stripped ASCII string."""
    raw_bytes = b"".join(struct.pack(">H", r) for r in regs)
    return raw_bytes.decode("ascii", errors="ignore").strip("\x00 ").strip()


class KstarModbusClient:
    """Async Modbus client supporting RS485 Serial RTU and Modbus over TCP."""

    def __init__(
        self,
        connection_type: str,
        slave_id: int,
        serial_port: str = DEFAULT_SERIAL_PORT,
        baudrate: int = DEFAULT_BAUDRATE,
        host: str = "",
        tcp_port: int = DEFAULT_TCP_PORT,
    ) -> None:
        """Initialize the Modbus client."""
        self.connection_type = connection_type
        self.slave_id = slave_id
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.host = host
        self.tcp_port = tcp_port
        self._lock = asyncio.Lock()

        if connection_type == CONN_TYPE_TCP:
            self.endpoint_id = f"{host}:{tcp_port}"
            self._client: AsyncModbusSerialClient | AsyncModbusTcpClient = (
                AsyncModbusTcpClient(
                    host=host,
                    port=tcp_port,
                    timeout=3,
                )
            )
        else:
            self.endpoint_id = serial_port
            self._client = AsyncModbusSerialClient(
                port=serial_port,
                baudrate=baudrate,
                bytesize=8,
                parity="N",
                stopbits=1,
                timeout=3,
            )

    async def connect(self) -> bool:
        """Connect to the RS485 serial port or TCP endpoint."""
        if not self._client.connected:
            return await self._client.connect()
        return True

    async def close(self) -> None:
        """Close the Modbus connection."""
        if self._client.connected:
            self._client.close()

    async def _read_input_registers(self, address: int, count: int) -> list[int] | None:
        """Read input registers (Function Code 0x04)."""
        try:
            res = await self._client.read_input_registers(
                address=address, count=count, slave=self.slave_id
            )
            if res.isError():
                _LOGGER.debug("Modbus error reading input 0x04 at %s: %s", address, res)
                return None
            return res.registers
        except ModbusException as err:
            _LOGGER.debug("Modbus exception reading input %s: %s", address, err)
            return None

    async def _read_holding_registers(self, address: int, count: int) -> list[int] | None:
        """Read holding registers (Function Code 0x03)."""
        try:
            res = await self._client.read_holding_registers(
                address=address, count=count, slave=self.slave_id
            )
            if res.isError():
                _LOGGER.debug("Modbus error reading holding 0x03 at %s: %s", address, res)
                return None
            return res.registers
        except ModbusException as err:
            _LOGGER.debug("Modbus exception reading holding %s: %s", address, err)
            return None

    async def write_register(self, address: int, value: int) -> bool:
        """Write a single register (Function Code 0x06)."""
        async with self._lock:
            if not await self.connect():
                return False
            try:
                res = await self._client.write_register(
                    address=address, value=value, slave=self.slave_id
                )
                if res.isError():
                    _LOGGER.error("Failed writing %s to register %s: %s", value, address, res)
                    return False
                return True
            except ModbusException as err:
                _LOGGER.error("Exception writing %s to register %s: %s", value, address, err)
                return False

    async def read_system_info(self) -> dict[str, Any]:
        """Read static system information via Function Code 0x03 (Registers 3200-3230)."""
        async with self._lock:
            if not await self.connect():
                return {}
            regs = await self._read_holding_registers(3200, 31)
            if not regs or len(regs) < 31:
                return {}

            machine_model = _regs_to_ascii(regs[0:5])
            dsp_ver = regs[5] >> 8
            arm_ver = regs[5] & 0xFF
            serial_number = _regs_to_ascii(regs[6:17])
            model_new = _regs_to_ascii(regs[21:29])

            return {
                "machine_model": model_new or machine_model or "Kstar Inverter",
                "serial_number": serial_number or "Unknown",
                "firmware_version": f"DSP V{dsp_ver / 10:.1f} / ARM V{arm_ver / 10:.1f}",
            }

    async def read_telemetry(self) -> dict[str, Any]:
        """Read real-time telemetry via Function Code 0x04."""
        async with self._lock:
            if not await self.connect():
                raise ConnectionError(f"Unable to connect to Modbus endpoint {self.endpoint_id}")

            # Block 1: Registers 3000 to 3060 (61 registers)
            b1 = await self._read_input_registers(3000, 61)
            if not b1 or len(b1) < 61:
                raise ConnectionError("Failed to read primary telemetry block (3000-3060)")

            # Block 2: Registers 3114 to 3126 (13 registers)
            b2 = await self._read_input_registers(3114, 13)

            # Block 3: Registers 3241 to 3243 (3 registers - 0.1 kWh daily yield)
            b3 = await self._read_input_registers(3241, 3)

            op_mode_byte = b1[30] >> 8
            model_byte = b1[30] & 0xFF

            # Note from Protocol Table 3.1.4: During system initialization (0x00), data is invalid
            if op_mode_byte == 0x00:
                _LOGGER.debug("Inverter is in System Initialization; telemetry invalid")
                return {
                    "operating_mode": OPERATING_MODES.get(0x00),
                    "inverter_model_code": INVERTER_MODELS.get(model_byte, f"0x{model_byte:02X}"),
                }

            dsp_alarm_raw = b1[27]
            dsp_error_raw = _to_u32(b1[28], b1[29])
            arm_alarm_raw = b1[36] >> 8
            arm_error_raw = b1[36] & 0xFF

            pf_raw = b1[56]
            if pf_raw == 0xFFFF:
                power_factor = 1.0
            elif pf_raw >= 10000:
                power_factor = round((pf_raw - 10000) / 1000.0, 3)
            else:
                power_factor = round(pf_raw / 1000.0, 3)

            data: dict[str, Any] = {
                # PV Inputs (3000-3011)
                "pv1_voltage": round(b1[0] * 0.1, 1),
                "pv2_voltage": round(b1[1] * 0.1, 1),
                "pv3_voltage": round(b1[2] * 0.1, 1),
                "pv1_current": round(b1[3] * 0.01, 2),
                "pv2_current": round(b1[4] * 0.01, 2),
                "pv3_current": round(b1[5] * 0.01, 2),
                "pv1_power": _to_s32(b1[6], b1[7]),
                "pv2_power": _to_s32(b1[8], b1[9]),
                "pv3_power": _to_s32(b1[10], b1[11]),
                # Bus & Grid Voltages/Frequencies/Currents (3012-3022)
                "pbus_voltage": round(b1[12] * 0.1, 1),
                "nbus_voltage": round(b1[13] * 0.1, 1),
                "grid_voltage_r": round(b1[14] * 0.1, 1),
                "grid_voltage_s": round(b1[15] * 0.1, 1),
                "grid_voltage_t": round(b1[16] * 0.1, 1),
                "grid_frequency_r": round(b1[17] * 0.01, 2),
                "grid_frequency_s": round(b1[18] * 0.01, 2),
                "grid_frequency_t": round(b1[19] * 0.01, 2),
                "grid_current_r": round(b1[20] * 0.01, 2),
                "grid_current_s": round(b1[21] * 0.01, 2),
                "grid_current_t": round(b1[22] * 0.01, 2),
                # Power & Temperatures (3023-3026)
                "grid_power": _to_s32(b1[23], b1[24]),
                "radiator_temperature": round(_to_s16(b1[25]) * 0.1, 1),
                "module_temperature": round(_to_s16(b1[26]) * 0.1, 1),
                # Status, Alarms & Errors (3027-3036)
                "dsp_alarm": _decode_bits(dsp_alarm_raw, DSP_ALARM_CODES),
                "dsp_error": _decode_bits(dsp_error_raw, DSP_ERROR_CODES),
                "operating_mode": OPERATING_MODES.get(op_mode_byte, f"Unknown (0x{op_mode_byte:02X})"),
                "inverter_model_code": INVERTER_MODELS.get(model_byte, f"0x{model_byte:02X}"),
                "fan_a_speed": b1[31],
                "fan_b_speed": b1[32],
                "fan_c_speed": b1[33],
                "arm_alarm_code": arm_alarm_raw,
                "arm_error_code": arm_error_raw,
                # Energy Yields (3038-3042)
                "total_energy": round(_to_u32(b1[38], b1[39]) * 0.1, 1),
                "annual_energy": _to_u32(b1[40], b1[41]),
                "daily_energy": float(b1[42]),
                # Power Quality & Insulation (3050-3057)
                "preset_active_power_pct": b1[50],
                "apparent_power": _to_s32(b1[52], b1[53]),
                "reactive_power": _to_s32(b1[54], b1[55]),
                "power_factor": power_factor,
                "dc_insulation_resistance": b1[57],
            }

            if b2 and len(b2) >= 13:
                data["back_current_limit"] = b2[0]  # 3114
                data["remote_control_enabled"] = bool(b2[9])  # 3123
                iv_raw = b2[12]  # 3126
                iv_state = iv_raw & 0xFF
                iv_progress = (iv_raw >> 8) & 0xFF
                data["iv_scan_status"] = (
                    f"Scanning ({iv_progress}%)" if iv_state == 0 else "Idle"
                )

            if b3 and len(b3) >= 1:
                # Register 3241 provides 0.1 kWh daily resolution
                data["daily_energy"] = round(b3[0] * 0.1, 1)

            return data
