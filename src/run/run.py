import copy
from matplotlib import pyplot as plt
from ..board import Board, Point
from .calculations import scale_vector, draw_spray_range
from ..drone import Drone, BatteryException


def distance(a: Point, b: Point) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5


class Run:
    def __init__(self, board: Board, drone: Drone,
                 position: Point, run_on_critical):
        self.time_spent = 0
        self.battery_spent = 0
        self.board, self.drone = board, drone
        self.movement = [0, 0]
        self.position = position
        self.run_on_critical = run_on_critical
        self.fig, self.ax = plt.subplots()
        self.board.to_image(self.ax)

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

    def calculate(self, seconds: float):
        prev_battery = self.drone.battery.remaining
        self.drone.calculate(seconds)
        new_battery = self.drone.battery.remaining
        self.time_spent += seconds
        self.battery_spent += prev_battery - new_battery
        self.check_critical()
        new_position = self.new_position(seconds)
        # Draw rectangle from position to new_position
        # Width = self.drone.pump.spray_range
        draw_spray_range(self.position, new_position, self.ax,
                         lw=self.drone.pump.spray_range, color='aquamarine', zorder=4)
        draw_spray_range(self.position, new_position, self.ax,
                         lw=1, color='lightcoral', zorder=5)
        self.position = new_position

    # Speed must be set first
    def go_to(self, position: Point):
        cpy = copy.deepcopy(self)
        try:
            dist = distance(self.position, position)
            time_needed = dist / self.drone.v
            self.point_to(position)
            self.calculate(time_needed)
        except Exception as e:
            self = cpy
            raise e
