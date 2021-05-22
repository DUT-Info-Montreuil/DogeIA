from typing import *

from .constants import *


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
		:return: return the distance
		"""
		return (self.x - x) ** 2 + (self.y - y) ** 2

	def __iter__(self):
		return (self.x, self.y).__iter__()

	def adjacent(self) -> tuple["Coordinate", "Coordinate", "Coordinate", "Coordinate"]:
		"""
		Return the current location around the Coordinate

		:return: return the coordinate for each side of the point
		"""
		x, y = self.x, self.y
		return self.board[x + 1, y], self.board[x - 1, y], self.board[x, y + 1], self.board[x, y - 1]

	def unmarked_adjacent(self):
		for adj in self.adjacent():
			if adj is not None and not adj.marked and adj.content == ROUTE:
				return adj
		return None

	def bfs_height(self):
		if self.next is None:
			return 0
		return 1 + self.next.bfs_height()

	def __eq__(self, other) -> bool:
		if isinstance(self, Coordinate):
			return self.x == other.x and self.y == other.y
		return NotImplemented

	def direction(self, other: "Coordinate") -> str:
		if self.x == other.x and self.y < other.y:
			return DIR_RIGHT
		elif self.x == other.x and self.y > other.y:
			return DIR_LEFT
		elif self.x < other.x and self.y == other.y:
			return DIR_BOTTOM
		elif self.x > other.x and self.y == other.y:
			return DIR_TOP
		return ""

	def __str__(self):
		return f"{self.x};{self.y}"


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
