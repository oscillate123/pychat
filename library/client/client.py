import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 6662
UTF8 = 'utf-8'

print(f'Connecting to: {IP}:{PORT}')
my_username = input('Username: ')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode(UTF8)
username_header = f"{len(username) :< {HEADER_LENGTH}}".encode(UTF8)

client_socket.send(username_header + username)

flag = True

while flag:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode(UTF8)
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode(UTF8)
        client_socket.send(message_header + message)

    flag2 = True

    try:
        while flag2:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode(UTF8).strip())
            username = client_socket.recv(username_length).decode(UTF8)

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode(UTF8).strip())
            message = client_socket.recv(message_length).decode(UTF8)

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno is not errno.EAGAIN and e.errno is not errno.EWOULDBLOCK:
            print(f"Reading error: {str(e)}")
            sys.exit()

    except Exception as e:
        print(f"General error: {str(e)}")

