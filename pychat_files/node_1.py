from socket import AF_INET, SOCK_STREAM
from threading import Thread
import socket


def handler_connection():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()





connected_nodes = {}
node_adresses = {}

IP = '127.0.0.1'
PORT = 6663
ENC8 = 'utf-8'
ADDR = (IP, PORT)
BUFF = 2048
USERNAME = 'NODE1'

node = socket.socket(AF_INET, SOCK_STREAM)
node.bind(ADDR)

if __name__ == "__main__":

	node.listen(10)
	print("Waiting for connection...")

