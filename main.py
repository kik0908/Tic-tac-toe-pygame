import pygame

import scenes

WIDTH = 302
HEIGHT = 357
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-tac-toe")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

scene_manager = scenes.SceneManager(screen)
scene_manager.new_scene(scenes.MainMenu(screen, scene_manager))

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    events = pygame.event.get()
    scene_manager.next_step(events)

    pygame.display.flip()

pygame.quit()
