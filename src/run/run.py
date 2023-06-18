import copy
import pygame
from ..board import Board, Point
from .calculations import scale_vector
from ..drone import Drone, BatteryException

# Constants
COLOR_RED = (255, 0, 0)
COLOR_SPRAY = (255, 193, 205)


def distance(a: Point, b: Point) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Run:
    def __init__(self, board: Board, drone: Drone,
                 position: Point, run_on_critical):
        self.board, self.drone = board, drone
        self.movement = [0, 0]
        self.position = position
        self.run_on_critical = run_on_critical

    # Vector auto-scaled to current velocity
    def set_movement(self, vector: tuple[float, float]):
        self.movement = scale_vector(vector, self.drone.v)

    # Vector auto-scaled to current velocity
    def point_to(self, position: Point):
        vector = position[0] - self.position[0], position[1] - self.position[1]
        self.set_movement(vector)

    def new_position(self, seconds: float) -> Point:
        position = (self.position[0] + seconds * self.movement[0],
                    self.position[1] + seconds * self.movement[1])
        return position

    def check_critical(self):
        min_distance = 1e18
        for term in self.board.terminals:
            min_distance = min(min_distance, distance(term, self.position))
        time_needed = min_distance / self.drone.max_speed
        try:
            cpy = copy.deepcopy(self.drone)
            cpy.change_speed(cpy.max_speed)
            cpy.pump.change_fp(0)
            cpy.calculate(time_needed)
        except BatteryException:
            self.run_on_critical(self)

    def draw_drone(self, screen: pygame.Surface):
        pygame.draw.circle(screen, COLOR_RED, self.position, 2, 0)

    def draw_spray_range(self,screen: pygame.Surface, new_position: Point):
        x, y = self.movement
        x, y = y, -x
        x, y = scale_vector((x, y), self.drone.pump.spray_range / 2)

        corners = (self.position[0] + x, self.position[1] + y), \
                  (self.position[0] - x, self.position[1] - y), \
                  (new_position[0] - x, new_position[1] - y), \
                  (new_position[0] + x, new_position[1] + y)

        pygame.draw.polygon(screen, COLOR_SPRAY, corners, 0)

    def calculate(self, screen: pygame.Surface, seconds: float):
        self.drone.calculate(seconds)
        self.check_critical()
        new_position = self.new_position(seconds)
        # Draw rectangle from position to new_position
        # Width = self.drone.pump.spray_range
        self.draw_spray_range(screen, new_position)
        self.position = new_position
