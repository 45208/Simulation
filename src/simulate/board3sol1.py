import math
from ..run import Run

def get_board3_sol1(run: Run) -> tuple[list[tuple[float, float]], str]:
    SPRAY_RANGE = 10 
    DRONE_PATH = []
    polygon = [(0.0, 150.0), (150.0, 150.0), (300.0, 600.0), (.0, 450.0)]
    for i in range(13):
        DRONE_PATH.append((run.board.terminals[0][0] + SPRAY_RANGE * (i+ 0.5),
                        run.board.terminals[0][1]))
        DRONE_PATH.append((polygon[0][0] + SPRAY_RANGE * (i       + 0.5),
                        polygon[0][1] + SPRAY_RANGE * (i        + 0.5)))
        if polygon[1][0] - SPRAY_RANGE * (i * 1/math.tan(math.radians(108.43/2))    + 0.5) > polygon[0][0] + SPRAY_RANGE * (i       + 0.5):
            DRONE_PATH.append((polygon[1][0] - SPRAY_RANGE * (i * 1/math.tan(math.radians(108.43/2))    + 0.5),
                        polygon[1][1] + SPRAY_RANGE * (i    + 0.5)))
        DRONE_PATH.append((polygon[2][0] - SPRAY_RANGE * (i*1.4    + 0.5),
                        polygon[2][1] - SPRAY_RANGE * (i*1.4    + 0.5)))
        DRONE_PATH.append((polygon[3][0] + SPRAY_RANGE * (i      + 0.5),
                        polygon[3][1] - SPRAY_RANGE * (i * 1/math.tan(math.radians(116.65/2))        + 0.5)))
        DRONE_PATH.append((run.board.terminals[0][0] + SPRAY_RANGE * (i+ 0.5),
                        run.board.terminals[0][1]))
        
    DRONE_PATH.append((polygon[0][0]+0.5, polygon[0][1]))
    polygon = [(0.0, 0.0), (450.0, 0.0), (450.0, 150.0), (0.0, 150.0)]

    for i in range(8):
        DRONE_PATH.append((polygon[0][0] + SPRAY_RANGE*(i + 0.5), polygon[0][1] + SPRAY_RANGE*(i+0.5)))
        DRONE_PATH.append((polygon[1][0] - SPRAY_RANGE*(i + 0.5), polygon[1][1] + SPRAY_RANGE*(i+0.5)))
        DRONE_PATH.append((polygon[2][0] - SPRAY_RANGE*(i + 0.5), polygon[2][1] - SPRAY_RANGE*(i+0.5)))
        DRONE_PATH.append((polygon[3][0] + SPRAY_RANGE*(i + 0.5), polygon[3][1] - SPRAY_RANGE*(i+0.5)))
    



    return DRONE_PATH, "board3_sol1"
