import pygame

from typing import Tuple, Dict


class BaseGUIObject:
    def __init__(self, scene, rect=pygame.Rect(0, 0, 0, 0)):
        self.rect = rect
        """
        state = 0 - passive
        state = 1 - hovered
        state = 2 - pressed
        """
        self.state = 0
        self.scene = scene

    def update(self):
        pass

    def render(self, display):
        pass

    def click(self):
        pass

    def check_event(self, event):
        pass


class Button(BaseGUIObject):
    def __init__(self, pos: Tuple[int, int], width, height, text: Dict, func, scene, passive_state, hovered_state=None,
                 pressed_state=None):
        """
        ***_state = = {'color': (int, int, int, int), 'bd_color':  (int, int, int, int), 'bd_width': 1}
        text = {'text': '', 'size'=int, 'color'=(int, int, int), 'font'=opt('')}
        """
        self.pos = pos
        self.size = (height, width)

        self.func = func

        self.text = text
        self.text['font'] = text.get('font', 'arial')

        font = pygame.font.match_font(self.text['font'])
        font = pygame.font.Font(font, self.text['size'])
        self.text_surface = font.render(self.text['text'], True, self.text['color'])
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.pos

        super().__init__(scene, pygame.Rect(self.pos, (height * 2, width * 2)))
        self.rect.center = pos
        self.states = {0: passive_state}
        if hovered_state is not None:
            self.states.update([(1, hovered_state)])
        if pressed_state is not None:
            self.states.update([(2, pressed_state)])

    def render(self, display):
        settings = self.states.get(self.state, self.states.get(1, self.states[0]))

        pygame.draw.rect(display, settings['color'], self.rect)

        if settings['bd_width'] >= 1:
            pygame.draw.rect(display, settings['bd_color'], self.rect, settings['bd_width'])
        display.blit(self.text_surface, self.text_rect)

    def click(self):
        self.func()

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(*event.pos) or self.text_rect.collidepoint(*event.pos):
                self.state = 1
            else:
                self.state = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect.collidepoint(*event.pos) or self.text_rect.collidepoint(*event.pos):
                    self.click()
