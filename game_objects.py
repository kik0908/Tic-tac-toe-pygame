from math import ceil
from typing import Tuple

import pygame


class GameObject:
    def update(self):
        pass

    def render(self, display):
        pass


class GameUnit(GameObject):
    pass


class Cross(GameObject):
    def __init__(self, pos: Tuple[int, int], size: int, width=3, color=(255, 255, 255)):
        self.pos = pos
        self.size = size

        self.width = width
        self.color = color

        self.start_pos1 = (pos[0] - size, pos[1] - size)
        self.end_pos1 = (pos[0] + size, pos[1] + size)

        self.start_pos2 = (pos[0] - size, 2 * size + pos[1] - size)
        self.end_pos2 = (2 * size + pos[0] - size, pos[1] - size)

    def render(self, display):
        pygame.draw.line(display, self.color, self.start_pos1, self.end_pos1, self.width)
        pygame.draw.line(display, self.color, self.start_pos2, self.end_pos2, self.width)


class Circle(GameObject):
    def __init__(self, pos: Tuple[int, int], size: int, width=3, color=(255, 255, 255)):
        self.pos = pos
        self.size = size

        self.width = width
        self.color = color

    def render(self, display):
        pygame.draw.circle(display, self.color, self.pos, self.size, self.width)


class Grid(GameObject):
    def __init__(self, pos: Tuple[int, int], size_of_cell: int, num_of_cell: Tuple[int, int], width=3,
                 color=(255, 255, 255)):
        self.pos = pos
        self.cells_size = size_of_cell
        self.cells_count = num_of_cell

        self.width = width
        self.color = color

        self.dy = self.cells_count[0] * self.cells_size
        self.dx = self.cells_count[1] * self.cells_size

        self.dys = self.dy // num_of_cell[0]
        self.dxs = self.dx // num_of_cell[1]

        self.grid = [[GameObject() for j in range(num_of_cell[1])] for _ in range(num_of_cell[0])]

    def render(self, display):
        pygame.draw.lines(display, self.color, True,
                          [self.pos,
                           (self.pos[0] + self.dx, self.pos[1]),
                           (self.pos[0] + self.dx,
                            self.pos[1] + self.dy),
                           (self.pos[0], self.pos[1] + self.dy)],
                          self.width)

        for i in range(1, self.cells_count[0]):
            pygame.draw.line(display, self.color,
                             (self.pos[0], self.pos[1] + self.dys * i),
                             (self.pos[0] + self.dx, self.pos[1] + self.dys * i), self.width)

        for i in range(1, self.cells_count[1]):
            pygame.draw.line(display, self.color,
                             (self.pos[0] + self.dxs * i, self.pos[1]),
                             (self.pos[0] + self.dxs * i, self.pos[1] + self.dy), self.width)

        for i in self.grid:
            for obj in i:
                obj.render(display)

    def get_ceil_pos(self, x, y):
        if x < self.pos[0] or y < self.pos[1]:
            return None

        x -= self.pos[0]
        y -= self.pos[1]

        x_coord = ceil(x / self.cells_size) - 1
        x_coord = 0 if x_coord < 0 else x_coord

        y_coord = ceil(y / self.cells_size) - 1
        y_coord = 0 if y_coord < 0 else y_coord

        if x_coord < self.cells_count[0] and y_coord < self.cells_count[1]:
            return x_coord, y_coord
        else:
            return None

    def edit(self, x: int, y: int, obj: GameObject):
        self.grid[y][x] = obj

    def get_centre(self, x: int, y: int):
        a = self.pos[0] + self.cells_size * (x + 1) - round(self.cells_size / 2)
        b = self.pos[1] + self.cells_size * (y + 1) - round(self.cells_size / 2)
        return a, b


class TicTacToeGrid(Grid):
    win_pos = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def check_win(self):
        pass
