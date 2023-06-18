import os
import shutil
import math
import copy
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
Point = tuple[float, float]
class Board:
    xp, yp = [0, -1, 0, 1], [-1, 0, 1, 0]
    EPSILON = 1e-7
    def __init__(self, vertices: tuple[Point], terminals: tuple[Point]):
        self.vertices = vertices
        self.terminals = terminals
        assert len(self.vertices) > 2
        self.size = 0
        for Point in self.vertices:
            self.size = max(self.size, Point[0], Point[1])
        self.size = math.ceil(self.size)
        self.board = [[False for _ in range(self.size)]
                      for _ in range(self.size)]
        self.__calculate_board()
    def to_nparray(self) -> np.ndarray:
        COLOR_FALSE = [151, 153, 155]
        COLOR_TRUE = [112, 224, 0]
        self.np_board = [[[COLOR_FALSE, COLOR_TRUE][cell]
                          for cell in line] for line in self.board]
        self.np_board = np.array(self.np_board)
        return self.np_board
    def __crossed(self, cx: float, cy: float, nx: float, ny: float) -> bool:
        def __counter_clockwise(a: Point, b: Point, c: Point) -> float:
            return (a[0]-b[0])*c[1] + (b[0]-c[0])*a[1] + (c[0]-a[0])*b[1]
        def __different_half_plane(x: Point, y: Point, a: Point, b: Point) -> bool:
            return __counter_clockwise(x, a, b) * __counter_clockwise(y, a, b) < self.EPSILON
        def __intersected(c: Point, n: Point, a: Point, b: Point) -> bool:
            return __different_half_plane(c, n, a, b) and __different_half_plane(a, b, c, n)
        for i in range(len(self.vertices)):
            a, b = self.vertices[i-1], self.vertices[i]
            if __intersected((cx, cy), (nx, ny), a, b):
                return True
        return False
    def __calculate_board(self) -> None:
        queue = deque()
        queue.append((0, 0))
        while len(queue):
            cx, cy = queue.popleft()
            for xa, ya in zip(self.xp, self.yp):
                nx, ny = cx + xa, cy + ya
                if self.__crossed(cx + .5, cy + .5, nx + .5, ny + .5):
                    continue
                if self.board[nx][ny]:
                    continue
                self.board[nx][ny] = 1
                queue.append((nx, ny))
    def to_image(self, ax: plt.Axes) -> None:
        board = []
        for y in range(self.size):
            board.append([])
            for x in range(self.size):
                result = None
                match self.board[x][y]:
                    case 0:
                        result = 0, 0, 0, 0
                    case 1:
                        result = 255, 228, 181, 255
                board[-1].append(result)
        ax.axis('off')
        ax.imshow(board, origin="lower")
    def __repr__(self):
        s = ""
        for y in range(self.size-1, -1, -1):
            for x in range(self.size):
                s += 'X' if self.board[x][y] else '-'
            s += '\n'
        return s
BOARD1 = (.0, .0), (100.0, .0), (100.0, 50.0), (.0, 50.0)
TERM1 = ((50, 0),)
BOARD2 = (.0, .0), (386.6025, .0), (236.6025, 150.0), (86.6025, 150.0)
TERM2 = ((186, 0),)
BOARD3 = (.0, .0), (450.0, .0), (450.0, 150.0), \
         (150.0, 150.0), (300.0, 600.0), (.0, 450.0)
TERM3 = ((0, 300), (300, 150))
boards = {}
boards[1] = Board(BOARD1, TERM1)
boards[2] = Board(BOARD2, TERM2)
boards[3] = Board(BOARD3, TERM3)
class BatteryException(Exception):
    pass
class Battery:
    voltage = 110
    def __init__(self, capacity: float):
        self.capacity = capacity * self.voltage
        self.remaining = self.capacity
    def calculate(self, amount: float):
        if self.remaining < amount:
            raise BatteryException()
        self.remaining -= amount
class ContainerException(Exception):
    pass
class Container:
    def __init__(self, battery: Battery, ct: float, capacity: float,
                 remaining: float | None = None):
        self.ct = ct
        self.capacity = capacity
        self.remaining = capacity if remaining is None else remaining
        self.battery = battery
    def calculate(self, seconds: float, used: float):
        hours = seconds / 3600
        self.battery.calculate(
            self.ct * (self.remaining * 2 - used) / 2 * hours)
        if self.remaining < used:
            raise ContainerException
        self.remaining -= used
