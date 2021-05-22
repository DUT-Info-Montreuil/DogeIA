from typing import *
import numpy as np

from constants import BOARD_SIZE


class Coordinate:
	def __init__(self, x: int, y: int) -> None:
		self.x = x
		self.y = y


class Deliverie(NamedTuple):
	@staticmethod
	def from_raw(resp: str) -> 'Deliverie':
		"""
		Static method to

		:param resp:
		:return:
		"""
		args = resp.split(";")
		return Deliverie(
			int(args[0]),
			float(args[2].replace(",", ".")),
			Coordinate(int(args[3]), int(args[4])),
			Coordinate(int(args[5]), int(args[6])),
			int(args[7])
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
