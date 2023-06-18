def fine_grain_path(start: tuple[float, float], drone_path: list[tuple[float, float]]) -> list[tuple[float, float]]:
    result = []
    for point in drone_path:
        segment = 1
        vector = (point[0] - start[0]) / segment, (point[1] - start[1]) / segment
        for i in range(segment):
            result.append((start[0] + vector[0] * (i+1), start[1] + vector[1] * (i+1)))
        start = point
    return result
