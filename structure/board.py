import numpy as np

from .constants import BOARD_SIZE, ROUTE, EMPTY, HOME, SHOP


class Board:
	def __init__(self, data) -> None:
		"""
		Initialization of the Board Class

		:param data:
		"""
		data = data.translate(str.maketrans("REHS", "0312"))
		self.board = np.array([[int(a) for a in data[i:i + BOARD_SIZE]] for i in range(0, BOARD_SIZE * BOARD_SIZE, BOARD_SIZE)])
		self.bikers = []

	def print(self) -> None:
		"""
		Displays the board
		"""
		print(self)

	def __iter__(self):
		return self.board.__iter__()

	def __str__(self) -> str:
		return "\n".join(" ".join(str(code) for code in line) for line in self)

	def route(self, x: int, y: int) -> bool:
		return self.board[y][x] == ROUTE

	def shop(self, x: int, y: int) -> bool:
		return self.board[y][x] == SHOP

	def empty(self, x: int, y: int) -> bool:
		return self.board[y][x] == EMPTY

	def home(self, x: int, y: int) -> bool:
		return self.board[y][x] == HOME
