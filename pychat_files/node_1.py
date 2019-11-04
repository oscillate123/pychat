from socket import AF_INET, SOCK_STREAM
from threading import Thread
import socket


def connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_addr = node_socket.accept()
        print(f"\n{client_addr} just connected\n")
        client.send(bytes(f"\n -{client_addr} connected to {ADDR}- \n", ENC8))
        node_addresses[client] = client_addr
        Thread(target=handle_client, args=(client,)).start()
        print()
        print(connected_clients)
        print(node_addresses)
        print()


def handle_client(client):
	""" Handles clients """
	name = client.recv(BUFF).decode(ENC8)
	welcome = f'Welcome! Type "!quit", to quit.'
	client.send(bytes(welcome, ENC8))
	msg = f'{name} connected'
	connected_clients[client] = name

	while True:
		msg = client.recv(BUFF).decode(ENC8)
		if msg is not "!quit":
			broadcast(msg, name+": ")
		else:
			client.send(bytes("Good bye", ENC8))
			client.close()
			del connected_clients[client]
			Thread(
				target=broadcast,
				args=(bytes(f"{name} disconnected", ENC8))
			)


def broadcast(msg):
	""" Broadcasts to all clients """
	for sock in connected_clients:
		sock.send(bytes(prefix, ENC8)+msg)


# -----------------------------------

connected_clients = {}
node_addresses = {}

IP = '127.0.0.1'
PORT = 6663
ENC8 = 'utf-8'
ADDR = (IP, PORT)
BUFF = 2048
USERNAME = 'NODE1'

node_socket = socket.socket(AF_INET, SOCK_STREAM)
node_socket.bind(ADDR)


if __name__ == "__main__":

	node_socket.listen(10)
	print("Waiting for connection...")

	connections_thread = Thread(target=connections)
	connections_thread.start()
	connections_thread.join()
	node_socket.close()
