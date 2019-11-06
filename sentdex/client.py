import socket
import select
import errno
import sys

from threading import Thread
from socket import AF_INET, SOCK_STREAM


HEADER_LENGTH = 10
ENC8 = 'utf-8'

IP = '32.226.165.83'
PORT = 5679

my_username = input('Username: ')
client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode(ENC8)
username_header = f"{len(username):<{HEADER_LENGTH}}".encode(ENC8)
client_socket.send(username_header + username)


while True:
	message = input(f"{my_username}: ")

	if message:
		message = message.encode(ENC8)
		message_header = f"{len(message):<{HEADER_LENGTH}}".encode(ENC8)
		client_socket.send(message_header + message)

	try:
		while True:
			# receive 
			username_header = client_socket.recv(HEADER_LENGTH)

			if not len(username_header):
				print(f"Connection closed by server")
				sys.exit()

			username_length = int(username_header.decode(ENC8).strip())
			username = client_socket.recv(username_length).decode(ENC8)

			message_header = client_socket.recv(HEADER_LENGTH)
			message_length = int(message_header.decode(ENC8).strip())
			message = client_socket.recv(message_length).decode(ENC8)

			print(f"{username} > {message}")

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		continue

	except Exception as e:
		print('General error', str(e))
		sys.exit()


"""
def receive():
	while True:
		try:
			while True:
				# receive 
				username_header = client_socket.recv(HEADER_LENGTH)

				if not len(username_header):
					print(f"Connection closed by server")
					sys.exit()

				username_length = int(username_header.decode(ENC8).strip())
				username = client_socket.recv(username_length).decode(ENC8)

				message_header = client_socket.recv(HEADER_LENGTH)
				message_length = int(message_header.decode(ENC8).strip())
				message = client_socket.recv(message_length).decode(ENC8)

				print(f"  {username} > {message}")

		except IOError as e:
			if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
				print('Reading error', str(e))
				sys.exit()
			continue

		except Exception as e:
			print('General error', str(e))
			sys.exit()


def send():
	while True:
		try:
			message = input(f"")

			if message:
				message = message.encode(ENC8)
				message_header = f"{len(message):<{HEADER_LENGTH}}".encode(ENC8)
				client_socket.send(message_header + message)

		except KeyboardInterrupt as e:
			print('Client closed', str(e))
			sys.exit()

if __name__ == "__main__":
	receive_thread = Thread(target=receive)
	receive_thread.start()

	send_thread = Thread(target=send)
	send_thread.start()"""
















