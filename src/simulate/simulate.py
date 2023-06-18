import time
import pygame
import copy
from ..board import boards, Point
from ..run import Run, distance
from .T40 import default_drone

# Constants
WIDTH = 1200
HEIGHT = 800
EPS = 15

COLOR_WHITE = (255, 255, 255)

def init():
    pygame.init()
    pygame.key.set_repeat((1 * 1000) // 30)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    field_type = 1
    return screen, field_type


def critical(run: Run):
    print("FUCK YOU!")

screen, field_type = init()

board = boards[field_type]

field = pygame.surfarray.make_surface(board.to_nparray())

run = Run(board, copy.deepcopy(default_drone), board.terminals[0], critical)

def draw_reset():
    screen.fill(COLOR_WHITE)
    screen.blit(field, (0, 0))

draw_reset()

cnt = 0

DRONE_PATH = [(100, 0), (100, 10), (0, 10)]

crr = 0

def next_point(point: Point, run :Run):
    global crr
    if distance(point, DRONE_PATH[crr]) < EPS: crr = crr+1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    # draw_reset()
    next_point(run.position, run)
    run.point_to(DRONE_PATH[crr])
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

    time.sleep(0.5)
