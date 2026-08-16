"""Bitmap fonts for the Yeelight Cube Lite text renderer.

Two font sizes are supported:
- ``FONT_4X5``: 4 pixels wide × 5 pixels tall (more detail)
- ``FONT_3X5``: 3 pixels wide × 5 pixels tall (fits more characters)

Each character is a list of 5 rows. For 4-wide fonts each row is a 4-bit
integer (MSB = leftmost pixel); for 3-wide fonts each row is a 3-bit integer.
A set bit means the pixel is lit.
"""

from __future__ import annotations

FONT_4X5: dict[str, list[int]] = {
    "A": [0b0110, 0b1001, 0b1111, 0b1001, 0b1001],
    "B": [0b1110, 0b1001, 0b1110, 0b1001, 0b1110],
    "C": [0b0111, 0b1000, 0b1000, 0b1000, 0b0111],
    "D": [0b1110, 0b1001, 0b1001, 0b1001, 0b1110],
    "E": [0b1111, 0b1000, 0b1110, 0b1000, 0b1111],
    "F": [0b1111, 0b1000, 0b1110, 0b1000, 0b1000],
    "G": [0b0111, 0b1000, 0b1011, 0b1001, 0b0111],
    "H": [0b1001, 0b1001, 0b1111, 0b1001, 0b1001],
    "I": [0b1110, 0b0100, 0b0100, 0b0100, 0b1110],
    "J": [0b0111, 0b0010, 0b0010, 0b1010, 0b0110],
    "K": [0b1001, 0b1010, 0b1100, 0b1010, 0b1001],
    "L": [0b1000, 0b1000, 0b1000, 0b1000, 0b1111],
    "M": [0b1001, 0b1111, 0b1111, 0b1001, 0b1001],
    "N": [0b1001, 0b1101, 0b1011, 0b1001, 0b1001],
    "O": [0b0110, 0b1001, 0b1001, 0b1001, 0b0110],
    "P": [0b1110, 0b1001, 0b1110, 0b1000, 0b1000],
    "Q": [0b0110, 0b1001, 0b1001, 0b1011, 0b0111],
    "R": [0b1110, 0b1001, 0b1110, 0b1010, 0b1001],
    "S": [0b0111, 0b1000, 0b0110, 0b0001, 0b1110],
    "T": [0b1111, 0b0100, 0b0100, 0b0100, 0b0100],
    "U": [0b1001, 0b1001, 0b1001, 0b1001, 0b0110],
    "V": [0b1001, 0b1001, 0b1001, 0b0110, 0b0110],
    "W": [0b1001, 0b1001, 0b1111, 0b1111, 0b1001],
    "X": [0b1001, 0b0110, 0b0110, 0b0110, 0b1001],
    "Y": [0b1001, 0b0110, 0b0100, 0b0100, 0b0100],
    "Z": [0b1111, 0b0001, 0b0110, 0b1000, 0b1111],
    "0": [0b0110, 0b1011, 0b1101, 0b1001, 0b0110],
    "1": [0b0100, 0b1100, 0b0100, 0b0100, 0b1110],
    "2": [0b0110, 0b1001, 0b0010, 0b0100, 0b1111],
    "3": [0b1110, 0b0001, 0b0110, 0b0001, 0b1110],
    "4": [0b1001, 0b1001, 0b1111, 0b0001, 0b0001],
    "5": [0b1111, 0b1000, 0b1110, 0b0001, 0b1110],
    "6": [0b0110, 0b1000, 0b1110, 0b1001, 0b0110],
    "7": [0b1111, 0b0001, 0b0010, 0b0100, 0b0100],
    "8": [0b0110, 0b1001, 0b0110, 0b1001, 0b0110],
    "9": [0b0110, 0b1001, 0b0111, 0b0001, 0b0110],
    " ": [0b0000, 0b0000, 0b0000, 0b0000, 0b0000],
    "!": [0b0100, 0b0100, 0b0100, 0b0000, 0b0100],
    "?": [0b0110, 0b0001, 0b0010, 0b0000, 0b0010],
    "-": [0b0000, 0b0000, 0b1110, 0b0000, 0b0000],
    ".": [0b0000, 0b0000, 0b0000, 0b0000, 0b0100],
    ":": [0b0000, 0b0100, 0b0000, 0b0100, 0b0000],
}

