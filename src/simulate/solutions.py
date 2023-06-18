import math
from ..run import Run


def get_board1_sol1() -> tuple[list[tuple[float, float]], str]:
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


def get_board1_sol2() -> tuple[list[tuple[float, float]], str]:
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
