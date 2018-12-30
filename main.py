import socket
import threading

class IRCWrapper():
	def __init__(self, irc_socket):
		self.irc_socket = irc_socket
		self.irc_channel = ' '
		print('Welcome to IRCWrapper by rogue')
		print('You can change channels by using the SWC command.')

	def send_data(self, cmd):
		self.irc_socket.send(bytes(cmd + '\n', 'utf8'))

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
				self.send_data('PONG ' + data.split()[len(data.split())-1].decode('utf8') + '\r\n')
				didnt_pong = False
		print('Pong!')

	def join_channel(self, channel):
		self.irc_channel = channel
		self.send_data('JOIN {}'.format(channel))
		print('Switched to channel: {}'.format(channel))

	def handle_user_commands(self):
		while True:
			buf = input()
			if buf == 'SWC':
				irc.join_channel(input('Channel: '))
			else:
				self.send_data(buf.replace('say', 'PRIVMSG'))

	def read_msgs(self):
		while True:
			msg = str.split(self.irc_socket.recv(1024).decode('utf8'))
			if len(msg) > 3:
				if msg[1] == 'PRIVMSG':
					print('|{0} in {1}'.format(msg[0].split('!')[0][1:], ' '.join(msg[2:]).replace(self.irc_channel + ' :', self.irc_channel + ' -> ')))

irc = IRCWrapper(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
irc.irc_conn('cathook.irc.inkcat.net', 8080)
irc.login('roguebot')
irc.pong()
irc.join_channel('#E')

threading.Thread(target=irc.handle_user_commands).start()
t = threading.Thread(target=irc.read_msgs); t.daemon = True; t.start()