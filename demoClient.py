import socket

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345  # Porta para conexão

# Criação do socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
client_socket.connect((HOST, PORT))

print("Conectado ao servidor")

# Enviar uma string teste
client_socket.sendall(b"Hello, World!")


# Fechar o socket
client_socket.close()