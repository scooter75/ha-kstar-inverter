"""Button platform for Kstar Inverter remote actions (Function Code 0x06)."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    REG_CLEAR_FAULT_RECORD,
    REG_REMOTE_OFF,
    REG_REVOKE_REMOTE_OFF,
    REG_START_IV_SCAN,
)
from .coordinator import KstarDataUpdateCoordinator
from .entity import KstarEntity


@dataclass(frozen=True)
class KstarButtonEntityDescription(ButtonEntityDescription):
    """Describes Kstar button entity."""

    register: int = 0
    payload: int = 1


BUTTONS: tuple[KstarButtonEntityDescription, ...] = (
    KstarButtonEntityDescription(
        key="remote_power_off",
        name="Remote Power Off",
        register=REG_REMOTE_OFF,
        payload=1,
        icon="mdi:power-off",
    ),
    KstarButtonEntityDescription(
        key="revoke_remote_power_off",
        name="Revoke Remote Power Off",
        register=REG_REVOKE_REMOTE_OFF,
        payload=1,
        icon="mdi:power-on",
    ),
    KstarButtonEntityDescription(
        key="start_iv_scan",
        name="Start I/V Curve Scan",
        register=REG_START_IV_SCAN,
        payload=1,
        icon="mdi:chart-bell-curve-cumulative",
    ),
    KstarButtonEntityDescription(
        key="clear_fault_record",
        name="Clear Fault Record",
        register=REG_CLEAR_FAULT_RECORD,
        payload=1,
        icon="mdi:broom",
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kstar action buttons."""
    coordinator: KstarDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        KstarButton(coordinator, description) for description in BUTTONS
    )


class KstarButton(KstarEntity, ButtonEntity):
    """Representation of a Kstar Inverter action button."""

    entity_description: KstarButtonEntityDescription

    def __init__(
        self,
        coordinator: KstarDataUpdateCoordinator,
        description: KstarButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    async def async_press(self) -> None:
        """Handle button press."""
        if await self.coordinator.client.write_register(
            self.entity_description.register, self.entity_description.payload
        ):
            await self.coordinator.async_request_refresh()
