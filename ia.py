from structure.client import *
from structure.utils import Coordinate


class IA(Client):
	"""
	The Class of the AI
	"""
	def __init__(self, host: str, port: int):
		super().__init__(host, port)
		self.turn = 0
		self.bikers = None
		self.biker = None

	def play(self) -> bool:
		"""
		Method to start the game and initialize bikers , deliveries and such
		:return:
		If the game is playing or not
		"""
		self.turn += 1
		board = self.map
		if self.bikers is None:
			self.bikers = self.get_bikers(self.id_team)
		deliveries = self.deliveries
		# others_bikers = [self.get_bikers(id_) for id_ in range(self.teams) if id_ != self.id_team]

		actions = ACTION_POINTS
		while actions > 0:
			pos = biker.pos
			if len(biker.carrying) == 0:
				# We find the closest delivery to take from the deliveries list
				path, delivery = board.nearest_delivery_to_take(deliveries, pos)
				if path is None:
					return self.end_and_wait_next_turn()
				shop = True
			elif len(self.biker.carrying) < 3:
				# We find the closest delivery to take from the deliveries list OR to deliver from the biker's backpack
				path_take, delivery_take = board.nearest_delivery_to_take(deliveries, self.biker.pos)
				path_depose, delivery_depose = board.nearest_delivery_to_depose(self.biker.carrying, self.biker.pos)
				if path_take is None or (path_depose is not None and len(path_depose) < len(path_take)):
					path, delivery = path_depose, delivery_depose
					shop = False
				elif path_depose is None or (path_take is not None and len(path_take) < len(path_depose)):
					path, delivery = path_take, delivery_take
					shop = True
				else:
					return self.end_and_wait_next_turn()
			else:
				# We find the closest delivery to deliver from the biker's backpack
				path, delivery = board.nearest_delivery_to_depose(self.biker.carrying, self.biker.pos)
				if path is None:
					return self.end_and_wait_next_turn()
				shop = False

			if path:
				dir_ = path[0]
				self.move(self.biker.nu, dir_)
				self.biker.pos = self.biker.pos.next_in_direction(dir_)
			elif shop:
				self.take(self.biker.nu, delivery.code)
				self.biker.carrying.add(delivery)
				deliveries.remove(delivery)
				# for delivery in deliveries:
				# 	if delivery.coord_restaurant == next \
				# 			and delivery not in self.biker.carrying \
				# 			and len(self.biker.carrying) < 3 \
				# 			and actions > 1:
				# 		self.take(self.biker.nu, delivery.code)
				# 		self.biker.carrying.append(delivery)
				# 		actions -= 1
			else:
				self.deliver(self.biker.nu, delivery.code)
				self.biker.carrying.remove(delivery)

			actions -= 1

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
