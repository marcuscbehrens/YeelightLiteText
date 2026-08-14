"""The Yeelight Lite Text integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_BG, CONF_COLOR, CONF_FONT_SIZE, DEFAULT_FONT_SIZE, DOMAIN
from .tcp import CubeTCP

PLATFORMS = [Platform.TEXT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    tcp = await hass.async_add_executor_job(
        CubeTCP, entry.data[CONF_HOST], entry.data[CONF_PORT]
    )
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "tcp": tcp,
        "color": entry.data.get(CONF_COLOR, "#ffffff"),
        "bg": entry.data.get(CONF_BG, "#000000"),
        "font_size": entry.data.get(CONF_FONT_SIZE, DEFAULT_FONT_SIZE),
    }
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        data = hass.data[DOMAIN].pop(entry.entry_id, {})
        tcp: CubeTCP = data.get("tcp")
        if tcp:
            await hass.async_add_executor_job(tcp.close)
    return unload_ok
