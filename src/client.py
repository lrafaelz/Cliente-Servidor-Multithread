import socket


# Configurações do servidor
HEADER = 64
PORT = 5050 
FORMAT = 'utf-8' 
DISCONNECT_MESSAGE = '!DESCONECTADO'
SERVER = '192.168.240.198'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
  message = msg.encode(FORMAT)
  msg_length = len (message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length)) # representação de byte
  client.send(send_length)
  client.send(message)
  print(client.recv(2048).decode(FORMAT))

send('Hello world!')
input()
send('teste')
input()
send('bye')

send(DISCONNECT_MESSAGE)