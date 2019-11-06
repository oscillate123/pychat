import socket
import select
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234
ENC8 = 'utf-8'

server_socket = socket.socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen(10)

sockets_list = [server_socket]

clients = {}



def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HEADER_LENGTH)

		if not len(message_header):
			return False

		message_length = int(message_header.decode(ENC8).strip())
		return {'header': message_header, 'data': client_socket.recv(message_length)}

	except:
		return False

try:
	while True:
		read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
		# read sockets, write sockets, error sockets

		for notified_socket in read_sockets:
			# iterate through read sockets, every socket which is a part of the network

			if notified_socket == server_socket:
				# if the element is server socket

				client_socket, client_address = server_socket.accept()
				# accept incoming connection

				user = receive_message(client_socket)
				# receive message

				if user is False:
					continue

				sockets_list.append(client_socket)
				# add the user 

				clients[client_socket] = user

				print(f"\nCONNECT# {client_address[0]}:{client_address[1]}")
				print(f"Username : {user['data'].decode(ENC8)}")

			else:
				message = receive_message(notified_socket)

				if message is False:
					print(f"DISCONNET# {clients[notified_socket]['data'].decode(ENC8)}")
					sockets_list.remove(notified_socket)
					del clients[notified_socket]
					continue

				user = clients[notified_socket]

				user_msg = f"MSG# {user['data'].decode(ENC8)}: {message['data'].decode(ENC8)}"
				print(user_msg)

				for client_socket in clients:
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


		for notified_socket in exception_sockets:
			sockets_list.remove(notified_socket)
			del clients[notified_socket]

except KeyboardInterrupt as error:
	print('Server closed', str(error)










