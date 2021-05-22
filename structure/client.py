import numpy as np
import pwn

from constants import *
from structure.board import Board
from utils import Biker, Deliverie


class Client:
	"""
	Represent a client connected to the server
	"""
	def __init__(self, host: str, port: int) -> None:
		"""
		Initialize Client class and setup socket

		:param host:
		:param port:
		"""
		self.socket = pwn.remote(host, port)
		self.socket.newline = TERMINATOR
		self.id_team = 0

	def send(self, cmd: str, *args: any) -> None:
		"""
		Method to send a command with an argument

		:param cmd:
		:param args:
		:return:
		VOID IS WATCHING
		"""
		self.send_raw(SEPARATOR.join([cmd, *[str(arg) for arg in args]]))

	def send_raw(self, msg: str) -> None:
		"""
		Method to send a message

		:param msg:
		:return:
		Nothing has been returned....
		"""
		self.socket.sendline(msg.encode())
		print(" - Sent \"{}\" to server".format(msg))

	def receive_command(self) -> list[str]:
		"""
		Method to receive
		:return:
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

		:return:
		Possibility of movement
		"""
		self.send(CMD_MOVE, delivery_number, direction)
		cmd, = self.receive_command()
		return cmd == SERVER_OK

	@property
	def teams(self) -> int:
		"""
		Method to get the number of own team

		:return:
		number of team
		"""
		self.send(CMD_TEAMS)
		_, teams = self.receive_command()
		return int(teams)

	def get_bikers(self, id_team: int) -> list[Biker]:
		"""
		Method that returns the bikers of a given team

		:param id_team:
		:return: Bikers of given team
		"""
		self.send(CMD_GETBIKERS, id_team)
		_, bikers_raw = self.receive_command()
		return [Biker(*[int(attr) for attr in biker_raw.split(";")]) for biker_raw in bikers_raw]

	@property
	def map(self) -> np.ndarray[int]:
		"""
		Method that returns the map of the game

		:return: The map
		"""
		self.send(CMD_GETMAP)
		cmd, board_raw = self.receive_command()
		return Board(board_raw)

	def take(self, nu_livr: int, code_command: int) -> bool:
		self.send(CMD_TAKE, nu_livr, code_command)
		cmd, = self.receive_command()
		return cmd == SERVER_OK

	def deliver(self, nu_livr: int, code_command: int) -> bool:
		self.send(CMD_DELIVER, nu_livr, code_command)
		cmd, = self.receive_command()
		return cmd == SERVER_OK

	@property
	def deliveries(self) -> list[Deliverie]:
		self.send(CMD_DELIVER)
		cmd, deliveries_raw = self.receive_command()
		return [Deliverie.from_raw(deliverie_raw) for deliverie_raw in deliveries_raw]

	def endturn(self) -> None:
		self.send(CMD_ENDTURN)
		_ = self.receive_command()

	def start(self) -> int:
		self.receive_command()
		self.send_raw(TEAM_NAME)
		_, id_team = self.receive_command()
		self.id_team = int(id_team)
		return self.id_team
