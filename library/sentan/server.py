import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 6662
UTF8 = 'utf-8'

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        pass


flag = True

while flag:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"\nNew connection {client_address[0]}:{client_address[1]} username: "
                  f"{user['data'].decode(UTF8)}\n")
        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"\n ## {clients[notified_socket]['data'].decode(UTF8)} disconnected ## \n")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f" # {user['data'].decode(UTF8)}: {message['data'].decode(UTF8)}")

            for client_socket in clients:
                if client_socket is not notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
