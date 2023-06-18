from ..run import Run

def get_board2_sol2(run: Run) -> tuple[list[tuple[float, float]], str]:
    DRONE_PATH = []
    SPRAY_RANGE = 10

    for i in range(0, 16, 2):
        DRONE_PATH.append((run.board.terminals[0][0], SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((SPRAY_RANGE*(i * 0.580123 + 1), SPRAY_RANGE * (i + 0.5)))
        DRONE_PATH.append((SPRAY_RANGE*((i+1) * 0.580123 + 1), SPRAY_RANGE * ((i+1) + 0.5)))
        DRONE_PATH.append((run.board.terminals[0][0], SPRAY_RANGE * ((i+1) + 0.5)))

    DRONE_PATH.pop()
    DRONE_PATH.pop()

    crrx, crry = run.board.vertices[2][0] - SPRAY_RANGE / 2 + 3, DRONE_PATH[-1][1]
    for i in range(0, 16, 2):
        DRONE_PATH.append((crrx + SPRAY_RANGE * i       , crry - SPRAY_RANGE * i))
        DRONE_PATH.append((crrx + SPRAY_RANGE * (i+1)   , crry - SPRAY_RANGE * (i+1)))
        DRONE_PATH.append((run.board.terminals[0][0]    , crry - SPRAY_RANGE * (i+1)))
        DRONE_PATH.append((run.board.terminals[0][0]    , crry - SPRAY_RANGE * (i+2)))
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    DRONE_PATH.pop()
    return DRONE_PATH, "board2_sol2"