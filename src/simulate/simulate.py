import time
import pygame
from ..board import boards
from ..run import Run
from .T40 import drone

# Constants
WIDTH = 1200
HEIGHT = 800

COLOR_WHITE = (255, 255, 255)

# Initialize all


def init():
    pygame.init()
    pygame.key.set_repeat((1 * 1000) // 30)

    # Initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    field_type = 1
    return screen, field_type


def critical():
    print("Fuck You!", flush=True)


screen, field_type = init()

board = boards[field_type]
board.to_nparray()

field = pygame.surfarray.make_surface(board.to_nparray())

run = Run(board, drone, board.terminals[0], critical)

# filled = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# newfill = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


def draw_reset():
    screen.fill(COLOR_WHITE)
    screen.blit(field, (0, 0))

draw_reset()

cnt = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    # draw_reset()
    run.set_movement((0, 1))
    run.calculate(screen, 1)

    # filled_arr = pygame.surfarray.array2d(filled)
    # newfill_arr = pygame.surfarray.array2d(newfill)
    # filled_arr = np.add(filled_arr, newfill_arr, casting="safe")
    # filled = pygame.surfarray.make_surface(filled_arr)
    # newfill = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)

    screen.blit(screen, (0, 0))
    run.draw_drone(screen)
    pygame.display.update()
    
    cnt += 1
    battery = drone.battery.remaining
    print(cnt, battery)

    time.sleep(0.01)
