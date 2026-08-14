"""Config flow for Yeelight Lite Text."""

from __future__ import annotations

import socket
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import (
    CONF_BG,
    CONF_COLOR,
    CONF_FONT_SIZE,
    DEFAULT_BG,
    DEFAULT_COLOR,
    DEFAULT_FONT_SIZE,
    DEFAULT_PORT,
    DOMAIN,
)

STEP_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_COLOR, default=DEFAULT_COLOR): str,
        vol.Required(CONF_BG, default=DEFAULT_BG): str,
        vol.Required(CONF_FONT_SIZE, default=DEFAULT_FONT_SIZE): vol.In(["4x5", "3x5"]),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Yeelight Lite Text."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            try:
                await self.hass.async_add_executor_job(_test_connect, host, port)
            except Exception:  # noqa: BLE001
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=host, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_SCHEMA, errors=errors
        )


def _test_connect(host: str, port: int) -> None:
    s = socket.create_connection((host, port), timeout=5)
    s.close()
