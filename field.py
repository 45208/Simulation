import math

class Field:
    def __init__(self, type):
        self.field_type = type

        self.dimensions = {
            1: [50, 100],
            2: [150, 400],
            3: [600, 450],
        }
        
        self.height = self.dimensions[self.field_type][0]
        self.width = self.dimensions[self.field_type][1]

        self.board = [[0] * self.width for _ in range(self.height)]
        self.setBoard()

    def setBoard(self):
        if self.field_type == 1:
            self.board = [[1] * self.width for _ in range(self.height)]
        if self.field_type == 2:
            EPSILON = 0.1 ** 6

            # Divide the board into sections
            # Section 1: Left part (30-60-90 triangle)
            standard_angle = math.atan2(150 - 0, 85 + 1)

            for column in range(0, 86):
                for row in range(0, 150):
                    y = 150 - row
                    x = column + 1

                    angle = math.atan2(y, x)
                    if angle < standard_angle + EPSILON:
                        self.board[row][column] = 1

            # Section 2: Square part
            for column in range(86, 236):
                for row in range(0, 150):
                    self.board[row][column] = 1

            # Section 3: Right part (45-45-90 triangle)
            standard_angle = math.atan2(150 - 0, 386 - 236)

            for column in range(236, 386):
                for row in range(0, 150):
                    y = 150 - row
                    x = 386 - column

                    angle = math.atan2(y, x)
                    if angle < standard_angle + EPSILON:
                        self.board[row][column] = 1

    def __repr__(self):
        return "\n".join(
            [f"Field type {self.field_type}"] +
            ["".join(["-X"[cell] for cell in row]) for row in self.board]
        )
