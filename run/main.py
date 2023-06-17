# Import
import sys
import pygame
from run.drone_old import Drone

# Constants
WIDTH = 1200
HEIGHT = 800
BOARD_SIDE = 650
OFFSET_X = 50
OFFSET_Y = 50

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)

EPSILON = 1e-6
SPEED = 4
FPS = 30
DISTANCE = SPEED / FPS

# Initialize pygame
pygame.init()
pygame.key.set_repeat((1 * 1000) // FPS)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Get drone and terminal points
field_type = int(sys.argv[1])
picture = {
    1: "draw\\board1.png",
    2: "draw\\board2.png",
    3: "draw\\board3.png",
}

terminal_points = {
    1: [(50, 0)],
    2: [(186, 0)],
    3: [(0, 300), (300, 150)],
}

board = pygame.image.load(picture[field_type])

# Fix board
board_width = board.get_width()
board_height = board.get_height()

ratio_width = BOARD_SIDE / board_width
ratio_height = BOARD_SIDE / board_height

board = pygame.transform.scale(board, (BOARD_SIDE, BOARD_SIDE))

# Create the drone
drone = Drone(40, 30000, 4, 720, terminal_points[field_type])

colored = pygame.Surface((OFFSET_X + BOARD_SIDE, OFFSET_Y + BOARD_SIDE), pygame.SRCALPHA)

delta_x = 1
delta_y = 0

drone.set_start_position(*terminal_points[field_type][0])
drone.set_movement(delta_x, delta_y)
drone.set_draw(((OFFSET_X, OFFSET_Y), (OFFSET_X + BOARD_SIDE, OFFSET_Y + BOARD_SIDE)), ratio_width, ratio_height)

def calculate_battery(current_weight, pump_speed):
    consumption_rate = 11000 + 0.42 * pump_speed + 857.14 * current_weight
    return consumption_rate / 3600

drone.formula = calculate_battery

def reset_draw():
    screen.fill(COLOR_WHITE)
    screen.blit(board, (OFFSET_X, OFFSET_Y))
    for pts in terminal_points[field_type]:
        X = OFFSET_X + pts[0] * ratio_width
        Y = OFFSET_Y + BOARD_SIDE - pts[1] * ratio_height
        pygame.draw.circle(screen,
                           color = COLOR_RED,
                           center = (X, Y),
                           radius = 5,
                           width = 0)

# Control loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drone.process()
                drone.consume_pesticide(1/FPS)
                drone.consume_battery(1/FPS)

                print(drone.current_weight, drone.current_battery)

    x, y = pygame.mouse.get_pos()
    x0, y0 = drone.pixel()

    vector = [x - x0, y0 - y]
    mult = (vector[0] ** 2 + vector[1] ** 2) ** 0.5 / DISTANCE
    if abs(mult) > EPSILON:
        vector[0] /= mult
        vector[1] /= mult

    drone.set_movement(*vector)
            
    reset_draw()
    drone.draw_spray(colored)
    screen.blit(colored, (0, 0))
    drone.draw_drone(screen)

    pygame.display.update()