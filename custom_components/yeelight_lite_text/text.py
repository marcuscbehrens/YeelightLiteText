"""Text entity for Yeelight Lite Text — type text, it appears on the panel."""

from __future__ import annotations

import base64
import logging
import re

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .font import render_frame, text_to_columns
from .tcp import CubeTCP

_LOGGER = logging.getLogger(__name__)

PANEL_WIDTH = 20
PANEL_HEIGHT = 5
_HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    display = YeelightLiteTextEntity(data["tcp"], data["color"], data["bg"], data["font_size"], entry)
    color = YeelightLiteColorEntity(display, data["color"], entry)
    async_add_entities([display, color])


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    v = hex_color.lstrip("#")
    return (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))


def _encode_frame(pixels: list[tuple[int, int, int]]) -> str:
    return "".join(
        base64.b64encode(bytes([r, g, b])).decode() for r, g, b in pixels
    )


def _push_text(tcp: CubeTCP, text: str, color_hex: str, bg_hex: str, font_size: str) -> None:
    color = _hex_to_rgb(color_hex)
    bg = _hex_to_rgb(bg_hex)
    columns = text_to_columns(text, font_size)
    offset = -max(0, (PANEL_WIDTH - len(columns)) // 2)
    pixels = render_frame(columns, offset=offset, width=PANEL_WIDTH, height=PANEL_HEIGHT, color=color, bg=bg)
    frame = _encode_frame(pixels)
    tcp.send("activate_fx_mode", [{"mode": "direct"}])
    tcp.send("update_leds", [frame])


class YeelightLiteTextEntity(TextEntity):
    """Text input — whatever you type is rendered on the panel."""

    _attr_name = "Display Text"
    _attr_native_min = 0
    _attr_native_max = 32
    _attr_native_value = ""
    _attr_should_poll = False

    def __init__(self, tcp: CubeTCP, color: str, bg: str, font_size: str, entry: ConfigEntry) -> None:
        self._tcp = tcp
        self._color = color
        self._bg = bg
        self._font_size = font_size
        self._attr_unique_id = f"{entry.entry_id}_text"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Yeelight Cube Lite",
            manufacturer="Yeelight",
            model="Cube Lite",
        )

    async def async_set_value(self, value: str) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()
        await self._redraw()

    async def _redraw(self) -> None:
        try:
            await self.hass.async_add_executor_job(
                _push_text, self._tcp, self._attr_native_value, self._color, self._bg, self._font_size
            )
        except Exception as exc:  # noqa: BLE001
            _LOGGER.error("Failed to push text to Cube Lite: %s", exc)


class YeelightLiteColorEntity(TextEntity):
    """Color input — enter a hex color (e.g. #ff0000) to change the text color live."""

    _attr_name = "Text Color"
    _attr_native_min = 4   # #rgb shortest valid
    _attr_native_max = 7   # #rrggbb
    _attr_should_poll = False
    _attr_pattern = "^#[0-9a-fA-F]{6}$"

    def __init__(self, display: YeelightLiteTextEntity, color: str, entry: ConfigEntry) -> None:
        self._display = display
        self._attr_native_value = color
        self._attr_unique_id = f"{entry.entry_id}_color"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Yeelight Cube Lite",
            manufacturer="Yeelight",
            model="Cube Lite",
        )

    async def async_set_value(self, value: str) -> None:
        if not _HEX_RE.match(value):
            _LOGGER.warning("Invalid hex color ignored: %r", value)
            return
        color = value if value.startswith("#") else f"#{value}"
        self._attr_native_value = color
        self.async_write_ha_state()
        self._display._color = color
        await self._display._redraw()
