import copy
from ..board.board import Board, Point
from ..board import board1, board2, board3
from ..drone import Drone, BatteryException


def distance(a: Point, b: Point) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class Run:
    def __init__(self, board: Board, drone: Drone,
                 position: Point, run_on_critical: function):
        self.board, self.drone = board, drone
        self.movement = [0, 0]
        self.position = position
        self.run_on_critical = run_on_critical

    # Vector auto-scaled to current velocity
    def set_movement(self, vector: tuple[float, float]):
        mult = (vector[0] ** 2 + vector[1] ** 2) ** 0.5 / self.drone.v
        if abs(mult) > 1e-9:
            vector[0] /= mult
            vector[1] /= mult
        self.movement = vector

    # Vector auto-scaled to current velocity
    def point_to(self, position: Point):
        vector = position[0] - self.position[0], position[1] - self.position[1]
        self.set_movement(vector)

    def new_position(self, seconds: float) -> Point:
        position = self.position
        position[0] += seconds * self.movement[0]
        position[1] += seconds * self.movement[1]
        return position

    def check_critical(self):
        min_distance = 1e18
        for term in self.board.terminals:
            min_distance = min(min_distance, distance(term, self.position))
        time_needed = min_distance / self.drone.max_speed
        try:
            cpy = copy.deepcopy(self)
            cpy.drone.change_speed(cpy.drone.max_speed)
            cpy.drone.pump.change_fp(0)
            cpy.calculate(time_needed)
        except BatteryException:
            self.run_on_critical()

    def calculate(self, seconds: float):
        self.drone.calculate(seconds)
        self.check_critical()
        new_position = self.new_position(seconds)
        # Draw rectangle from position to new_position
        # Width = self.drone.pump.spray_range
        # TODO
        self.position = new_position

