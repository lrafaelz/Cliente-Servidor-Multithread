import socket

# Configurações do servidor
HEADER = 256
PORT = 5050 
FORMAT = 'utf-8' 
SHUTDOWN_MESSAGE = '!ENCERRAR'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

def send(msg, client):
  message = msg.encode(FORMAT)
  msg_length = len (message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length)) # representação de byte
  client.send(send_length)
  client.send(message)

def receive(client):
  msg_length = client.recv(HEADER).decode(FORMAT)
  if msg_length:
      msg_length = len(msg_length)
      msg = client.recv(msg_length).decode(FORMAT)
      return msg
  return ""

def stopServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    receive(client)
    print('Enviando mensagem de encerramento...')
    send(SHUTDOWN_MESSAGE, client)
  