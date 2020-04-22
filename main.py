import pygame
from game_objects import Cross, Circle, Grid


WIDTH = 360
HEIGHT = 480
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

gr = Grid((0, 0), 50, (3, 3), width=2)
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = gr.get_ceil_pos(*pygame.mouse.get_pos())
            a, b = gr.get_centre(x, y)
            gr.add(x, y, Cross((a, b), 20))

    gr.render(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
