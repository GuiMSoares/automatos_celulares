"""Main WireWorld application class."""

import os
import pygame
from pygame import Rect
from typing import List, Tuple

from constants import (
    GRID_WIDTH, WIDTH_BOX, GRID_HEIGHT, HEIGHT_BOX, CELL_SIZE, MARGIN, TOP_UI_HEIGHT, FPS, DEFAULT_TPS,
    EMPTY, CONDUCTOR, ELECTRON_HEAD, ELECTRON_TAIL
)
from wireworld import (
    new_grid, copy_grid, load_state, save_state, step_wireworld, clamp
)
from ui import Button, pixel_to_cell, draw_frame


class WireWorldApp:
    """Main application class for the WireWorld cellular automaton."""
    
    def __init__(self, initial_file: str | None):
        pygame.init()
        self.font = pygame.font.SysFont('consolas', 18)
        self.small_font = pygame.font.SysFont('consolas', 14)

        # Initialize grid state
        self.grid = new_grid(GRID_WIDTH, GRID_HEIGHT, EMPTY)
        self.initial_grid = copy_grid(self.grid)
        self.running = False
        self.tps = DEFAULT_TPS
        self.accumulator = 0.0
        self.generation = 0
        self.brush = CONDUCTOR  # default brush
        self.mouse_grid_pos = (None, None)  # track mouse position on grid

        # Load initial file if provided
        if initial_file and os.path.exists(initial_file):
            try:
                loaded = load_state(initial_file)
                self.resize_to_loaded(loaded)
                self.grid = loaded
                self.initial_grid = copy_grid(self.grid)
            except Exception as e:
                print(f"Failed to load '{initial_file}': {e}")

        # Create window
        self._create_window()
        pygame.display.set_caption("WireWorld — Pygame Template")

        # Create UI buttons
        self.buttons: List[Button] = []
        self.create_buttons()

        self.clock = pygame.time.Clock()

    def _create_window(self):
        """Create the main window based on current grid size."""
        #w = GRID_WIDTH * (CELL_SIZE + MARGIN) + MARGIN
        #h = TOP_UI_HEIGHT + GRID_HEIGHT * (CELL_SIZE + MARGIN) + MARGIN
        self.screen = pygame.display.set_mode((WIDTH_BOX, HEIGHT_BOX))

    def resize_to_loaded(self, loaded: List[List[int]]):
        """Resize grid dimensions to match loaded state."""
        #global GRID_WIDTH, GRID_HEIGHT
        HEIGHT_BOX = len(loaded)
        WIDTH_BOX = len(loaded[0]) if GRID_HEIGHT else 0

    def create_buttons(self):
        """Create UI buttons."""
        x = 10
        y = 8
        bw = 110
        bh = 34
        gap = 8

        aw = 175
        
        def add(label, callback, KEY):
            nonlocal x
            nonlocal y
            if KEY:
                self.buttons.append(Button(Rect(x, y, bw, bh), label, callback))
                x += bw + gap
            
            else:
                self.buttons.append(Button(Rect(x, y, aw, bh), label, callback))
                y += bh + gap
        
        add('Play/Pause', self.toggle_running, True)
        add('Step', self.step_once, True)
        add('Reset', self.reset, True)
        add('Load', self.prompt_load, True)
        add('Save', self.prompt_save, True)
        add('Speed -', lambda: self.set_speed(self.tps - 1), True)
        add('Speed +', lambda: self.set_speed(self.tps + 1), True)
        #add('examples:', self.examples("..\gates\gate-and.txt"), False)
        #add('NOT', self.examples("..\gates\gate-not.txt"), False)
        #add('OR', self.examples("..\gates\gate-or.txt"), False)
        #add('AND', self.examples("..\gates\gate-and.txt"), False)
        #add('XOR', self.examples("..\gates\gate-xor.txt"), False)
        #add('Flip-Flop', self.examples("..\gates\gate-flip-flop.txt"), False)
        

    # ------------- Actions -------------
    def toggle_running(self):
        """Toggle simulation running state."""
        self.running = not self.running

    def step_once(self):
        """Perform one simulation step."""
        self.grid = step_wireworld(self.grid)
        self.generation += 1

    def reset(self):
        """Reset to initial state."""
        self.grid = copy_grid(self.initial_grid)
        self.generation = 0
        self.running = False

    def set_speed(self, tps):
        """Set simulation speed (ticks per second)."""
        self.tps = clamp(int(tps), 1, 120)

    def prompt_load(self):
        """Prompt user to load a file."""
        path = input("Enter path to load (.txt): ").strip()
        if path and os.path.exists(path):
            try:
                loaded = load_state(path)
                self.resize_to_loaded(loaded)
                self.grid = loaded
                self.initial_grid = copy_grid(self.grid)
                self.recreate_window()
                self.generation = 0
                print(f"Loaded {path}")
            except Exception as e:
                print(f"Error loading: {e}")
        else:
            print("File not found.")

    def prompt_save(self):
        """Prompt user to save the current state."""
        path = input("Enter path to save (.txt): ").strip()
        if path:
            try:
                save_state(path, self.grid)
                print(f"Saved to {path}")
            except Exception as e:
                print(f"Error saving: {e}")

    def examples(self, path):
        """Load a predefined example from the given path."""
        try:
            loaded = load_state(path)
            self.resize_to_loaded(loaded)
            self.grid = loaded
            self.initial_grid = copy_grid(self.grid)
            self.recreate_window()
            self.generation = 0
            print(f"{path} example loaded.")
        except Exception as e:
            print(f"Error loading: {e}")
    

    def recreate_window(self):
        """Recreate window and buttons after grid resize."""
        self._create_window()
        self.buttons.clear()
        self.create_buttons()

    # ------------- Event Handling -------------
    def handle_mouse_grid(self, pos, button, shift=False):
        """Handle mouse interaction with the grid."""
        gx, gy = pixel_to_cell(pos, GRID_WIDTH, GRID_HEIGHT)
        if gx is None:
            return
        
        if button == 1 and not shift:
            self.grid[gy][gx] = self.brush
        elif button == 1 and shift:
            self.grid[gy][gx] = (self.grid[gy][gx] + 1) % 4
        elif button == 2:
            self.grid[gy][gx] = (self.grid[gy][gx] + 1) % 4
        elif button == 3:
            self.grid[gy][gx] = EMPTY

    def handle_key(self, event):
        """Handle keyboard input."""
        if event.key == pygame.K_SPACE:
            self.toggle_running()
        elif event.key == pygame.K_n:
            self.step_once()
        elif event.key == pygame.K_r:
            self.reset()
        elif event.key == pygame.K_l:
            self.prompt_load()
        elif event.key == pygame.K_s:
            self.prompt_save()
        elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
            self.set_speed(self.tps + 1)
        elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
            self.set_speed(self.tps - 1)
        elif event.key == pygame.K_1:
            self.brush = EMPTY
        elif event.key == pygame.K_2:
            self.brush = CONDUCTOR
        elif event.key == pygame.K_3:
            self.brush = ELECTRON_HEAD
        elif event.key == pygame.K_4:
            self.brush = ELECTRON_TAIL
        
    # ------------- Main Loop -------------
    def run(self):
        """Run the main application loop."""
        running_flag = True
        while running_flag:
            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_flag = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running_flag = False
                    else:
                        self.handle_key(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Forward to buttons first
                    for b in self.buttons:
                        b.handle_event(event)
                    # Then to grid
                    shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
                    self.handle_mouse_grid(event.pos, event.button, shift)
                elif event.type == pygame.MOUSEMOTION:
                    for b in self.buttons:
                        b.handle_event(event)
                    # Update mouse position on grid for display
                    self.mouse_grid_pos = pixel_to_cell(event.pos, GRID_WIDTH, GRID_HEIGHT)

            # Update simulation
            if self.running:
                self.accumulator += dt
                tick_len = 1.0 / max(self.tps, 1)
                while self.accumulator >= tick_len:
                    self.grid = step_wireworld(self.grid)
                    self.generation += 1
                    self.accumulator -= tick_len

            # Draw
            draw_frame(self.screen, self.grid, self.buttons, self.font, self.small_font,
                      self.generation, self.tps, self.brush, self.running, self.mouse_grid_pos)

        pygame.quit()
