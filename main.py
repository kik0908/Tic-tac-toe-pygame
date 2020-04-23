import pygame

import scenes
from game_objects import Cross, Circle, Grid, TicTacToeGrid
from gui import Button, Label

WIDTH = 302
HEIGHT = 357
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-tac-toe")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


scene_manager = scenes.SceneManager(screen)
scene_manager.new_scene(scenes.MainMenu(screen, scene_manager))


running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    aa = pygame.event.get()
    scene_manager.next_step(aa)

    pygame.display.flip()

pygame.quit()
