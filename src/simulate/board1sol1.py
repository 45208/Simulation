
def get_board1_sol1() -> tuple[list[tuple[float, float]], str]:
    DRONE_PATH = []
    SPRAY_RANGE = 10
    for i in range(0, 3):
        DRONE_PATH += [(50, SPRAY_RANGE / 2 + SPRAY_RANGE * i),
                       (100 - SPRAY_RANGE / 2 - SPRAY_RANGE * i, SPRAY_RANGE / 2 + SPRAY_RANGE * i),
                       (100 - SPRAY_RANGE / 2 - SPRAY_RANGE * i, 50 - SPRAY_RANGE / 2 - SPRAY_RANGE * i),
                       (SPRAY_RANGE / 2 + SPRAY_RANGE * i, 50 - SPRAY_RANGE / 2 - SPRAY_RANGE * i),
                       (SPRAY_RANGE / 2 + SPRAY_RANGE * i, SPRAY_RANGE / 2 + SPRAY_RANGE * i),
                       (50, SPRAY_RANGE / 2 + SPRAY_RANGE*i)]
    return DRONE_PATH, "board1_sol1"