FONT_3X5: dict[str, list[int]] = {
    "A": [0b010, 0b101, 0b111, 0b101, 0b101],
    "B": [0b110, 0b101, 0b110, 0b101, 0b110],
    "C": [0b011, 0b100, 0b100, 0b100, 0b011],
    "D": [0b110, 0b101, 0b101, 0b101, 0b110],
    "E": [0b111, 0b100, 0b110, 0b100, 0b111],
    "F": [0b111, 0b100, 0b110, 0b100, 0b100],
    "G": [0b011, 0b100, 0b101, 0b101, 0b011],
    "H": [0b101, 0b101, 0b111, 0b101, 0b101],
    "I": [0b111, 0b010, 0b010, 0b010, 0b111],
    "J": [0b111, 0b001, 0b001, 0b101, 0b010],
    "K": [0b101, 0b101, 0b110, 0b101, 0b101],
    "L": [0b100, 0b100, 0b100, 0b100, 0b111],
    "M": [0b101, 0b111, 0b111, 0b101, 0b101],
    "N": [0b101, 0b111, 0b111, 0b101, 0b101],
    "O": [0b010, 0b101, 0b101, 0b101, 0b010],
    "P": [0b110, 0b101, 0b110, 0b100, 0b100],
    "Q": [0b010, 0b101, 0b101, 0b111, 0b011],
    "R": [0b110, 0b101, 0b110, 0b101, 0b101],
    "S": [0b011, 0b100, 0b010, 0b001, 0b110],
    "T": [0b111, 0b010, 0b010, 0b010, 0b010],
    "U": [0b101, 0b101, 0b101, 0b101, 0b010],
    "V": [0b101, 0b101, 0b101, 0b010, 0b010],
    "W": [0b101, 0b101, 0b111, 0b111, 0b101],
    "X": [0b101, 0b010, 0b010, 0b010, 0b101],
    "Y": [0b101, 0b010, 0b010, 0b010, 0b010],
    "Z": [0b111, 0b001, 0b010, 0b100, 0b111],
    "0": [0b111, 0b101, 0b101, 0b101, 0b111],
    "1": [0b110, 0b010, 0b010, 0b010, 0b111],
    "2": [0b111, 0b001, 0b111, 0b100, 0b111],
    "3": [0b111, 0b001, 0b011, 0b001, 0b111],
    "4": [0b101, 0b101, 0b111, 0b001, 0b001],
    "5": [0b111, 0b100, 0b111, 0b001, 0b111],
    "6": [0b111, 0b100, 0b111, 0b101, 0b111],
    "7": [0b111, 0b001, 0b001, 0b001, 0b001],
    "8": [0b111, 0b101, 0b111, 0b101, 0b111],
    "9": [0b111, 0b101, 0b111, 0b001, 0b111],
    " ": [0b000, 0b000, 0b000, 0b000, 0b000],
    "!": [0b010, 0b010, 0b010, 0b000, 0b010],
    "?": [0b110, 0b001, 0b010, 0b000, 0b010],
    "-": [0b000, 0b000, 0b111, 0b000, 0b000],
    ".": [0b000, 0b000, 0b000, 0b000, 0b010],
    ":": [0b000, 0b010, 0b000, 0b010, 0b000],
}

CHAR_HEIGHT = 5
CHAR_SPACING = 1  # blank column between characters

FONTS = {
    "4x5": (FONT_4X5, 4),
    "3x5": (FONT_3X5, 3),
}


def text_to_columns(text: str, font_size: str = "4x5") -> list[list[bool]]:
    """Convert text to a list of columns (each column = 5 bools, top to bottom).

    ``font_size`` must be ``"4x5"`` or ``"3x5"``. Unknown characters are
    replaced with a space.
    """
    font, char_width = FONTS[font_size]
    columns: list[list[bool]] = []
    for i, ch in enumerate(text.upper()):
        rows = font.get(ch, font[" "])
        for col in range(char_width):
            columns.append([bool(row >> (char_width - 1 - col) & 1) for row in rows])
        if i < len(text) - 1:
            columns.append([False] * CHAR_HEIGHT)
    return columns


def render_frame(
    columns: list[list[bool]],
    offset: int,
    width: int = 20,
    height: int = 5,
    color: tuple[int, int, int] = (255, 255, 255),
    bg: tuple[int, int, int] = (0, 0, 0),
) -> list[tuple[int, int, int]]:
    """Return a flat row-major list of (r,g,b) for a width x height grid.

    ``offset`` is the first column of ``columns`` to show (for scrolling).
    Columns beyond the end of the text are filled with ``bg``.
    """
    pixels: list[tuple[int, int, int]] = []
    for row in range(height - 1, -1, -1):  # row 0 of font = bottom of panel
        for col in range(width):
            src = offset + col
            if 0 <= src < len(columns) and columns[src][row]:
                pixels.append(color)
            else:
                pixels.append(bg)
    return pixels
