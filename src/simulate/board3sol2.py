import math
from ..run import Run

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
        DRONE_PATH.append((rbx + SPRAY_RANGE*(i * 1 / math.tan(math.radians(71.56))), sty + SPRAY_RANGE*i))
        DRONE_PATH.append((rbx + SPRAY_RANGE*((i+1) * 1 / math.tan(math.radians(71.56))), sty + SPRAY_RANGE*(i+1)))
        DRONE_PATH.append((lbx, sty + SPRAY_RANGE*(i+1)))

    sty = 450 + SPRAY_RANGE/2
    rbx = 250 - SPRAY_RANGE/2
    for i in range(0, 16, 2):
        DRONE_PATH.append((lbx + SPRAY_RANGE*((i+1) * 1 / math.tan(math.radians(26.56))), sty + SPRAY_RANGE*i))
        DRONE_PATH.append((rbx + SPRAY_RANGE*(i * 1 / math.tan(math.radians(71.56))), sty + SPRAY_RANGE*i))
        DRONE_PATH.append((rbx + SPRAY_RANGE*((i+1) * 1 / math.tan(math.radians(71.56))), sty + SPRAY_RANGE*(i+1)))
        DRONE_PATH.append((lbx + SPRAY_RANGE*((i+2) * 1 / math.tan(math.radians(26.56))), sty + SPRAY_RANGE*(i+1)))
    
    DRONE_PATH.pop()
    DRONE_PATH.pop()

    DRONE_PATH.append((SPRAY_RANGE/2, 450))
    
    return DRONE_PATH, "board3_sol2"
