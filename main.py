import pygame

import scenes
from game_objects import Cross, Circle, Grid, TicTacToeGrid

WIDTH = 500
HEIGHT = 500
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


scene_manager = scenes.SceneManager(screen)
scene_manager.new_scene(scenes.MainGame(screen, scene_manager))
# gr = TicTacToeGrid((0, 0), 100, (3, 3), width=2)
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     # elif event.type == pygame.MOUSEBUTTONDOWN:
    #     #     if gr.check_event(event):
    #     #         gr.click(event)

    # gr.render(screen)
    scene_manager.next_step(pygame.event.get())
    pygame.display.flip()

pygame.quit()
