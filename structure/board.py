from queue import Queue
from typing import *

from .constants import BOARD_SIZE, ROUTE, EMPTY, HOME, SHOP, MAP
from .utils import Coordinate


class Board:
	def __init__(self, data) -> None:
		"""
		Initialization of the Board Class

		:param data:
		"""
		self.board = []
		for x in range(BOARD_SIZE):
			for y in range(BOARD_SIZE):
				self.board.append(Coordinate(x, y, self, int(MAP[data[x * BOARD_SIZE + y]])))
		self.bikers = []

	def __getitem__(self, pos: tuple[int, int]) -> Optional[Coordinate]:
		x = pos[0]
		y = pos[1]
		if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
			return None
		return self.board[x * BOARD_SIZE + y]

	def print(self) -> None:
		"""
		Displays the board
		"""
		for x in range(BOARD_SIZE):
			for y in range(BOARD_SIZE):
				print(self[x, y].content, end=" ")
			print()

	def route(self, x: int, y: int) -> bool:
		"""
		return true if (x,y) is the location of a road

		:param x:
		:param y:
		:return: a boolean
		"""
		tile = self[x, y]
		return tile is not None and tile.content == ROUTE

	def shop(self, x: int, y: int) -> bool:
		"""
		return true if (x,y) is the location of a shop

		:param x:
		:param y:
		:return: a boolean
		"""
		tile = self[x, y]
		return tile is not None and tile.content == SHOP

	def empty(self, x: int, y: int) -> bool:
		"""
		return true if (x,y) is an empty the location

		:param x:
		:param y:
		:return: a boolean
		"""
		tile = self[x, y]
		return tile is not None and tile.content == EMPTY

	def home(self, x: int, y: int) -> bool:
		"""
		return true if (x,y) is the location of a home

		:param x:
		:param y:
		:return: a boolean
		"""
		tile = self[x, y]
		return tile is not None and tile.content == HOME

	def clear_bfs(self):
		for coord in self.board:
			coord.marked = False
			coord.next = None

	def bfs(self, pos: Coordinate) -> None:
		self.clear_bfs()
		q: Queue[Coordinate] = Queue()
		pos.marked = True
		q.put(pos)

		while not q.empty():
			c = q.get()
			while True:
				d = c.unmarked_adjacent()
				if d is None:
					break
				d.marked = True
				d.next = c
				q.put(d)
