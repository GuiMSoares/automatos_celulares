from __future__ import annotations
import os
import sys
import pygame
from pygame import Rect
from typing import List, Tuple

# --------------- Constantes de estado do WireWorld ---------------
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

# --------------- Configurações ---------------
CELL_SIZE = 16          # pixels
GRID_WIDTH = 60         # células
GRID_HEIGHT = 36        # células
MARGIN = 1              # espaço entre células (visual)
TOP_UI_HEIGHT = 50      # pixels reservados para barra superior
FPS = 60
DEFAULT_TPS = 10        # ticks por segundo durante reprodução

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

# --------------- Funções auxiliares ---------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

# --------------- Manipulação da grade ---------------
def new_grid(w: int, h: int, fill: int = EMPTY) -> List[List[int]]:
    return [[fill for _ in range(w)] for _ in range(h)]


def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]


def load_state(path: str) -> List[List[int]]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    maxlen = max((len(line) for line in lines), default=0)
    grid = []
    for line in lines:
        row = [CHAR_TO_STATE.get(ch, EMPTY) for ch in line]
        if len(row) < maxlen:
            row.extend([EMPTY] * (maxlen - len(row)))
        grid.append(row)
    return grid


def save_state(path: str, grid: List[List[int]]):
    with open(path, 'w', encoding='utf-8') as f:
        for row in grid:
            f.write(''.join(STATE_CHARS.get(cell, '.') for cell in row) + '\n')


# --------------- Atualização do WireWorld ---------------
def count_head_neighbors(grid: List[List[int]], x: int, y: int) -> int:
    h = len(grid)
    w = len(grid[0]) if h else 0
    cnt = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] == ELECTRON_HEAD:
                    cnt += 1
    return cnt


def step_wireworld(grid: List[List[int]]) -> List[List[int]]:
    h = len(grid)
    w = len(grid[0]) if h else 0
    nextg = new_grid(w, h, EMPTY)
    for y in range(h):
        for x in range(w):
            cell = grid[y][x]
            if cell == EMPTY:
                nextg[y][x] = EMPTY
            elif cell == ELECTRON_HEAD:
                nextg[y][x] = ELECTRON_TAIL
            elif cell == ELECTRON_TAIL:
                nextg[y][x] = CONDUCTOR
            elif cell == CONDUCTOR:
                heads = count_head_neighbors(grid, x, y)
                nextg[y][x] = ELECTRON_HEAD if heads in (1, 2) else CONDUCTOR
    return nextg


# --------------- Componentes da Interface ---------------
class Button:
    def __init__(self, rect: Rect, label: str, on_click):
        self.rect = Rect(rect)
        self.label = label
        self.on_click = on_click
        self.hover = False
        self.active = False

    def draw(self, surf, font):
        bg = BUTTON_BG_ACTIVE if self.active else (BUTTON_BG_HOVER if self.hover else BUTTON_BG)
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        text = font.render(self.label, True, BUTTON_TEXT)
        text_rect = text.get_rect(center=self.rect.center)
        surf.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


