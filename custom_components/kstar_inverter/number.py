"""Number platform for Kstar Inverter power control (Function Code 0x06)."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, REG_SET_ACTIVE_POWER_PCT, REG_SET_BACK_CURRENT_LIMIT
from .coordinator import KstarDataUpdateCoordinator
from .entity import KstarEntity


@dataclass(frozen=True)
class KstarNumberEntityDescription(NumberEntityDescription):
    """Describes Kstar number entity."""

    register: int = 0
    state_key: str = ""


NUMBERS: tuple[KstarNumberEntityDescription, ...] = (
    KstarNumberEntityDescription(
        key="active_power_limit",
        name="Active Power Limit",
        register=REG_SET_ACTIVE_POWER_PCT,
        state_key="preset_active_power_pct",
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        mode=NumberMode.BOX,
        icon="mdi:speedometer",
    ),
    KstarNumberEntityDescription(
        key="back_current_limit",
        name="Export Power Limit",
        register=REG_SET_BACK_CURRENT_LIMIT,
        state_key="back_current_limit",
        native_min_value=0,
        native_max_value=65535,
        native_step=10,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        mode=NumberMode.BOX,
        icon="mdi:transmission-tower-export",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kstar number controls."""
    coordinator: KstarDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        KstarNumber(coordinator, description) for description in NUMBERS
    )


class KstarNumber(KstarEntity, NumberEntity):
    """Representation of a Kstar Inverter writable numeric register."""

    entity_description: KstarNumberEntityDescription

    def __init__(
        self,
        coordinator: KstarDataUpdateCoordinator,
        description: KstarNumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if not self.coordinator.data:
            return None
        val = self.coordinator.data.get(self.entity_description.state_key)
        return float(val) if val is not None else None

    async def async_set_native_value(self, value: float) -> None:
        """Write new value to the inverter register."""
        if await self.coordinator.client.write_register(
            self.entity_description.register, int(value)
        ):
            await self.coordinator.async_request_refresh()
