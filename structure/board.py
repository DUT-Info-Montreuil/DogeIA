import numpy as np

from constants import BOARD_SIZE


class Board:
	def __init__(self, data) -> None:
		"""
		Initialization of the Board Class
		:param data:
		"""
		data = data.translate(str.maketrans("REHS", "0312"))
		self.board = np.array([[int(a) for a in data[i:i + BOARD_SIZE]] for i in range(0, BOARD_SIZE * BOARD_SIZE, BOARD_SIZE)])

	def print(self) -> None:
		"""
		Display board
		"""
		print(self)

	def __iter__(self):
		return self.board.__iter__()

	def __str__(self) -> str:
		return "\n".join(" ".join(code for code in line) for line in self)
