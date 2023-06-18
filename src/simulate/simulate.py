import copy
from matplotlib import pyplot as plt
from ..drone import ContainerException, BatteryException
from ..board import boards
from ..run import Run, distance
from .T40 import default_drone

# Constants
COLOR_WHITE = (255, 255, 255)
SPRAY_RANGE = 10

DRONE_PATH = []

for i in range(0, 3):
    DRONE_PATH += [(50, SPRAY_RANGE / 2 + SPRAY_RANGE * i), (100 - SPRAY_RANGE / 2 - SPRAY_RANGE * i, SPRAY_RANGE / 2 + SPRAY_RANGE * i), (100 - SPRAY_RANGE / 2 - SPRAY_RANGE * i, 50 - SPRAY_RANGE / 2 - SPRAY_RANGE * i), (SPRAY_RANGE / 2 + SPRAY_RANGE * i, 50 - SPRAY_RANGE / 2 - SPRAY_RANGE * i), (SPRAY_RANGE / 2 + SPRAY_RANGE * i, SPRAY_RANGE / 2 + SPRAY_RANGE * i), (50, SPRAY_RANGE / 2 + SPRAY_RANGE*i), ]

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

board = boards[1]
run = Run(board, copy.deepcopy(default_drone), board.terminals[0], critical)

run.drone.pump.change_range(SPRAY_RANGE)

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
        critical(run)
    print(run.drone.battery.remaining, run.time_spent, run.drone.pump.container.remaining)
    save_ax(run.ax, f"board1/solution0/{idx}.png")
