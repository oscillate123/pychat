from socket import AF_INET, SOCK_STREAM
from threading import Thread
import socket


def receive():
	""" Handels receiving """
	while True:
		try:
			msg = node_socket.recv(BUFF)
			print(msg.decode(ENC8))
		except OSError:
			break

def send():
	""" Handles sending """
	while True:
		msg = input(f"{USERNAME} > ")
		msg = f"{USERNAME} > {msg}"

		if msg == "!quit"
			node_socket.close()
			exit()
		else:
			node_socket.send(bytes(msg, ENC8))



connected_nodes = {}
node_adresses = {}

IP = '127.0.0.1'
PORT = 6663
ENC8 = 'utf-8'
ADDR = (IP, PORT)
BUFF = 2048
USERNAME = 'NODE2'

node_socket = socket.socket(AF_INET, SOCK_STREAM)
node_socket.connect(ADDR)


if __name__ == "__main__":

	receive_thread = Thread(target=receive)
	receive_thread.start()

	send_thread = Thread(target=send)
	send_thread.start()