class Pump:
    def __init__(self, battery: Battery, container: Container,
                 cp: float, max_spray_range: float, max_flow: float,
                 fp: float | None = None, spray_range: float | None = None):
        self.battery, self.container = battery, container
        self.cp = cp
        self.max_flow = max_flow
        self.fp = self.max_flow if fp is None else fp
        self.max_spray_range = max_spray_range
        self.spray_range = self.max_spray_range if spray_range is None else spray_range
    def change_fp(self, fp: float):
        assert self.max_flow >= self.fp
        self.fp = fp
    def change_range(self, spray_range: float):
        self.spray_range = spray_range
    def calculate(self, seconds: float):
        hours = seconds / 3600
        self.battery.calculate(self.cp * self.fp * hours)
        self.container.calculate(seconds, self.fp * hours)
class Drone:
    def __init__(self, battery: Battery, pump: Pump, c: float, max_speed: float, v: float | None = None):
        self.battery = battery
        self.pump = pump
        self.c = c
        self.max_speed = max_speed
        self.v = max_speed if v is None else v
    def change_speed(self, v: float):
        assert self.max_speed >= v
        self.v = v
    def change_speed_based_on_pump(self, concen: float):
        assert self.pump.fp != 0
        assert self.pump.spray_range != 0
        # Convert to L/m^2
        concen /= 1e4
        new_speed = self.pump.fp / (concen * self.pump.spray_range)
        # Convert to m/s
        new_speed /= 3600
        self.change_speed(new_speed)
    def calculate(self, seconds: float):
        hours = seconds / 3600
        self.pump.calculate(seconds)
        self.battery.calculate(self.c * hours)
    def normal_working(self, concen: float):
        self.pump.change_fp(self.pump.max_flow)
        self.change_speed_based_on_pump(concen)
# T40 Constants
DEFAULT_SPRAY_RANGE = 10
MAX_FLOW = 720
battery = Battery(30)
container = Container(battery, ct=857.14, capacity=40)
pump = Pump(battery, container, cp=0.42,
            max_spray_range=DEFAULT_SPRAY_RANGE, max_flow=MAX_FLOW)
default_drone = Drone(battery, pump, c=11000, max_speed=10)
def scale_vector(vector: Point, dist: float):
    mult = (vector[0] ** 2 + vector[1] ** 2) ** 0.5 / dist
    if abs(mult) > 1e-9:
        vector = (vector[0] / mult, vector[1] / mult)
    return vector
# Reference: https://stackoverflow.com/questions/19394505/expand-the-line-with-specified-width-in-data-unit/42972469
class LineDataUnits(Line2D):
    def __init__(self, *args, **kwargs):
        _lw_data = kwargs.pop("lw", 1)
        super().__init__(*args, **kwargs)
        self._lw_data = _lw_data
    def _get_lw(self):
        if self.axes is not None:
            ppd = 72./self.axes.figure.dpi
            trans = self.axes.transData.transform
            return ((trans((1, self._lw_data))-trans((0, 0)))*ppd)[1]
        else:
            return 1
    def _set_lw(self, lw):
        self._lw_data = lw
    _linewidth = property(_get_lw, _set_lw)
def draw_spray_range(a: Point, b: Point, ax: plt.Axes, **kwargs):
    line = LineDataUnits([a[0], b[0]], [a[1], b[1]], **kwargs)
    ax.add_line(line)
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
def get_board1_sol1(run: Run) -> tuple[list[tuple[float, float]], str]:
    DRONE_PATH = []
    SPRAY_RANGE = 10
    for i in range(0, 3):
        DRONE_PATH += [(50, SPRAY_RANGE / 2 + SPRAY_RANGE * i),
                       (100 - SPRAY_RANGE / 2 - SPRAY_RANGE *
                        i, SPRAY_RANGE / 2 + SPRAY_RANGE * i),
                       (100 - SPRAY_RANGE / 2 - SPRAY_RANGE * i,
                        50 - SPRAY_RANGE / 2 - SPRAY_RANGE * i),
                       (SPRAY_RANGE / 2 + SPRAY_RANGE * i,
                        50 - SPRAY_RANGE / 2 - SPRAY_RANGE * i),
                       (SPRAY_RANGE / 2 + SPRAY_RANGE * i,
                        SPRAY_RANGE / 2 + SPRAY_RANGE * i),
                       (50, SPRAY_RANGE / 2 + SPRAY_RANGE*i)]
    return DRONE_PATH, "board1_sol1"
