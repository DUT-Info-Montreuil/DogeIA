from typing import *


class Coordinate:
	def __init__(self, x: int, y: int) -> None:
		self.x = x
		self.y = y

	def dist(self, x: int, y: int) -> int:
		"""
		Return the distance between 2 points.

		:param x:
		:param y:
		:return: return the distznce
		"""
		return abs((self.x - x) + (self.y + y))

	def __iter__(self):
		return (self.x, self.y).__iter__()

	def adjacent(self) -> tuple["Coordinate", "Coordinate", "Coordinate", "Coordinate"]:
		"""
		Returnthe location aroudn 

		:return:
		"""
		x, y = self.x, self.y
		return Coordinate(x + 1, y), Coordinate(x - 1, y), Coordinate(x, y + 1), Coordinate(x, y - 1)


class Deliverie(NamedTuple):
	@staticmethod
	def from_raw(resp: str) -> "Deliverie":
		"""
		Static method to

		:param resp:
		:return:
		"""
		args = resp.split(";")
		return Deliverie(
			int(args[0]),
			float(args[1].replace(",", ".")),
			Coordinate(int(args[2]), int(args[3])),
			Coordinate(int(args[4]), int(args[5])),
			int(args[6])
		)

	code: int
	valeur: float
	coord_restaurant: Coordinate
	coord_maison: Coordinate
	limit_turn: int


class Biker:
	def __init__(self, nu: int, x: int, y: int) -> None:
		self.nu = nu
		self.x = x
		self.y = y
