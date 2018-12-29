import socket
import threading

class IRCWrapper():
	def __init__(self, irc_socket):
		self.irc_socket = irc_socket
		print('Welcome to IRCWrapper by rogue')
		print('You can change channels by using the SWC command.')

	def send_data(self, cmd):
		self.irc_socket.send(cmd.encode('utf8') + b'\n')

	def irc_conn(self, server, port):
		self.irc_socket.connect((server, port))
		print('Connected to {0}:{1}'.format(server, port))

	def login(self, username, realname = 'not', hostname = 'used', servername = '.'):
		self.send_data('NICK {}'.format(username))
		self.send_data('USER {0} {1} {2} :{3}'.format(username, hostname, servername, realname))
		print('Logged in as {}'.format(username))

	def pong(self):
		didnt_pong = True
		while didnt_pong:
			data = self.irc_socket.recv(4096)
			if data.find(b'PING :') != -1:
				self.send_data('PONG ' + data.split()[9].decode('utf8') + '\r\n')
				didnt_pong = False
		print('Pong!')

	def join_channel(self, channel):
		self.send_data('JOIN {}'.format(channel))
		print('Switched to channel: {}'.format(channel))

	def send_user_msg(self):
		while True:
			buf = input('Command: ')
			if buf == 'SWC':
				irc.join_channel(input('Channel: '))
			else:
				self.send_data(buf)

	def read_msgs(self):
		while True:
			msg = str.split(self.irc_socket.recv(1024).decode('utf8'))
			if msg[1] == 'PRIVMSG':
				print('\n {0} in {1}'.format(msg[0], ' '.join(msg[2:])))

irc = IRCWrapper(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
irc.irc_conn('cathook.irc.inkcat.net', 8080)
irc.login('roguebot')
irc.pong()
irc.join_channel('#cat_coms')

threading.Thread(target=irc.send_user_msg).start()
threading.Thread(target=irc.read_msgs).start()