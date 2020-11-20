import pygame
from pygame.locals import *
import copy
class Cell:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.is_alive = False
    
    def animate(self) -> None:
        self.is_alive = True

    def kill(self) -> None:
        self.is_alive = False    

class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, delay: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.cells = [[] for i in range(self.cell_width)]
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                self.cells[i].append(Cell(i,j))
        self.cells[4][4].animate()
        self.cells[4][3].animate()
        self.cells[4][5].animate()
        self.cells[3][3].animate()

        self.cells[2][4].animate()
        # Скорость протекания игры
        self.delay = delay
    def get_neighbours(self, cell) -> int:
        result = 0
        coords = [(cell.x-1,cell.y-1), (cell.x-1,cell.y), (cell.x-1,cell.y+1), (cell.x,cell.y-1), (cell.x,cell.y+1), (cell.x+1,cell.y-1), (cell.x+1,cell.y), (cell.x+1,cell.y+1)]
        for coord in coords:
            if 0 <= coord[0] <= self.cell_width-1 and 0 <= coord[1] <= self.cell_height-1:
                if self.cells[coord[0]][coord[1]].is_alive:
                    result += 1 
        return result
    def refresh_cells(self) -> None:
        cells = copy.deepcopy(self.cells)
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if self.get_neighbours(self.cells[i][j]) > 3 or self.get_neighbours(self.cells[i][j]) < 2:
                    cells[i][j].kill()
                if self.get_neighbours(self.cells[i][j]) == 3:
                    cells[i][j].animate()
        self.cells=cells
    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))
    
    def draw_cells(self) -> None:
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if self.cells[i][j].is_alive:
                    pygame.draw.rect(self.screen, pygame.Color('forestgreen'), (self.cells[i][j].x * self.cell_size + 1, self.cells[i][j].y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
    def initial(self) -> None:
        pygame.init()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
   
        running = True
        while running: 
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()             
                    self.cells[x//self.cell_size][y//self.cell_size].animate()
                    pygame.draw.rect(self.screen, pygame.Color('forestgreen'), (x//self.cell_size*self.cell_size + 1, y//self.cell_size*self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                if event.type == QUIT:
                    running = False
                if event.type == KEYUP:
                    self.run()
                    running=False
            self.draw_lines()
            self.draw_cells()
            pygame.display.flip()
    
    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_cells()
            self.refresh_cells()
            pygame.display.flip()
            pygame.time.delay(self.delay)
        pygame.quit()


if __name__ == '__main__':
    n=100
    game = GameOfLife(16*n, 10*n, 20)
    game.initial()