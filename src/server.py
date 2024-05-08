import socket
import threading # Importa a biblioteca de threads
import time

# Configurações do servidor
HEADER = 64 # Quantidade limite de bytes para cada mensagem
PORT = 5050  # Porta para conexão
SERVER = socket.gethostbyname(socket.gethostname()) # Endereço IP do servidor local
# SERVER = '' # https://whatismyipaddress.com/
# print(SERVER)
ADDR = (SERVER, PORT) # Tupla com o endereço e porta
FORMAT = 'utf-8' 
DISCONNECT_MESSAGE = '!DESCONECTADO'

# Criação do socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket com o endereço e porta
server.bind(ADDR)

def handle_client(conn, addr):
  print(f'[NOVA CONEXÃO] {addr} conectado.')
  connected = True
  while connected:
    msg_length = conn.recv(HEADER).decode(FORMAT) # limitar mensagem ao tamanho máximo em Bytes
    if msg_length:
      msg_length = int(msg_length) # Obter tamanho da mensagem
      msg = conn.recv(msg_length).decode(FORMAT)
      if msg == DISCONNECT_MESSAGE:
        connected = False
      print(f'[{addr}] {msg}')
      conn.send('msg recebida corretamente'.encode(FORMAT))

  conn.close()

def start():
  # Habilita o servidor para aceitar conexões
  server.listen()
  print(f'[AGUARDANDO] O servidor está aguardando conexão em {SERVER}')
  while True:
    # Aceita a conexão de um cliente
    conn, addr = server.accept()
    # Ramifica em uma thread e envia conexão para função handle_client
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f'[CONEXÕES ATIVAS] {threading.active_count() -1}')


print('[INICIANDO] O servidor está iniciando...')
start()

# # Fechar os sockets
# client_socket.close()
# server_socket.close()