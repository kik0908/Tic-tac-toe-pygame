import pygame
from game_objects import Cross, Circle, Grid, TicTacToeGrid


WIDTH = 360
HEIGHT = 480
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

gr = TicTacToeGrid((0, 0), 100, (3, 3), width=2)
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
            # x, y = gr.get_ceil_pos(*pygame.mouse.get_pos())
            # a, b = gr.get_centre(x, y)
            # gr.edit(x, y, Cross((a, b), 20))
            if gr.check_click(event.pos):
                gr.click(event.button, event.pos)

    gr.render(screen)
    pygame.display.flip()

pygame.quit()
