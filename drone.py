import math
import pygame

COLOR_BLUE = (0, 0, 255)

# Create a drone
class Drone:
    def __init__(self, capacity, max_battery, spray_range, region, rw, rh):
        self.capacity = capacity
        self.max_battery = max_battery

        self.spray_range = spray_range
        # type of region is ((x1, y1), (x2, y2))
        self.region = region
        self.rw = rw
        self.rh = rh

        self.movement = [0, 0]
        self.position = [0, 0]
        self.spray = []
        self.last_spray = []

    def set_start_position(self, x, y):
        self.position = [x, y]
        self.update_spray()

    def set_movement(self, dx, dy):
        self.movement = [dx, dy]
        self.update_spray()

    def update_spray(self):
        try:
            mult = (self.spray_range / 2) / math.sqrt(self.movement[0] ** 2 + self.movement[1] ** 2)
            self.alt_movement = [self.movement[1], -self.movement[0]]
            self.last_spray = self.spray
            self.spray = [
                [self.position[0] - self.alt_movement[0] * mult, self.position[1] - self.alt_movement[1] * mult],
                [self.position[0] + self.alt_movement[0] * mult, self.position[1] + self.alt_movement[1] * mult]
            ]
            if not self.last_spray:
                self.last_spray = self.spray
        except ZeroDivisionError as e:
            pass

    def process(self):
        for d in range(2):
            self.position[d] += self.movement[d]
        self.update_spray()

    def draw(self, surface):
        X = round(self.region[0][0] + self.position[0] * self.rw)
        Y = round(self.region[1][1] - self.position[1] * self.rh)

        pygame.draw.circle(surface,
                           color = COLOR_BLUE,
                           center = (X, Y),
                           radius = 3,
                           width = 0)
