from structure.client import *


class IA(Client):
	def play(self):
		board = self.map
		deliveries = self.deliveries
		bikers = self.get_bikers(self.id_team)
		others_bikers = [self.get_bikers(id_) for id_ in range(self.teams) if id_ != self.id_team]

		return self.end_and_wait_next_turn()




