from math import ceil
from typing import Tuple, Dict

import pygame


class GameObject:
    def __init__(self, scene=None, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)):
        self.rect = rect

        self.scene = scene

    def update(self):
        pass

    def render(self, display):
        pass

    def click(self, event):
        pass

    def check_event(self, event):
        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            return self.rect.collidepoint(*event.pos)


class GameUnit(GameObject):
    def __init__(self, kind=None, scene=None):
        super().__init__(scene)
        self.value = kind

    def __eq__(self, other):
        if type(other) == type(self):
            return True
        return False

    def __ne__(self, other):
        if type(other) != type(self):
            return True
        return False


class Cross(GameUnit):
    def __init__(self, pos: Tuple[int, int], size: int, width=3, color=(255, 255, 255), scene=None):
        super().__init__('x', scene)

        self.pos = pos
        self.size = size

        self.width = width
        self.color = color

        self.start_pos1 = (pos[0] - size, pos[1] - size)
        self.end_pos1 = (pos[0] + size, pos[1] + size)

        self.rect = pygame.Rect(self.start_pos1, (size * 2 + width, size * 2 + width))

        self.start_pos2 = (pos[0] - size, 2 * size + pos[1] - size)
        self.end_pos2 = (2 * size + pos[0] - size, pos[1] - size)

    def render(self, display):
        pygame.draw.line(display, self.color, self.start_pos1, self.end_pos1, self.width)
        pygame.draw.line(display, self.color, self.start_pos2, self.end_pos2, self.width)


class Circle(GameUnit):
    def __init__(self, pos: Tuple[int, int], size: int, width=3, color=(255, 255, 255), scene=None):
        super().__init__('o', scene)

        self.pos = pos
        self.size = size

        self.rect = pygame.Rect(pos[0] - size, pos[1] - size, size * 2 + width, size * 2 + width)

        self.width = width
        self.color = color

    def render(self, display):
        pygame.draw.circle(display, self.color, self.pos, self.size, self.width)


class Grid(GameObject):
    def __init__(self, pos: Tuple[int, int], size_of_cell: int, num_of_cell: Tuple[int, int], width=3,
                 color=(255, 255, 255), scene=None):
        super().__init__(scene)

        self.pos = pos
        self.cells_size = size_of_cell
        self.cells_count = num_of_cell

        self.width = width
        self.color = color

        self.dy = self.cells_count[0] * self.cells_size
        self.dx = self.cells_count[1] * self.cells_size

        self.dys = self.dy // num_of_cell[0]
        self.dxs = self.dx // num_of_cell[1]

        self.grid = [[GameObject() for _ in range(num_of_cell[1])] for _ in range(num_of_cell[0])]

        self.rect = pygame.Rect(pos, (size_of_cell * num_of_cell[0] + width, size_of_cell * num_of_cell[1] + width))

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
        self.grid[x][y] = obj
        return True

    def get_centre(self, x: int, y: int):
        a = self.pos[0] + self.cells_size * (x + 1) - round(self.cells_size / 2)
        b = self.pos[1] + self.cells_size * (y + 1) - round(self.cells_size / 2)
        return a, b


class TicTacToeGrid(Grid):
    def __init__(self, pos: Tuple[int, int], size_of_cell: int, num_of_cell: Tuple[int, int], width=3,
                 color=(255, 255, 255), scene=None):
        super().__init__(pos, size_of_cell, num_of_cell, width, color, scene)

        self.grid = [[GameUnit() for _ in range(self.cells_count[1])] for _ in range(self.cells_count[0])]

        self.__n_char = 0
        self.__chars = (Cross, Circle)

        self.unit_settings = {'width': width, 'color': color, 'size': round(size_of_cell * 40 / 100)}

    def set_unit_settings(self, settings: Dict):
        self.unit_settings = settings

    def edit(self, x, y, obj):
        if self.grid[x][y] == GameUnit():
            super().edit(x, y, obj)
            return True
        return False

        # return super().edit(x, y, obj)

    def check_win(self):
        ans_x = [[], []]
        ans_o = [[], []]
        for i in range(self.cells_count[0]):
            ans_x[0].append(self.grid[i][i].value == 'x')
            ans_o[0].append(self.grid[i][i].value == 'o')

            ans_x[1].append(self.grid[self.cells_count[0] - i - 1][i].value == 'x')
            ans_o[1].append(self.grid[self.cells_count[0] - i - 1][i].value == 'o')
        if any(map(lambda x: all(x), ans_x)):
            return 'x'
        elif any(map(lambda x: all(x), ans_o)):
            return 'o'

        ans_x = []
        ans_o = []
        for i in self.grid:
            ans_x.append(all(map(lambda x: x.value == 'x', i)))
            ans_o.append(all(map(lambda x: x.value == 'o', i)))
        if any(ans_x):
            return 'x'
        elif any(ans_o):
            return 'o'

        ans_x = []
        ans_o = []
        for i in range(self.cells_count[1]):
            _1, _2 = [], []
            for j in range(self.cells_count[0]):
                _1.append(self.grid[j][i].value == 'x')
                _2.append(self.grid[j][i].value == 'o')

            ans_x.append(all(_1))
            ans_o.append(all(_2))
        if any(ans_x):
            return 'x'
        elif any(ans_o):
            return 'o'

        _c = 0
        for i in self.grid:
            for j in i:
                if j != GameUnit():
                    _c += 1
        if _c == self.cells_count[0] * self.cells_count[1]:
            print('123421')
            return 'b'

    @property
    def char(self):
        return self.__chars[self.__n_char]

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            but, pos = event.button, event.pos
            if but == 1:
                coords = self.get_ceil_pos(*pos)
                char = self.char

                pos = self.get_centre(*coords)

                if self.edit(*coords, char(pos, self.unit_settings['size'], self.unit_settings['width'],
                                           self.unit_settings['color'])):
                    self.__n_char = not self.__n_char
                    ans = self.check_win()
                    if ans is not None:
                        self.scene.callback('player_win', {'char': ans})
