"""Switch platform for Kstar Inverter remote control (Function Code 0x06)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, REG_REMOTE_CONTROL_ENABLE
from .coordinator import KstarDataUpdateCoordinator
from .entity import KstarEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kstar switches."""
    coordinator: KstarDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KstarRemoteControlSwitch(coordinator)])


class KstarRemoteControlSwitch(KstarEntity, SwitchEntity):
    """Switch to enable/disable Remote Control (Register 4029)."""

    _attr_name = "Remote Control Enable"
    _attr_icon = "mdi:remote"

    def __init__(self, coordinator: KstarDataUpdateCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, "remote_control_enable")

    @property
    def is_on(self) -> bool | None:
        """Return true if remote control is enabled."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("remote_control_enabled")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable remote control."""
        if await self.coordinator.client.write_register(REG_REMOTE_CONTROL_ENABLE, 1):
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable remote control."""
        if await self.coordinator.client.write_register(REG_REMOTE_CONTROL_ENABLE, 0):
            await self.coordinator.async_request_refresh()
