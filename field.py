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
        pass

    def __repr__(self):
        return "\n".join(
            [f"Field type {self.field_type}"] +
            ["".join(["-X"[cell] for cell in row]) for row in self.board]
        )
