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
