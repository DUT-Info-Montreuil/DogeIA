from typing import *


class Coordinate:
	def __init__(self, x: int, y: int, board=None, content: int = -1) -> None:
		"""
		Initializes Coordinate

		:param x:
		:param y:
		:return: none
		"""
		self.x = x
		self.y = y
		self.board = board
		self.content = content
		self.next = None
		self.marked = False

	def dist_coords(self, other: "Coordinate"):
		return self.dist(other.x, other.y)

	def dist(self, x: int, y: int) -> int:
		"""
		Return the distance between 2 points.

		:param x:
		:param y:
		:return: return the distznce
		"""
		return (self.x - x) ** 2 + (self.y - y) ** 2

	def __iter__(self):
		return (self.x, self.y).__iter__()

	def adjacent(self) -> tuple["Coordinate", "Coordinate", "Coordinate", "Coordinate"]:
		"""
		Returnthe location aroudn the oi

		:return:
		"""
		x, y = self.x, self.y
		return self.board[x + 1, y], self.board[x - 1, y], self.board[x, y + 1], self.board[x, y - 1]


class Delivery(NamedTuple):
	@staticmethod
	def from_raw(board, resp: str) -> "Delivery":
		"""
		Static method to

		:param board:
		:param resp:
		:return:
		"""
		args = resp.split(";")
		return Delivery(
			int(args[0]),
			float(args[1].replace(",", ".")),
			board[int(args[2]), int(args[3])],
			board[int(args[4]), int(args[5])],
			int(args[6])
		)

	code: int
	valeur: float
	coord_restaurant: Coordinate
	coord_maison: Coordinate
	limit_turn: int


class Biker:
	def __init__(self, board, nu: int, x: int, y: int) -> None:
		"""
		Inititalizes the biker

		:param nu:
		:param x:
		:param y:
		:return: none
		"""
		self.nu = nu
		self.pos = board[x, y]
		self.carrying = []
