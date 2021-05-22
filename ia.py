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

		biker = self.bikers[0]
		actions = ACTION_POINTS
		while actions > 0:
			pos = biker.pos
			if len(biker.carrying) == 0:
				# We find the closest delivery to take from the deliveries list
				path, delivery = board.nearest_delivery_to_take(deliveries, pos)
				if path is None:
					return self.end_and_wait_next_turn()
				shop = True

				# board.bfs(pos)
				# closest = None
				# min_height = 0
				# for delivery in deliveries:
				# 	height = delivery.coord_restaurant.bfs_height()
				# 	if closest is None or height <= min_height:
				# 		closest = delivery
				# 		min_height = height
				# dest = closest.coord_restaurant
			elif len(biker.carrying) < 3:
				# We find the closest delivery to take from the deliveries list OR to deliver from the biker's backpack
				path_take, delivery_take = board.nearest_delivery_to_take(deliveries, pos)
				path_depose, delivery_depose = board.nearest_delivery_to_depose(biker.carrying, pos)
				if path_take is None or (path_depose is not None and len(path_depose) < len(path_take)):
					path, delivery = path_depose, delivery_depose
					shop = False
				elif path_depose is None or (path_take is not None and len(path_take) < len(path_depose)):
					path, delivery = path_take, delivery_take
					shop = True
				else:
					return self.end_and_wait_next_turn()

				# board.bfs(pos)
				# closest = None
				# min_height = 0
				# maison = False
				# for delivery in deliveries + biker.carrying:
				# 	height = delivery.coord_restaurant.bfs_height()
				# 	if closest is None or height <= min_height:
				# 		closest = delivery
				# 		min_height = height
				# 		maison = False
				# 	height = delivery.coord_maison.bfs_height()
				# 	if closest is None or height <= min_height and delivery in biker.carrying:
				# 		closest = delivery
				# 		min_height = height
				# 		maison = True
				# if maison:
				# 	dest = closest.coord_maison
				# 	delivery = biker.carrying[0]
				# else:
				# 	dest = closest.coord_restaurant
			else:
				# We find the closest delivery to deliver from the biker's backpack
				path, delivery = board.nearest_delivery_to_depose(biker.carrying, pos)
				if path is None:
					return self.end_and_wait_next_turn()
				shop = False

			print(pos, path, delivery.coord_restaurant)
			if len(path):
				dir_ = path[0]
				self.move(biker.nu, dir_)
				biker.pos = pos.next_in_direction(dir_)
			elif shop:
				self.take(biker.nu, delivery.code)
				biker.carrying.append(delivery)
				for delivery in deliveries:
					if delivery.coord_restaurant == next \
							and delivery not in biker.carrying \
							and len(biker.carrying) < 3 \
							and actions > 1:
						self.take(biker.nu, delivery.code)
						biker.carrying.append(delivery)
						actions -= 1
			else:
				self.deliver(biker.nu, delivery.code)
				biker.carrying.remove(delivery)

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
