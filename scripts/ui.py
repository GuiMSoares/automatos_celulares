"""UI components for the WireWorld application."""

import pygame
from pygame import Rect
from typing import Tuple, List
from constants import (
    BUTTON_BG, BUTTON_BG_HOVER, BUTTON_BG_ACTIVE, BUTTON_TEXT,
    BG_COLOR, GRID_BG, COLORS, TEXT_COLOR, WIDTH_BOX, HEIGHT_BOX,
    CELL_SIZE, MARGIN, TOP_UI_HEIGHT,RIGTH_UI_WIDTH, EMPTY
)


class Button:
    """A clickable button widget."""
    
    def __init__(self, rect: Rect, label: str, on_click):
        self.rect = Rect(rect)
        self.label = label
        self.on_click = on_click
        self.hover = False
        self.active = False

    def draw(self, surf, font):
        """Draw the button on the given surface."""
        
        bg = BUTTON_BG_ACTIVE if self.active else (BUTTON_BG_HOVER if self.hover else BUTTON_BG)
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        text = font.render(self.label, True, BUTTON_TEXT)
        text_rect = text.get_rect(center=self.rect.center)
        surf.blit(text, text_rect)

    def handle_event(self, event):
        """Handle mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


def pixel_to_cell(pos: Tuple[int, int], grid_width: int, grid_height: int) -> Tuple[int | None, int | None]:
    """Convert pixel coordinates to grid cell coordinates."""
    x, y = pos
    if y < TOP_UI_HEIGHT:
        return (None, None)
    y -= TOP_UI_HEIGHT
    cell_w = CELL_SIZE + MARGIN
    cell_h = CELL_SIZE + MARGIN
    gx = (x - MARGIN) // cell_w
    gy = (y - MARGIN) // cell_h
    if 0 <= gx < grid_width and 0 <= gy < grid_height:
        # within cell bounds; also ensures not in margin space
        cx = MARGIN + gx * cell_w
        cy = MARGIN + gy * cell_h
        if (x >= cx and x < cx + CELL_SIZE) and (y >= cy and y < cy + CELL_SIZE):
            return int(gx), int(gy)
    return (None, None)


def draw_ui(screen, buttons: List[Button], font, small_font, generation: int, tps: int, 
           brush: int, running: bool, mouse_grid_pos: Tuple[int | None, int | None]):
    """Draw the top UI bar with buttons and information."""
    # Top bar background
    pygame.draw.rect(screen, GRID_BG, Rect(0, 0, screen.get_width(), TOP_UI_HEIGHT))
    
    # Draw buttons
    for b in buttons:
        if b.label == 'Play/Pause':
            b.active = running
        b.draw(screen, font)

    # Information text
    brush_names = {EMPTY: 'EMPTY', 1: 'COND', 2: 'HEAD', 3: 'TAIL'}
    info = f"Gen: {generation}  TPS: {tps}  Brush: {brush_names.get(brush, 'UNK')}  Running: {running}"
    
    # Add mouse position if over grid
    if mouse_grid_pos[0] is not None:
        info += f"  Mouse: ({mouse_grid_pos[0]}, {mouse_grid_pos[1]})"
    
    text = small_font.render(info, True, TEXT_COLOR)
    screen.blit(text, (10, TOP_UI_HEIGHT - 22))


def draw_grid(screen, grid: List[List[int]], mouse_grid_pos: Tuple[int | None, int | None]):
    """Draw the cellular automaton grid."""
    grid_height = len(grid)
    grid_width = len(grid[0]) if grid_height else 0
    
    # Draw cells
    for y in range(grid_height):
        for x in range(grid_width):
            state = grid[y][x]
            color = COLORS.get(state, COLORS[EMPTY])
            px = MARGIN + x * (CELL_SIZE + MARGIN)
            py = TOP_UI_HEIGHT + MARGIN + y * (CELL_SIZE + MARGIN)
            
            # Highlight cell under mouse cursor
            if mouse_grid_pos == (x, y):
                # Draw a slightly brighter version of the color
                highlight_color = tuple(min(255, c + 30) for c in color)
                pygame.draw.rect(screen, highlight_color, Rect(px, py, CELL_SIZE, CELL_SIZE), border_radius=3)
                # Draw a thin border
                pygame.draw.rect(screen, (255, 255, 255), Rect(px, py, CELL_SIZE, CELL_SIZE), width=1, border_radius=3)
            else:
                pygame.draw.rect(screen, color, Rect(px, py, CELL_SIZE, CELL_SIZE), border_radius=3)


def draw_frame(screen, grid: List[List[int]], buttons: List[Button], font, small_font,
              generation: int, tps: int, brush: int, running: bool, 
              mouse_grid_pos: Tuple[int | None, int | None]):
    """Draw a complete frame of the application."""
    screen.fill(GRID_BG)
    draw_ui(screen, buttons, font, small_font, generation, tps, brush, running, mouse_grid_pos)
    draw_grid(screen, grid, mouse_grid_pos)
    pygame.display.flip()
