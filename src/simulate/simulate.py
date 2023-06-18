import copy
import os
import shutil
from matplotlib import pyplot as plt
from ..drone import ContainerException, BatteryException
from ..board import boards
from ..run import Run, distance
from .T40 import default_drone
from .board2sol2 import get_board2_sol2
from .finegrain import fine_grain_path

# Constants
COLOR_WHITE = (255, 255, 255)
SPRAY_RANGE = 10


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


board = boards[2]
run = Run(board, copy.deepcopy(default_drone), board.terminals[0], critical)


run.drone.pump.change_range(SPRAY_RANGE)

DRONE_PATH, NAME = get_board2_sol2(run)
DRONE_PATH = fine_grain_path(run.position, DRONE_PATH + [run.board.terminals[0]])

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