from .board import Board

SCALE = 5
BOARD1 = (.0, .0), (100.0, .0), (100.0, 50.0), (.0, 50.0)
TERM1 = ((50, 0),)

BOARD2 = (.0, .0), (386.6025, .0), (236.6025, 150.0), (86.6025, 150.0)
TERM2 = ((186, 0),)

BOARD3 = (.0, .0), (450.0, .0), (450.0, 150.0), (150.0, 150.0), (300.0, 600.0), (.0, 450.0)
TERM3 = ((0, 300), (300, 150))

board1 = Board(BOARD1, TERM1, SCALE)
board2 = Board(BOARD2, TERM2, SCALE)
board3 = Board(BOARD3, TERM3, SCALE)
