import copy
import math
from matplotlib import pyplot as plt
from ..drone import ContainerException, BatteryException
from ..board import boards
from ..run import Run, distance
from .T40 import default_drone

# Constants
COLOR_WHITE = (255, 255, 255)
SPRAY_RANGE = 10

def critical(run: Run):
    run.drone.pump.change_fp(0)
    run.drone.pump.change_range(0)
    run.drone.change_speed(run.drone.max_speed)
    try:
        run.go_to(run.board.terminals[0])
    except BatteryException:
        pass
    print("New drone")
    run.drone = copy.deepcopy(default_drone)

board = boards[2]
run = Run(board, copy.deepcopy(default_drone), board.terminals[0], critical)


run.drone.pump.change_range(SPRAY_RANGE)

DRONE_PATH = []



for i in range(8):
    DRONE_PATH.append((run.board.terminals[0][0],
                       run.board.vertices[0][1] + SPRAY_RANGE * (i        + 0.5)))
    DRONE_PATH.append((run.board.vertices[0][0] + SPRAY_RANGE * (i * 1/math.tan(math.pi/6)        + 0.5),
                       run.board.vertices[0][1] + SPRAY_RANGE * (i        + 0.5)))
    DRONE_PATH.append((run.board.vertices[1][0] - SPRAY_RANGE * (i * 1/math.tan(math.pi*(1/8))    + 0.5),
                       run.board.vertices[1][1] + SPRAY_RANGE * (i    + 0.5)))
    DRONE_PATH.append((run.board.vertices[2][0] - SPRAY_RANGE * (i * 1/math.tan(math.pi*(3/8))    + 0.5),
                       run.board.vertices[2][1] - SPRAY_RANGE * (i    + 0.5)))
    DRONE_PATH.append((run.board.vertices[3][0] + SPRAY_RANGE * (i * 1/math.tan(math.pi/3)        + 0.5),
                       run.board.vertices[3][1] - SPRAY_RANGE * (i        + 0.5)))
    DRONE_PATH.append((run.board.vertices[0][0] + SPRAY_RANGE * (i * 1/math.tan(math.pi/6)        + 0.5),
                       run.board.vertices[0][1] + SPRAY_RANGE * (i        + 0.5)))
    DRONE_PATH.append((run.board.terminals[0][0],
                       run.board.vertices[0][1] + SPRAY_RANGE * (i       + 0.5)))

# Reference: https://stackoverflow.com/questions/43096972/how-can-i-render-a-matplotlib-axes-object-to-an-image-as-a-numpy-array
def save_ax(ax: plt.Axes, filename: str, **kwargs):
    ax.axis("off")
    ax.figure.canvas.draw()
    trans = ax.figure.dpi_scale_trans.inverted() 
    bbox = ax.bbox.transformed(trans)
    plt.savefig(filename, dpi="figure", bbox_inches=bbox,  **kwargs)

for idx, point in enumerate(DRONE_PATH):
    run.drone.change_speed_based_on_pump(75)
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

    print(run.drone.battery.remaining, run.time_spent, run.drone.pump.container.remaining)
    save_ax(run.ax, f"images/board2/solution0/{idx}.png")
