import socket

HOST = '127.0.0.1'
PORT = 4444
ENC8 = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

flag = True

while flag:
    payload = input("")

    s.send(payload.encode(ENC8))
