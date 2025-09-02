"""Constants and configuration for WireWorld cellular automaton."""

# --------------- WireWorld State Constants ---------------
EMPTY = 0
CONDUCTOR = 1
ELECTRON_HEAD = 2
ELECTRON_TAIL = 3

STATE_CHARS = {
    EMPTY: '.',
    CONDUCTOR: '#',
    ELECTRON_HEAD: 'H',
    ELECTRON_TAIL: 't',
}

CHAR_TO_STATE = {
    '.': EMPTY, '0': EMPTY, ' ': EMPTY,
    '#': CONDUCTOR, '1': CONDUCTOR,
    'H': ELECTRON_HEAD, '2': ELECTRON_HEAD,
    't': ELECTRON_TAIL, '3': ELECTRON_TAIL,
}

# --------------- Display Configuration ---------------
CELL_SIZE = 16          # pixels
WIDTH_BOX = 1021
HEIGHT_BOX = 663
GRID_WIDTH = 49         # cells
GRID_HEIGHT = 36        # cells
MARGIN = 1              # space between cells (visual)
TOP_UI_HEIGHT = 50      # pixels reserved for top bar
RIGTH_UI_WIDTH = 840     # pixels reserved for right bar (not used)
FPS = 60
DEFAULT_TPS = 6        # ticks per second during playback


# --------------- Colors ---------------
BG_COLOR = (20, 22, 28)
GRID_BG = (30, 33, 40)
COLORS = {
    EMPTY: (35, 38, 45),
    CONDUCTOR: (244, 208, 63),   
    ELECTRON_HEAD: (52, 152, 219),
    ELECTRON_TAIL: (231, 76, 60),
}
TEXT_COLOR = (230, 234, 240)
BUTTON_BG = (55, 60, 72)
BUTTON_BG_HOVER = (70, 76, 92)
BUTTON_BG_ACTIVE = (90, 160, 90)
BUTTON_TEXT = (240, 244, 250)