def get_board1_sol2(run: Run) -> tuple[list[tuple[float, float]], str]:
    SPRAY_RANGE = 50/6
    DRONE_PATH = [(50, SPRAY_RANGE / 2)]
    leftx, rightx = SPRAY_RANGE * 1.5, 100 - SPRAY_RANGE/2
    for i in range(0, 6, 2):
        DRONE_PATH.append((rightx, SPRAY_RANGE*(i + 0.5)))
        DRONE_PATH.append((rightx, SPRAY_RANGE*((i+1) + 0.5)))
        DRONE_PATH.append((leftx, SPRAY_RANGE*((i+1) + 0.5)))
        DRONE_PATH.append((leftx, SPRAY_RANGE*((i+2) + 0.5)))
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    DRONE_PATH.append((SPRAY_RANGE/2, 50 - SPRAY_RANGE/2))
    DRONE_PATH.append((SPRAY_RANGE/2, SPRAY_RANGE/2))
    DRONE_PATH.append((50, SPRAY_RANGE/2))
    return DRONE_PATH, "board1_sol2"
def get_board2_sol1(run: Run) -> tuple[list[tuple[float, float]], str]:
    DRONE_PATH = []
    SPRAY_RANGE = 10
    for i in range(8):
        DRONE_PATH.append((run.board.terminals[0][0],
                           run.board.vertices[0][1] + SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((run.board.vertices[1][0] - SPRAY_RANGE * (i * 1/math.tan(math.pi*(1/8)) + 0.5),
                           run.board.vertices[1][1] + SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((run.board.vertices[2][0] - SPRAY_RANGE * (i * 1/math.tan(math.pi*(3/8)) + 0.5),
                           run.board.vertices[2][1] - SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((run.board.vertices[3][0] + SPRAY_RANGE * (i * 1/math.tan(math.pi/3) + 0.5),
                           run.board.vertices[3][1] - SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((run.board.vertices[0][0] + SPRAY_RANGE * (i * 1/math.tan(math.pi/6) + 0.5),
                           run.board.vertices[0][1] + SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((run.board.terminals[0][0],
                           run.board.vertices[0][1] + SPRAY_RANGE * (i + 0.5)))
    return DRONE_PATH, "board2_sol1"
def get_board2_sol2(run: Run) -> tuple[list[tuple[float, float]], str]:
    DRONE_PATH = []
    SPRAY_RANGE = 10
    for i in range(0, 16, 2):
        DRONE_PATH.append((run.board.terminals[0][0], SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append(
            (SPRAY_RANGE*(i * 0.580123 + 1), SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((SPRAY_RANGE*((i+1) * 0.580123 + 1),
                          SPRAY_RANGE * ((i+1) + 0.5)))
        DRONE_PATH.append(
            (run.board.terminals[0][0], SPRAY_RANGE * ((i+1) + 0.5)))
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    crrx, crry = run.board.vertices[2][0] - \
        SPRAY_RANGE / 2 + 3, DRONE_PATH[-1][1]
    for i in range(0, 16, 2):
        DRONE_PATH.append((crrx + SPRAY_RANGE * i, crry - SPRAY_RANGE * i))
        DRONE_PATH.append((crrx + SPRAY_RANGE * (i+1),
                          crry - SPRAY_RANGE * (i+1)))
        DRONE_PATH.append(
            (run.board.terminals[0][0], crry - SPRAY_RANGE * (i+1)))
        DRONE_PATH.append(
            (run.board.terminals[0][0], crry - SPRAY_RANGE * (i+2)))
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    return DRONE_PATH, "board2_sol2"
def get_board3_sol1(run: Run) -> tuple[list[tuple[float, float]], str]:
    SPRAY_RANGE = 10
    DRONE_PATH = []
    polygon = [(0.0, 150.0), (150.0, 150.0), (300.0, 600.0), (.0, 450.0)]
    for i in range(13):
        DRONE_PATH.append((run.board.terminals[0][0] + SPRAY_RANGE * (i + 0.5),
                           run.board.terminals[0][1]))
        DRONE_PATH.append((polygon[0][0] + SPRAY_RANGE * (i + 0.5),
                           polygon[0][1] + SPRAY_RANGE * (i + 0.5)))
        if polygon[1][0] - SPRAY_RANGE * (i * 1/math.tan(math.radians(108.43/2)) + 0.5) > polygon[0][0] + SPRAY_RANGE * (i + 0.5):
            DRONE_PATH.append((polygon[1][0] - SPRAY_RANGE * (i * 1/math.tan(math.radians(108.43/2)) + 0.5),
                               polygon[1][1] + SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((polygon[2][0] - SPRAY_RANGE * (i*1.4 + 0.5),
                           polygon[2][1] - SPRAY_RANGE * (i*1.4 + 0.5)))
        DRONE_PATH.append((polygon[3][0] + SPRAY_RANGE * (i + 0.5),
                           polygon[3][1] - SPRAY_RANGE * (i * 1/math.tan(math.radians(116.65/2)) + 0.5)))
        DRONE_PATH.append((run.board.terminals[0][0] + SPRAY_RANGE * (i + 0.5),
                           run.board.terminals[0][1]))
    DRONE_PATH.append((polygon[0][0]+0.5, polygon[0][1]))
    polygon = [(0.0, 0.0), (450.0, 0.0), (450.0, 150.0), (0.0, 150.0)]
    for i in range(8):
        DRONE_PATH.append(
            (polygon[0][0] + SPRAY_RANGE*(i + 0.5), polygon[0][1] + SPRAY_RANGE*(i+0.5)))
        DRONE_PATH.append(
            (polygon[1][0] - SPRAY_RANGE*(i + 0.5), polygon[1][1] + SPRAY_RANGE*(i+0.5)))
        DRONE_PATH.append(
            (polygon[2][0] - SPRAY_RANGE*(i + 0.5), polygon[2][1] - SPRAY_RANGE*(i+0.5)))
        DRONE_PATH.append(
            (polygon[3][0] + SPRAY_RANGE*(i + 0.5), polygon[3][1] - SPRAY_RANGE*(i+0.5)))
    return DRONE_PATH, "board3_sol1"
def get_board3_sol2(run: Run) -> tuple[list[tuple[float, float]], str]:
    SPRAY_RANGE = 10
    DRONE_PATH = []
    polygon = [(0.0, 150.0), (150.0, 150.0), (300.0, 600.0), (.0, 450.0)]
    lbx, rbx = SPRAY_RANGE/2, 450 - SPRAY_RANGE/2
    for i in range(0, 16, 2):
        DRONE_PATH.append((lbx, SPRAY_RANGE*(i + 0.5)))
        DRONE_PATH.append((rbx, SPRAY_RANGE*(i + 0.5)))
        DRONE_PATH.append((rbx, SPRAY_RANGE*((i+1) + 0.5)))
        DRONE_PATH.append((lbx, SPRAY_RANGE*((i+1) + 0.5)))
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    lbx = SPRAY_RANGE/2
    rbx = 150 - SPRAY_RANGE/2
    sty = 150 + SPRAY_RANGE/2
    for i in range(0, 30, 2):
        DRONE_PATH.append((lbx, sty + SPRAY_RANGE*i))
        DRONE_PATH.append(
            (rbx + SPRAY_RANGE*(i * 1 / math.tan(math.radians(71.56))), sty + SPRAY_RANGE*i))
        DRONE_PATH.append((rbx + SPRAY_RANGE*((i+1) * 1 /
                          math.tan(math.radians(71.56))), sty + SPRAY_RANGE*(i+1)))
        DRONE_PATH.append((lbx, sty + SPRAY_RANGE*(i+1)))
    sty = 450 + SPRAY_RANGE/2
    rbx = 250 - SPRAY_RANGE/2
    for i in range(0, 16, 2):
        DRONE_PATH.append((lbx + SPRAY_RANGE*((i+1) * 1 /
                          math.tan(math.radians(26.56))), sty + SPRAY_RANGE*i))
        DRONE_PATH.append(
            (rbx + SPRAY_RANGE*(i * 1 / math.tan(math.radians(71.56))), sty + SPRAY_RANGE*i))
        DRONE_PATH.append((rbx + SPRAY_RANGE*((i+1) * 1 /
                          math.tan(math.radians(71.56))), sty + SPRAY_RANGE*(i+1)))
        DRONE_PATH.append((lbx + SPRAY_RANGE*((i+2) * 1 /
                          math.tan(math.radians(26.56))), sty + SPRAY_RANGE*(i+1)))
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    DRONE_PATH.append((SPRAY_RANGE/2, 450))
    return DRONE_PATH, "board3_sol2"
# Constants
COLOR_WHITE = (255, 255, 255)
SPRAY_RANGE = 10
def fine_grain_path(start: tuple[float, float], drone_path: list[tuple[float, float]]) -> list[tuple[float, float]]:
    result = []
    for point in drone_path:
        segment = 5
        vector = (point[0] - start[0]) / \
            segment, (point[1] - start[1]) / segment
        for i in range(segment):
            result.append((start[0] + vector[0] * (i+1),
                          start[1] + vector[1] * (i+1)))
        start = point
    return result
def critical(run: Run):
    run.drone.pump.change_fp(0)
    run.drone.pump.change_range(0)
    run.drone.change_speed(run.drone.max_speed)
    try:
        if len(run.board.terminals) < 2:
            run.go_to(run.board.terminals[0])
        else:
            if distance(run.board.terminals[0], run.position) < distance(run.board.terminals[1], run.position):
                run.go_to(run.board.terminals[0])
            else:
                run.go_to(run.board.terminals[1])
    except BatteryException:
        pass
    print("New drone")
    run.drone = copy.deepcopy(default_drone)
board = boards[1]
run = Run(board, copy.deepcopy(default_drone), board.terminals[0], critical)
run.drone.pump.change_range(SPRAY_RANGE)
DRONE_PATH, NAME = get_board1_sol1(run)
DRONE_PATH = fine_grain_path(
    run.position, DRONE_PATH + [run.board.terminals[0]])
# Reference: https://stackoverflow.com/questions/43096972/how-can-i-render-a-matplotlib-axes-object-to-an-image-as-a-numpy-array
def save_ax(ax: plt.Axes, filename: str, **kwargs):
    ax.axis("off")
    ax.figure.canvas.draw()
    trans = ax.figure.dpi_scale_trans.inverted()
    bbox = ax.bbox.transformed(trans)
    plt.savefig(filename, dpi="figure", bbox_inches=bbox,  **kwargs)
try:
    shutil.rmtree(f"images/{NAME}")
    os.makedirs(f"images/{NAME}")
except Exception as e:
    print(e)
CONCENTRATION = 75
for idx, point in enumerate(DRONE_PATH):
    run.drone.change_speed_based_on_pump(CONCENTRATION)
    try:
        run.go_to(point)
    except ContainerException:
        position = run.position
        critical(run)
        run.drone.pump.change_fp(0)
        run.drone.pump.change_range(0)
        run.go_to(position)
        run.drone.pump.change_fp(run.drone.pump.max_flow)
        run.drone.pump.change_range(run.drone.pump.max_spray_range)
        run.go_to(point)
    print(run.drone.battery.remaining, run.time_spent,
          run.battery_spent, run.drone.pump.container.remaining)
    save_ax(run.ax, f"images/{NAME}/{idx}.png")
print(NAME)
print(f"Concentration: {CONCENTRATION}L/ha")
print(f"Time spent: {run.time_spent*(500/CONCENTRATION)}s")
print(f"Energy consumed: {run.battery_spent*(500/CONCENTRATION)}Wh")
def export(FOLDER_NAME: str):
    import glob
    from pathlib import Path
    import imageio
    FOLDER_NAME = "images\\boardx_soly"
    def srt(a: str):
        return int(Path(a).stem)
    image_names = glob.glob(f"{FOLDER_NAME}\\*.png")
    image_names = sorted(image_names, key=srt)
    images = []
    for name in image_names:
        images.append(imageio.imread(name))
    imageio.mimsave(f"{FOLDER_NAME}\\result.gif", images)
