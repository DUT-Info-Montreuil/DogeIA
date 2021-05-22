import pwn

from .constants import *
from .board import Board
from .utils import Biker, Delivery


class Client:
	def __init__(self, host: str, port: int) -> None:
		"""
		Initialize Client class and setup socket

		:param host:
		:param port:
		"""
		self.socket = pwn.remote(host, port)
		self.socket.newline = TERMINATOR
		pwn.context.log_level = "info"
		self.receive_command()
		self.send_raw(TEAM_NAME)
		_, id_team = self.receive_command()
		self.id_team = int(id_team)
		self._map = None
		self._teams = None
		self._bikers = {}
		pwn.log.info(f"Started as team number {self.id_team}!")

	def send(self, cmd: str, *args: any) -> None:
		"""
		Method to send a command with an argument

		:param cmd:
		:param args:
		:return: VOID IS WATCHING
		"""
		self.send_raw(SEPARATOR.join([cmd, *[str(arg) for arg in args]]))

	def send_raw(self, msg: str) -> None:
		"""
		Method to send a message

		:param msg:
		:return: Nothing has been returned....
		"""
		self.socket.sendline(msg.encode())
		pwn.log.info(f"Sent \"{msg}\" to server")

	def receive_command(self) -> list[str]:
		"""
		Method to receive a server-side command
		:return: The command itself
		"""
		msg = self.socket.recvline(keepends=False).decode()
		pwn.log.info(f"Received message \"{msg}\" from server")
		cmd, *args = msg.split(SEPARATOR)
		joined_args = ", ".join(args)
		pwn.log.info(f"Received command \"{cmd}\" with args [{joined_args}] from server")
		if cmd == SERVER_NOK:
			pwn.log.warn(f"Received a NOK command from server!\n{SEPARATOR.join(args)}")
		return [cmd, *args]

	def move(self, biker_number: int, direction: str) -> bool:
		"""
		Method to move a given biker into a given direction

		:param biker_number:
		:param direction:

		:return: Possibility of movement
		"""
		self.send(CMD_MOVE, biker_number, direction)
		cmd, *_ = self.receive_command()
		return cmd == SERVER_OK

	@property
	def teams(self) -> int:
		"""
		Method to get the number of own team

		:return: number of team
		"""
		if self._teams is None:
			self.send(CMD_TEAMS)
			_, teams = self.receive_command()
			self._teams = int(teams)
		return self._teams

	def get_bikers(self, id_team: int) -> dict[int, Biker]:
		"""
		Method that returns the bikers of a given team

		:param id_team:
		:return: Bikers of given team
		"""
		self.send(CMD_GETBIKERS, id_team)
		_, *bikers_raw = self.receive_command()
		for biker_raw in bikers_raw:
			id_, x, y = [int(attr) for attr in biker_raw.split(";")]
			if id_ in self._bikers:
				biker = self._bikers[id_]
				biker.pos.x = x
				biker.pos.y = y
			else:
				self._bikers[id_] = Biker(self._map, id_, x, y)
		return self._bikers

	@property
	def map(self) -> Board:
		"""
		Method that returns the map of the game

		:return: The map
		"""
		if self._map is None:
			self.send(CMD_GETMAP)
			cmd, board_raw = self.receive_command()
			self._map = Board(board_raw)
		return self._map

	def take(self, nu_livr: int, code_command: int) -> bool:
		"""
		The biker takes a command from a restaurant

		:param nu_livr:
		:param code_command:
		:return: If he took the command or not
		"""
		self.send(CMD_TAKE, nu_livr, code_command)
		cmd, *_ = self.receive_command()
		return cmd == SERVER_OK

	def deliver(self, nu_livr: int, code_command: int) -> bool:
		"""
		The biker delivers the command to the house

		:param nu_livr:
		:param code_command:
		:return: If the command was receved by the recipient or not
		"""
		self.send(CMD_DELIVER, nu_livr, code_command)
		cmd, *_ = self.receive_command()
		return cmd == SERVER_OK

	@property
	def deliveries(self) -> list[Delivery]:
		"""
		Method to get all the available commands on the board

		:return: A list of availables deliveries
		"""
		self.send(CMD_GETDELIVERIES)
		cmd, *deliveries_raw = self.receive_command()
		return [Delivery.from_raw(self._map, deliverie_raw) for deliverie_raw in deliveries_raw]

	def end_and_wait_next_turn(self) -> bool:
		"""
		Ends the turn when there is no PA left and waitfor the next turn that matches the team's ID

		:return: When you stare at the void...
		"""
		self.send(CMD_ENDTURN)
		self.receive_command()  # End turn acknowledgement
		cmd, *_ = self.receive_command()  # Wait until next turn
		return cmd == SERVER_START

	def start(self) -> int:
		"""
		Starts the game, initializes the team's name and receive it's ID

		:return: The id of our team
		"""
		self.receive_command()
		self.send_raw(TEAM_NAME)
		_, id_team = self.receive_command()
		self.id_team = int(id_team)
		return self.id_team
