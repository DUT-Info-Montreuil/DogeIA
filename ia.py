from structure.client import *


class IA(Client):
	def play(self):
		board = self.get_map()
		deliveries = self.get_deliveries()
		bikers = self.get_bikers(self.)


		self.endturn()


