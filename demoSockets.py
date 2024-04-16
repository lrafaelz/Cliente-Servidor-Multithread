import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta para conexão

# Criação do socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket com o endereço e porta
server_socket.bind((HOST, PORT))

# Habilita o servidor para aceitar conexões
server_socket.listen()

print(f"Servidor TCP esperando por conexões em {HOST}:{PORT}")

# Aceita a conexão de um cliente
client_socket, client_address = server_socket.accept()

print(f"Conexão estabelecida com {client_address}")

# Aqui você pode continuar a lógica do servidor para receber e enviar dados
data = client_socket.recv(302)
# printar string recebida pelo cliente
print(f"Recebido: {data.decode()}")

# Fechar os sockets
client_socket.close()
server_socket.close()