from .board import Board

SCALE = 5
BOARD1 = (.0, .0), (100.0, .0), (100.0, 50.0), (.0, 50.0)
BOARD2 = (.0, .0), (386.6025, .0), (236.6025, 150.0), (86.6025, 150.0)
BOARD3 = (.0, .0), (450.0, .0), (450.0, 150.0), (150.0, 150.0), (300.0, 600.0), (.0, 450.0)

board1 = Board(BOARD1, SCALE)
board2 = Board(BOARD2, SCALE)
board3 = Board(BOARD3, SCALE)
