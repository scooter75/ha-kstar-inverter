"""DataUpdateCoordinator for Kstar Inverter."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .modbus_client import KstarModbusClient

_LOGGER = logging.getLogger(__name__)


class KstarDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Kstar inverter data over RS485."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: KstarModbusClient,
        scan_interval: int,
        system_info: dict[str, Any],
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.client = client
        self.system_info = system_info

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch telemetry data from the inverter."""
        try:
            return await self.client.read_telemetry()
        except ConnectionError as err:
            raise UpdateFailed(f"Error communicating with Kstar inverter: {err}") from err
