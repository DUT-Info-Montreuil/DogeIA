from structure.client import *
from structure.utils import Coordinate
from pathfinding.finder.best_first import BestFirst
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement


class IA(Client):
	"""
	The Class of the AI
	"""
	def __init__(self, host: str, port: int):
		super().__init__(host, port)

	def play(self) -> bool:
		board = self.map
		deliveries = self.deliveries
		bikers = self.get_bikers(self.id_team)
		others_bikers = [self.get_bikers(id_) for id_ in range(self.teams) if id_ != self.id_team]

		delivery = min(deliveries, key=lambda d: d.coord_restaurant.dist(0, 0))
		x, y = self.get_route_neighbor(delivery.coord_restaurant)
		grid = Grid(matrix=self.map)
		finder = BestFirst(
			heuristic=None,
			weight=31,
			diagonal_movement=DiagonalMovement.never,
			time_limit=float("inf"),
			max_runs=float("inf")
		)
		path, runs = finder.find_path(start=grid.node(x=bikers[0].x, y=bikers[1].y), end=grid.node(x, y), grid=grid)




		return self.end_and_wait_next_turn()

	def get_route_neighbor(self, coord: Coordinate):
		for adj in coord.adjacent():
			if self.map.route(adj.x, adj.y):
				return coord
		return None







