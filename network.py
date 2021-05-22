from enum import Enum

import pwn

SEPARATOR = "|"
TERMINATOR = "\r\n"


class Cmd(Enum):
	MOVE = "MOVE"
	TEAMS = "TEAMS"
	GETBIKERS = "GETBIKERS"
	GETMAP = "GETMAP"
	GETDELIVERIES = "GETDELIVERIES"
	TAKE = "TAKE"
	DELIVER = "DELIVER"
	ENDTURN = "ENDTURN"
	SCORE = "SCORE"


class ServerCmd(Enum):
	OK = "OK"
	NOK = "NOK"
	NAME = "NAME"
	START = "START"
	ENDGAME = "ENDGAME"


class Connection:
	def __init__(self, host, port):
		self.socket = pwn.remote(host, port)
		self.socket.newline = TERMINATOR

	def send(self, cmd, *args):
		self.send_raw(SEPARATOR.join([cmd, *args]))

	def send_raw(self, msg):
		self.socket.sendline(msg.encode())
		print(" - Sent \"{}\" to server".format(msg))

	def receive_command(self):
		msg = self.socket.recvline(keepends=False).decode()
		print(" - Received message \"{}\" from server".format(msg))
		cmd, *args = msg.split(SEPARATOR)
		print(" - Received command \"{}\" with args [{}] from server".format(cmd, ", ".join(args)))
		if cmd == Cmd.SERVER_NOK:
			print(" - WARNING: Received a NOK command from server!\n" + SEPARATOR.join(args))
		return [cmd, *args]
