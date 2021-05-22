import pwn

from .constants import *
from .board import Board
from .utils import Biker, Deliverie


class Client:
	def __init__(self, host: str, port: int) -> None:
		"""
		Initialize Client class and setup socket

		:param host:
		:param port:
		"""
		self.socket = pwn.remote(host, port)
		self.socket.newline = TERMINATOR
		self.receive_command()
		self.send_raw(TEAM_NAME)
		_, id_team = self.receive_command()
		self.id_team = int(id_team)
		self._map = None
		self._teams = None
		print(f"Started as team number {self.id_team}!")

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
		print(" - Sent \"{}\" to server".format(msg))

	def receive_command(self) -> list[str]:
		"""
		Method to receive a server-side command
		:return: The command itself
		"""
		msg = self.socket.recvline(keepends=False).decode()
		print(" - Received message \"{}\" from server".format(msg))
		cmd, *args = msg.split(SEPARATOR)
		print(" - Received command \"{}\" with args [{}] from server".format(cmd, ", ".join(args)))
		if cmd == SERVER_NOK:
			print(" - WARNING: Received a NOK command from server!\n" + SEPARATOR.join(args))
		return [cmd, *args]

	def move(self, delivery_number: int, direction: str) -> bool:
		"""
		Method to move a given biker into a given direction

		:param delivery_number:
		:param direction:

		:return: Possibility of movement
		"""
		self.send(CMD_MOVE, delivery_number, direction)
		cmd, = self.receive_command()
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

	def get_bikers(self, id_team: int) -> list[Biker]:
		"""
		Method that returns the bikers of a given team

		:param id_team:
		:return: Bikers of given team
		"""
		self.send(CMD_GETBIKERS, id_team)
		_, *bikers_raw = self.receive_command()
		return [Biker(*[int(attr) for attr in biker_raw.split(";")]) for biker_raw in bikers_raw]

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
		cmd, = self.receive_command()
		return cmd == SERVER_OK

	def deliver(self, nu_livr: int, code_command: int) -> bool:
		"""
		The biker delivers the command to the house

		:param nu_livr:
		:param code_command:
		:return: If the command was receved by the recipient or not
		"""
		self.send(CMD_DELIVER, nu_livr, code_command)
		cmd, = self.receive_command()
		return cmd == SERVER_OK

	@property
	def deliveries(self) -> list[Deliverie]:
		"""
		Method to get all the available commands on the board

		:return: A list of availables deliveries
		"""
		self.send(CMD_GETDELIVERIES)
		cmd, *deliveries_raw = self.receive_command()
		return [Deliverie.from_raw(deliverie_raw) for deliverie_raw in deliveries_raw]

	def end_and_wait_next_turn(self) -> bool:
		"""
		Ends the turn when there is no PA left and waitfor the next turn that matches the team's ID

		:return: When you stare at the void...
		"""
		self.send(CMD_ENDTURN)
		self.receive_command()  # End turn acknowledgement
		cmd, _ = self.receive_command()  # Wait until next turn
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
