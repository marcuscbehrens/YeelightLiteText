"""4-wide x 5-tall bitmap font for uppercase A-Z and digits 0-9.

Each character is a list of 5 rows, each row a 4-bit integer (MSB = leftmost pixel).
A set bit means the pixel is lit.
"""

from __future__ import annotations

FONT: dict[str, list[int]] = {
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

CHAR_WIDTH = 4
CHAR_HEIGHT = 5
CHAR_SPACING = 1  # blank column between characters


def text_to_columns(text: str) -> list[list[bool]]:
    """Convert text to a list of columns (each column = 5 bools, top to bottom).

    Unknown characters are replaced with a space.
    """
    columns: list[list[bool]] = []
    for i, ch in enumerate(text.upper()):
        rows = FONT.get(ch, FONT[" "])
        for col in range(CHAR_WIDTH):
            columns.append([bool(row >> (3 - col) & 1) for row in rows])
        if i < len(text) - 1:
            columns.append([False] * CHAR_HEIGHT)  # spacing column
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
    for row in range(height):
        for col in range(width):
            src = offset + col
            if 0 <= src < len(columns) and columns[src][row]:
                pixels.append(color)
            else:
                pixels.append(bg)
    return pixels
