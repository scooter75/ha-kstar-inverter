"""Base entity for Kstar Inverter integration."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KstarDataUpdateCoordinator


class KstarEntity(CoordinatorEntity[KstarDataUpdateCoordinator]):
    """Base class for Kstar Inverter entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: KstarDataUpdateCoordinator, key: str) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._key = key
        serial = coordinator.system_info.get("serial_number", "Unknown")
        model = coordinator.system_info.get("machine_model", "KSG Series")
        fw = coordinator.system_info.get("firmware_version")

        identifier = f"{coordinator.client.port}_{coordinator.client.slave_id}"
        self._attr_unique_id = f"{identifier}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, identifier)},
            name=f"Kstar {model} ({coordinator.client.slave_id})",
            manufacturer="Shenzhen Kstar Science & Technology",
            model=model,
            serial_number=serial if serial != "Unknown" else None,
            sw_version=fw,
        )
