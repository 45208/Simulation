import math
from collections import deque
from matplotlib import pyplot as plt

Point = tuple[float, float]

class Board:
    xp, yp = [0, -1, 0, 1], [-1, 0, 1, 0]
    EPSILON = 1e-7

    def __init__(self, vertices: tuple[Point], terminals: tuple[Point], scale: int):
        self.vertices = [(vertex[0] * self.scale, vertex[1] * self.scale)
                         for vertex in vertices]
        self.terminals = terminals
        self.scale = scale

        assert len(self.vertices) > 2

        self.size = 0
        for Point in self.vertices:
            self.size = max(self.size, Point[0], Point[1])
        self.size = math.ceil(self.size)

        self.board = [[False for _ in range(self.size)]
                      for _ in range(self.size)]
        self.__calculate_board()

    def __crossed(self, cx: float, cy: float, nx: float, ny: float) -> bool:
        def __counter_clockwise(a: Point, b: Point, c: Point) -> float:
            return (a[0]-b[0])*c[1] + (b[0]-c[0])*a[1] + (c[0]-a[0])*b[1]

        def __different_half_plane(x: Point, y: Point, a: Point, b: Point) -> bool:
            return __counter_clockwise(x, a, b) * __counter_clockwise(y, a, b) < self.EPSILON

        def __intersected(c: Point, n: Point, a: Point, b: Point) -> bool:
            return __different_half_plane(c, n, a, b) and __different_half_plane(a, b, c, n)

        for i in range(len(self.vertices)):
            a, b = self.vertices[i-1], self.vertices[i]
            if __intersected((cx, cy), (nx, ny), a, b):
                return True
        return False

    def __calculate_board(self) -> None:
        queue = deque()
        queue.append((0, 0))
        while len(queue):
            cx, cy = queue.popleft()
            for xa, ya in zip(self.xp, self.yp):
                nx, ny = cx + xa, cy + ya
                if self.__crossed(cx + .5, cy + .5, nx + .5, ny + .5):
                    continue
                if self.board[nx][ny]:
                    continue
                self.board[nx][ny] = 1
                queue.append((nx, ny))

    def to_image(self, fname: str, **kwargs) -> None:
        board = []
        for y in range(self.size):
            board.append([])
            for x in range(self.size):
                result = None
                match self.board[x][y]:
                    case 0:
                        result = 0, 0, 0, 0
                    case 1:
                        result = 90, 228, 165, 255
                    case 2:
                        result = 204, 201, 72, 255
                board[-1].append(result)
        plt.axis('off')
        window = plt.imshow(board, origin="lower")
        window.write_png(fname)

    def __repr__(self):
        s = ""
        for y in range(self.size-1, -1, -1):
            for x in range(self.size):
                s += 'X' if self.board[x][y] else '-'
            s += '\n'
        return s
