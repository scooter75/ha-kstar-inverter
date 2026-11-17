"""The Kstar Inverter (RS485 / TCP Modbus) integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BAUDRATE,
    CONF_CONNECTION_TYPE,
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_SERIAL_PORT,
    CONF_SLAVE_ID,
    CONN_TYPE_SERIAL,
    CONN_TYPE_TCP,
    DEFAULT_BAUDRATE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SERIAL_PORT,
    DEFAULT_SLAVE_ID,
    DEFAULT_TCP_PORT,
    DOMAIN,
)
from .coordinator import KstarDataUpdateCoordinator
from .modbus_client import KstarModbusClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.BUTTON,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kstar Inverter from a config entry."""
    conn_type = entry.data.get(CONF_CONNECTION_TYPE, CONN_TYPE_SERIAL)
    slave_id = entry.data.get(CONF_SLAVE_ID, DEFAULT_SLAVE_ID)
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    if conn_type == CONN_TYPE_TCP:
        client = KstarModbusClient(
            connection_type=CONN_TYPE_TCP,
            slave_id=slave_id,
            host=entry.data[CONF_HOST],
            tcp_port=entry.data.get(CONF_PORT, DEFAULT_TCP_PORT),
        )
    else:
        client = KstarModbusClient(
            connection_type=CONN_TYPE_SERIAL,
            slave_id=slave_id,
            serial_port=entry.data.get(CONF_SERIAL_PORT, DEFAULT_SERIAL_PORT),
            baudrate=entry.data.get(CONF_BAUDRATE, DEFAULT_BAUDRATE),
        )

    system_info = await client.read_system_info()

    coordinator = KstarDataUpdateCoordinator(
        hass=hass,
        client=client,
        scan_interval=scan_interval,
        system_info=system_info,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator: KstarDataUpdateCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.client.close()

    return unload_ok