# --------------- Aplicação Principal ---------------
class WireWorldApp:
    def __init__(self, initial_file: str | None):
        pygame.init()
        self.font = pygame.font.SysFont('consolas', 18)
        self.small_font = pygame.font.SysFont('consolas', 14)

        self.grid = new_grid(GRID_WIDTH, GRID_HEIGHT, EMPTY)
        self.initial_grid = copy_grid(self.grid)
        self.running = False
        self.tps = DEFAULT_TPS
        self.accumulator = 0.0
        self.generation = 0
        self.brush = CONDUCTOR  # pincel padrão
        self.mouse_grid_pos = (None, None)  # rastrear posição do mouse na grade

        if initial_file and os.path.exists(initial_file):
            try:
                loaded = load_state(initial_file)
                self.resize_to_loaded(loaded)
                self.grid = loaded
                self.initial_grid = copy_grid(self.grid)
            except Exception as e:
                print(f"Falha ao carregar '{initial_file}': {e}")

        # tamanho da janela
        w = GRID_WIDTH * (CELL_SIZE + MARGIN) + MARGIN
        h = TOP_UI_HEIGHT + GRID_HEIGHT * (CELL_SIZE + MARGIN) + MARGIN
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("WireWorld — Pygame Template")

        # botões
        self.buttons: List[Button] = []
        self.create_buttons()

        self.clock = pygame.time.Clock()

    def resize_to_loaded(self, loaded: List[List[int]]):
        global GRID_WIDTH, GRID_HEIGHT
        GRID_HEIGHT = len(loaded)
        GRID_WIDTH = len(loaded[0]) if GRID_HEIGHT else 0

    def create_buttons(self):
        x = 10
        y = 8
        bw = 110
        bh = 34
        gap = 8
        def add(label, cb):
            nonlocal x
            self.buttons.append(Button(Rect(x, y, bw, bh), label, cb))
            x += bw + gap
        add('Play/Pause', self.toggle_running)
        add('Step', self.step_once)
        add('Reset', self.reset)
        add('Load', self.prompt_load)
        add('Save', self.prompt_save)
        add('Speed -', lambda: self.set_speed(self.tps - 1))
        add('Speed +', lambda: self.set_speed(self.tps + 1))
        add('Demo', self.create_demo_pattern)

    # ------------- Ações -------------
    def toggle_running(self):
        self.running = not self.running

    def step_once(self):
        self.grid = step_wireworld(self.grid)
        self.generation += 1

    def reset(self):
        self.grid = copy_grid(self.initial_grid)
        self.generation = 0
        self.running = False

    def set_speed(self, tps):
        self.tps = clamp(int(tps), 1, 120)

    def create_demo_pattern(self):
        """Cria um padrão de demonstração simples"""
        # Limpa a grade
        self.grid = new_grid(GRID_WIDTH, GRID_HEIGHT, EMPTY)
        
        # Cria um fio horizontal com um elétron
        y = GRID_HEIGHT // 2
        for x in range(10, 30):
            self.grid[y][x] = CONDUCTOR
        
        # Adiciona um elétron no início
        self.grid[y][12] = ELECTRON_HEAD
        self.grid[y][11] = ELECTRON_TAIL
        
        # Cria um segundo padrão - loop pequeno
        loop_y = GRID_HEIGHT // 2 - 8
        loop_x = 15
        # Faz um quadrado pequeno
        for i in range(6):
            self.grid[loop_y][loop_x + i] = CONDUCTOR     # topo
            self.grid[loop_y + 5][loop_x + i] = CONDUCTOR # baixo
            self.grid[loop_y + i][loop_x] = CONDUCTOR     # esquerda  
            self.grid[loop_y + i][loop_x + 5] = CONDUCTOR # direita
        
        # Adiciona elétron no loop
        self.grid[loop_y][loop_x + 1] = ELECTRON_HEAD
        self.grid[loop_y][loop_x + 2] = ELECTRON_TAIL
        
        # Atualiza o estado inicial
        self.initial_grid = copy_grid(self.grid)
        self.generation = 0
        self.running = False
        print("Padrão de demonstração criado! Pressione Play para ver a simulação.")

    def prompt_load(self):
        path = input("Digite o caminho para carregar (.txt): ").strip()
        if path and os.path.exists(path):
            try:
                loaded = load_state(path)
                self.resize_to_loaded(loaded)
                self.grid = loaded
                self.initial_grid = copy_grid(self.grid)
                self.recreate_window()
                self.generation = 0
                print(f"Carregado {path}")
            except Exception as e:
                print(f"Erro ao carregar: {e}")
        else:
            print("Arquivo não encontrado.")

    def prompt_save(self):
        path = input("Digite o caminho para salvar (.txt): ").strip()
        if path:
            try:
                save_state(path, self.grid)
                print(f"Salvo em {path}")
            except Exception as e:
                print(f"Erro ao salvar: {e}")

    def recreate_window(self):
        w = GRID_WIDTH * (CELL_SIZE + MARGIN) + MARGIN
        h = TOP_UI_HEIGHT + GRID_HEIGHT * (CELL_SIZE + MARGIN) + MARGIN
        self.screen = pygame.display.set_mode((w, h))
        self.buttons.clear()
        self.create_buttons()

    # ------------- Manipulação de Eventos -------------
    def handle_mouse_grid(self, pos, button, shift=False):
        gx, gy = self.pixel_to_cell(pos)
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

    def pixel_to_cell(self, pos: Tuple[int,int]) -> Tuple[int | None, int | None]:
        x, y = pos
        if y < TOP_UI_HEIGHT:
            return (None, None)
        y -= TOP_UI_HEIGHT
        cell_w = CELL_SIZE + MARGIN
        cell_h = CELL_SIZE + MARGIN
        gx = (x - MARGIN) // cell_w
        gy = (y - MARGIN) // cell_h
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            # dentro dos limites da célula; também garante que não está no espaço da margem
            cx = MARGIN + gx * cell_w
            cy = MARGIN + gy * cell_h
            if (x >= cx and x < cx + CELL_SIZE) and (y >= cy and y < cy + CELL_SIZE):
                return int(gx), int(gy)
        return (None, None)

    def handle_key(self, event):
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
        elif event.key == pygame.K_d:
            self.create_demo_pattern()

    # ------------- Loop Principal -------------
    def run(self):
        running_flag = True
        while running_flag:
            dt_ms = self.clock.tick(FPS)
            dt = dt_ms / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_flag = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running_flag = False
                    else:
                        self.handle_key(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # encaminha para botões primeiro
                    for b in self.buttons:
                        b.handle_event(event)
                    # depois para a grade
                    shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
                    self.handle_mouse_grid(event.pos, event.button, shift)
                elif event.type == pygame.MOUSEMOTION:
                    for b in self.buttons:
                        b.handle_event(event)
                    # Atualiza posição do mouse na grade para exibição
                    self.mouse_grid_pos = self.pixel_to_cell(event.pos)

            # atualiza simulação
            if self.running:
                self.accumulator += dt
                tick_len = 1.0 / max(self.tps, 1)
                while self.accumulator >= tick_len:
                    self.grid = step_wireworld(self.grid)
                    self.generation += 1
                    self.accumulator -= tick_len

            # desenha
            self.draw()

        pygame.quit()

    # ------------- Desenho -------------
    def draw(self):
        self.screen.fill(BG_COLOR)
        # barra superior
        pygame.draw.rect(self.screen, GRID_BG, Rect(0, 0, self.screen.get_width(), TOP_UI_HEIGHT))
        for b in self.buttons:
            if b.label == 'Play/Pause':
                b.active = self.running
            b.draw(self.screen, self.font)

        info = f"Gen: {self.generation}  TPS: {self.tps}  Brush: {self.brush_name()}  Running: {self.running}"
        # Adiciona posição do mouse se estiver sobre a grade
        if self.mouse_grid_pos[0] is not None:
            info += f"  Mouse: ({self.mouse_grid_pos[0]}, {self.mouse_grid_pos[1]})"
        text = self.small_font.render(info, True, TEXT_COLOR)
        self.screen.blit(text, (10, TOP_UI_HEIGHT - 22))

        # área da grade
        gx0 = 0
        gy0 = TOP_UI_HEIGHT
        pygame.draw.rect(self.screen, GRID_BG, Rect(gx0, gy0, self.screen.get_width(), self.screen.get_height() - gy0))

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                state = self.grid[y][x]
                color = COLORS.get(state, COLORS[EMPTY])
                px = MARGIN + x * (CELL_SIZE + MARGIN)
                py = gy0 + MARGIN + y * (CELL_SIZE + MARGIN)
                
                # Destaca célula sob o cursor do mouse
                if self.mouse_grid_pos == (x, y):
                    # Desenha uma versão ligeiramente mais brilhante da cor
                    highlight_color = tuple(min(255, c + 30) for c in color)
                    pygame.draw.rect(self.screen, highlight_color, Rect(px, py, CELL_SIZE, CELL_SIZE), border_radius=3)
                    # Desenha uma borda fina
                    pygame.draw.rect(self.screen, (255, 255, 255), Rect(px, py, CELL_SIZE, CELL_SIZE), width=1, border_radius=3)
                else:
                    pygame.draw.rect(self.screen, color, Rect(px, py, CELL_SIZE, CELL_SIZE), border_radius=3)

        pygame.display.flip()

    def brush_name(self) -> str:
        return {EMPTY: 'EMPTY', CONDUCTOR: 'COND', ELECTRON_HEAD: 'HEAD', ELECTRON_TAIL: 'TAIL'}[self.brush]


# --------------- Ponto de entrada ---------------
def main():
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    app = WireWorldApp(initial_file)
    app.run()


if __name__ == '__main__':
    main()
