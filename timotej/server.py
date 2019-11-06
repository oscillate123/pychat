import socket
import select

HEADER_LENGTH = 10
#IP = "172.20.200.195"
IP = "192.168.1.57"
PORT = 55222

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

socket_list = [server_socket]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

# def send_message(message):
#     for client_socket in clients:
#         if client_socket != notified_socket:
#             client_socket.send(f"\n---{user['data'].decode('utf-8')} has entered the building\n".encode('utf-8'))


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user

            print(f"\n--- {user['data'].decode('utf-8')} has entered the chat ---\n")

        else:
            message = receive_message(notified_socket)
            if message is False:
                #user_logged_off = f"\n--- {clients[notified_socket]['data'].decode('utf-8')} left the chat ---\n"
                print(f"\n--- {clients[notified_socket]['data'].decode('utf-8')} left the chat ---\n")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"{user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
