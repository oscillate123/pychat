from socket import AF_INET, SOCK_STREAM
from threading import Thread
import socket


connected_nodes = {}
node_adresses = {}
IP = '127.0.0.1'
PORT = 6663
ENC8 = 'utf-8'

node_socket = socket.socket(AF_INET, SOCK_STREAM)
node_socket.bind((IP, PORT))
node_socket.listen(10)

