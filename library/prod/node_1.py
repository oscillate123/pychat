import socket
import select

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def random_client_int():
    ran = random.randint(1, 1000)
    if ran not in busy_nums:
        busy_nums.append(ran)
        return ran
    else:
        random_client_int()


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


def old_version():
	while flag:
	    s.listen(5)
	    (client, (ip, port)) = s.accept()
	    print(ip, port)
	    client_data = client.recv(2048)
	    print(client_data.decode(ENC8))
	    print('')

	    if client_data:
	        s.listen(5)
	    continue


def handler_connection():
	"""
	1. Listen for incomming connections
	2. Store unique client id
	3. Return unique client id to client
	"""
	flag = True

	while flag:
		client, c_address = s.accept()
		clients[unique_client_generator(client)] = c_address
		broadcast(prefix=f'New connection: {client}')
		msg = f"Store your unique id {unique_client} for this session"
		client.send(bytes(msg))


def broadcast(msg, prefix=""):
	""" Broadcast message to all clients, e.g. someone has connected """
	for client in clients:
		s_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		payload_addr = clients[client]
		s_temp.bind((payload_addr))
		payload = prefix + msg
		s_temp.send(payload.encode(ENC8))
		s_temp.close()




if __name__ == "__main__":

	username = input("Username: ")
	username_ip = get_ip()
	print(f'Username: {username} ### IP: {username_ip}')
	host_input = input(f'Connect to host: ')

	HOST = f'{host_input}'
	PORT = 6662
	ENC8 = 'utf-8'
	BUFSIZE = 2048
	ADDR = (HOST, PORT)

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(5)

	sockets_list = [s]
	clients = {}
	s.listen(5)
	handler_connection()

	flag = True
	while flag:
		""" seperate approved sockets from other sockets """
		green_sockets, smh, red_sockets = select.select(sockets_list, [], sockets_list)	

