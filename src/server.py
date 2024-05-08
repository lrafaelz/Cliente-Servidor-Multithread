import socket
import threading # Importa a biblioteca de threads
import time

# Configurações do servidor
HEADER = 128 # Quantidade limite de bytes para cada mensagem
PORT = 5050  # Porta para conexão
SERVER = socket.gethostbyname(socket.gethostname()) # Endereço IP do servidor local
# SERVER = '' # https://whatismyipaddress.com/
# print(SERVER)
ADDR = (SERVER, PORT) # Tupla com o endereço e porta
FORMAT = 'utf-8' 
DISCONNECT_MESSAGE = '!DESCONECTADO'

client_counter = 0

# Criação do socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket com o endereço e porta
server.bind(ADDR)

def handle_client(conn, addr):
  global client_counter
  print(f'[NOVA CONEXÃO] {addr} conectado.')
  # Gere um intervalo numérico único para o cliente
  intervalo_inicio = client_counter * 1000
  intervalo_fim = intervalo_inicio + 99
  intervalo = f'[{intervalo_inicio}, {intervalo_fim}]'
  send(conn, intervalo)
  client_counter += 1
  connected = True
  while connected:
    received_msg = receive(conn)
    if received_msg == DISCONNECT_MESSAGE:
      connected = False
      print(f'[{addr}] {received_msg}')
      conn.send('msg recebida corretamente'.encode(FORMAT))
  conn.close()

# Funções send e receive para simplificar o envio e recebimento de mensagens
def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f'[MENSAGEM RECEBIDA] {msg}')
        return msg
    return ""

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