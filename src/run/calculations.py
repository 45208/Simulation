from ..board import Point

def scale_vector(vector: Point, dist: float):
    mult = (vector[0] ** 2 + vector[1] ** 2) ** 0.5 / dist
    if abs(mult) > 1e-9:
        vector = (vector[0] / mult, vector[1] / mult)
    return vector
