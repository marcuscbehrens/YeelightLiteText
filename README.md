# Yeelight Cube Lite Text

A Home Assistant custom integration that renders text on the **Yeelight Cube Lite** (5×20 LED panel) via direct TCP — no cloud, no Yeelight app, no external dependencies.

## How it works

Type text into a HA text entity → the integration sends `activate_fx_mode` + `update_leds` commands directly to the device over TCP, rendering the text using a built-in bitmap font.

## Prerequisites

1. **Enable LAN control** in the Yeelight app: open the device → Settings → LAN Control → toggle on
2. **Close the Yeelight app** after enabling LAN control — leaving it open causes connection conflicts with Home Assistant

## Supported characters

A–Z, 0–9, space, `!`, `?`, `-`, `.`, `:`

## Font sizes

| Size | Width | Best for |
|---|---|---|
| `4x5` | 4 px wide | Letters — more readable |
| `3x5` | 3 px wide | Numbers — fits more characters (up to 5 on screen) |

## Installation

### HACS (recommended)

1. **HACS → ⋮ → Custom repositories** → add `https://github.com/marcuscbehrens/YeelightLiteText`, category **Integration**
2. Open it → **Download**
3. Restart Home Assistant

### Manual

Copy `custom_components/yeelight_lite_text/` into your `config/custom_components/` folder and restart Home Assistant.

## Configuration

**Settings → Devices & Services → Add Integration → "Yeelight Cube Lite Text"**

| Field | Description |
|---|---|
| IP Address | Local IP of your Cube Lite |
| Port | TCP port (default: `55443`) |
| Text color | Hex color for the text, e.g. `#ffffff` |
| Background color | Hex color for the background, e.g. `#000000` |
| Font size | `4x5` (default) or `3x5` |

## Usage

After setup a **text entity** (`text.display_text`) appears. Set its value from the UI, an automation, or a script:

```yaml
action: text.set_value
target:
  entity_id: text.display_text
data:
  value: "HELLO"
```

Text wider than 20 columns is clipped at the right edge.

## Requirements

- Home Assistant 2024.4.0+
- Yeelight Cube Lite reachable on the local network with LAN control enabled
- No Python package dependencies
