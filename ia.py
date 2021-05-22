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

	def play(self):
		board = self.map
		deliveries = self.deliveries
		bikers = self.get_bikers(self.id_team)
		others_bikers = [self.get_bikers(id_) for id_ in range(self.teams) if id_ != self.id_team]

		return self.end_and_wait_next_turn()




