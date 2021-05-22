from structure.client import *
from structure.utils import Coordinate


class IA(Client):
	"""
	The Class of the AI
	"""
	def __init__(self, host: str, port: int):
		super().__init__(host, port)

	def play(self) -> bool:
		board = self.map
		# board.print()
		# others_bikers = [self.get_bikers(id_) for id_ in range(self.teams) if id_ != self.id_team]

		bikers = self.get_bikers(self.id_team)
		biker = bikers[0]
		for i in range(8):
			deliveries = self.deliveries
			if len(biker.carrying) == 0:
				board.bfs(biker.pos)
				closest = None
				min_height = 0
				for delivery in deliveries:
					height = delivery.coord_restaurant.bfs_height()
					if closest is None or height <= min_height:
						closest = delivery
						min_height = height
				dest = closest.coord_restaurant
			else:
				delivery = biker.carrying[0]
				dest = delivery.coord_maison

			# print(dest)
			board.bfs(dest)
			pos = biker.pos
			next = pos.next
			if next.content == ROUTE:
				# print(pos, next)
				self.move(biker.nu, pos.direction(next))
				biker.pos = next
			elif next.content == SHOP:
				self.take(biker.nu, closest.code)
				biker.carrying.append(closest)
			elif next.content == HOME:
				self.deliver(biker.nu, delivery.code)
				biker.carrying.remove(delivery)

		return self.end_and_wait_next_turn()

	def get_route_neighbor(self, coord: Coordinate):
		"""
		Find a route near to coord

		:param coord:
		:return: Coordinate of a road location
		"""
		for adj in coord.adjacent():
			if self.map.route(adj.x, adj.y):
				return coord
		return None



