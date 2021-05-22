from queue import Queue
from typing import *

from .constants import BOARD_SIZE, ROUTE, EMPTY, HOME, SHOP, MAP
from .utils import Coordinate, pathify, Delivery


class Board:
	def __init__(self, data) -> None:
		"""
		Initialization of the Board Class

		:param data:
		"""
		self.content = []
		for x in range(BOARD_SIZE):
			for y in range(BOARD_SIZE):
				self.content.append(Coordinate(x, y, self, int(MAP[data[x * BOARD_SIZE + y]])))
		self.bikers = []
		self.graph = {}
		for x in range(BOARD_SIZE):
			for y in range(BOARD_SIZE):
				coord = self[x, y]
				if coord.content == ROUTE:
					self.graph[coord] = self.neighbors_routes(coord)
		self.__build_all_paths()

	def __build_all_paths(self):
		"""
		Generates every paths possible.

		:return:
		"""
		self.paths = {}
		for c1 in self.graph:
			bfs = self.bfs2(c1)
			for c2 in self.graph:
				self.paths[(c1, c2)] = bfs[c2]

	def bfs2(self, coord: Coordinate):
		"""
		Explores the map and save the path for every coord.

		:param coord:
		:return: the path for every coord
		"""

		explored = {coord: None}
		queue = [coord]
		while queue:
			sommet = queue.pop(0)
			for adjacent in self.graph[sommet]:
				if adjacent not in explored:
					explored[adjacent] = sommet
					queue.append(adjacent)

		return {coord: pathify(explored, coord)[::-1] for coord in explored}

	def shortest(self, coord1: Coordinate, coord2: Coordinate):
		"""
		Returns the shortest path between the 2 coord.

		:param coord1:
		:param coord2:
		:return: a shortest path
		"""
		return self.paths[(coord1, coord2)]

	def neighbors_routes(self, coord: Coordinate):
		"""
		Returns every road paths auround coord.

		:param coord:
		:return: a location
		"""
		nears = []
		for near in coord.adjacent():
			if near:
				x = near.x
				y = near.y
				if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and near.content == ROUTE:
					nears.append(near)
		return nears

	def nearest_delivery_to_take(self, deliveries: list[Delivery], coord: Coordinate) -> Tuple[Optional[str], Optional[Delivery]]:
		"""
		Returns the shortest_path in order to get the nearest delivery from a location.

		:param deliveries:
		:param coord:
		:return: a path
		"""

		shortest_path = None
		delivery_near = None
		for delivery in deliveries:
			coords_routes = self.neighbors_routes(delivery.coord_restaurant)
			for coord_route in coords_routes:
				path = self.shortest(coord, coord_route)
				if shortest_path is None or len(path) < len(shortest_path):
					shortest_path = path
					delivery_near = delivery
		return shortest_path, delivery_near

	def nearest_delivery_to_depose(self, deliveries: list[Delivery], coord: Coordinate) -> Tuple[Optional[str], Optional[Delivery]]:
		shortest_path = None
		delivery_near = None
		for delivery in deliveries:
			coords_routes = self.neighbors_routes(delivery.coord_maison)
			for coord_route in coords_routes:
				path = self.shortest(coord, coord_route)
				if shortest_path is None or len(path) < len(shortest_path):
					shortest_path = path
					delivery_near = delivery
		return shortest_path, delivery_near

	def __getitem__(self, pos: tuple[int, int]) -> Optional[Coordinate]:
		x = pos[0]
		y = pos[1]
		if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
			return None
		return self.content[x * BOARD_SIZE + y]

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
		for coord in self.content:
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
