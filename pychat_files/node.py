from socket import socket, AF_INET, SOCK_STREAM
import threading


connected_nodes = {}
IP = gethostname()
PORT = 6663
ENC8 = 'utf-8'

node_socket = socket(AF_INET, SOCK_STREAM)
node_socket.bind((IP, PORT))
node_socket.listen(10)


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(BUFSIZE)

        if not len(message_header):
            return False

        message_length = int(message_header.decode(ENC8).strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        pass


def unique_client_generator(client):
	""" Generate a unique client ID so we won't get clashing clientnames """
	unique_client = str(random_client_int()) + client
	return unique_client


def broadcast(prefix="", msg):
	""" Broadcast message to all clients, e.g. someone has connected """
	for node in connected_nodes:
		s_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		payload_addr = connected_nodes[node]
		s_temp.bind((payload_addr))
		payload = prefix + msg
		s_temp.send(payload.encode(ENC8))
		s_temp.close()


main_flag = True

while main_flag:
	""" Handle connections """
	client_socket, client_address = node_socket.accept()
	connected_nodes[client_socket] = client_address
	broadcast(prefix='Connection from: ', msg=client_address)
