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

	def __repr__(self):
		"""
		Print the details of the coordinate

		:return:
		"""
		return self.__str__()

	def __hash__(self) -> int:
		return self.x + self.y * 31

	def __eq__(self, other: object) -> int:
		if isinstance(other, Coordinate):
			return self.x == other.x and self.y == other.y
		return NotImplemented

	def dist_coords(self, other: "Coordinate"):
		"""
		Returns the distance between the current Coordinate and other.

		:param other:
		:return: a distance
		"""
		return self.dist(other.x, other.y)

	def dist(self, x: int, y: int) -> int:
		"""
		Returns the distance between 2 points.

		:param x:
		:param y:
		:return: distance
		"""
		return (self.x - x) ** 2 + (self.y - y) ** 2

	def __iter__(self):

		return (self.x, self.y).__iter__()

	def adjacent(self) -> tuple["Coordinate", "Coordinate", "Coordinate", "Coordinate"]:
		"""
		Return the current location around the Coordinate.

		:return: return the coordinate for each side of the point
		"""
		x, y = self.x, self.y
		return self.board[x + 1, y], self.board[x - 1, y], self.board[x, y + 1], self.board[x, y - 1]

	def unmarked_adjacent(self):
		"""
		Returns the road location around a point.

		:return: a road location
		"""

		for adj in self.adjacent():
			if adj is not None and not adj.marked and adj.content == ROUTE:
				return adj
		return None

	def bfs_height(self):
		"""
		Returns each height of a bfs path.

		:return: integer
		"""
		if self.next is None:
			return 0
		return 1 + self.next.bfs_height()

	def direction(self, other: "Coordinate") -> str:
		"""
		Gives the next location in order to arrive at other.

		:param other:
		:return: a letter for the direction
		"""

		if self.x == other.x and self.y < other.y:
			return DIR_RIGHT
		elif self.x == other.x and self.y > other.y:
			return DIR_LEFT
		elif self.x < other.x and self.y == other.y:
			return DIR_BOTTOM
		elif self.x > other.x and self.y == other.y:
			return DIR_TOP
		return ""

	def next_in_direction(self, direction: str) -> Optional["Coordinate"]:
		if direction == DIR_TOP:
			return self.board[self.x - 1, self.y]
		elif direction == DIR_BOTTOM:
			return self.board[self.x + 1, self.y]
		elif direction == DIR_LEFT:
			return self.board[self.x, self.y - 1]
		elif direction == DIR_RIGHT:
			return self.board[self.x, self.y + 1]

	def __str__(self):
		"""
		Return coodinate

		:return: Coordinate
		"""
		return f"{self.x};{self.y}"


def pathify(bfs: dict[Coordinate, Coordinate], coord: Coordinate) -> str:
	"""
	Looking for a path to coord.

	:param bfs:
	:param coord:
	:return: a path
	"""
	prev = bfs[coord]
	if coord is None or prev is None:
		return ""
	dx = coord.x - prev.x
	dy = coord.y - prev.y
	return DPOS[(dx, dy)] + pathify(bfs, prev)


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
