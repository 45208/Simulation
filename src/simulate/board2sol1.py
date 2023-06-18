import math
from ..run import Run

def get_board2_sol1(run : Run) -> tuple[list[tuple[float, float]], str]:
    DRONE_PATH = []
    SPRAY_RANGE = 10
    for i in range(8):
        DRONE_PATH.append((run.board.terminals[0][0],
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
    return DRONE_PATH, "board2_sol1"