"""Config flow for Kstar Inverter (RS485 Modbus) integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    BAUDRATES,
    CONF_BAUDRATE,
    CONF_SCAN_INTERVAL,
    CONF_SERIAL_PORT,
    CONF_SLAVE_ID,
    DEFAULT_BAUDRATE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SERIAL_PORT,
    DEFAULT_SLAVE_ID,
    DOMAIN,
)
from .modbus_client import KstarModbusClient

_LOGGER = logging.getLogger(__name__)


class KstarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kstar Inverter."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            port = user_input[CONF_SERIAL_PORT]
            baudrate = user_input[CONF_BAUDRATE]
            slave_id = user_input[CONF_SLAVE_ID]

            await self.async_set_unique_id(f"{port}_{slave_id}")
            self._abort_if_unique_id_configured()

            client = KstarModbusClient(port=port, baudrate=baudrate, slave_id=slave_id)
            try:
                await client.read_telemetry()
                sys_info = await client.read_system_info()
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception connecting to Kstar inverter")
                errors["base"] = "unknown"
            finally:
                await client.close()

            if not errors:
                model = sys_info.get("machine_model", "Kstar Inverter")
                title = f"{model} (ID {slave_id})"
                return self.async_create_entry(title=title, data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_SERIAL_PORT, default=DEFAULT_SERIAL_PORT): str,
                vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.In(BAUDRATES),
                vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=32)
                ),
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                    vol.Coerce(int), vol.Range(min=5, max=300)
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> KstarOptionsFlowHandler:
        """Get the options flow for this handler."""
        return KstarOptionsFlowHandler(config_entry)


class KstarOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Kstar Inverter options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=current_interval
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
                }
            ),
        )
