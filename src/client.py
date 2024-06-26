import socket

# Configurações do servidor
HEADER = 256
PORT = 5050 
FORMAT = 'utf-8' 
DISCONNECT_MESSAGE = '!DESCONECTADO'
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

# Calculos

def soma_pares(inicio, fim):
    soma = 0
    for num in range(inicio, fim + 1):
        if num % 2 == 0: # Verifica se o número é par
            soma += num
    return soma

def soma_impares(inicio, fim):
    soma = 0
    for num in range(inicio, fim + 1):
        if num % 2 != 0: # Verifica se o número é ímpar
            soma += num
    return soma

def pi(a, b):
    pi = 0
    for n in range(a, b + 1):
        pi += 4 * ((-1) ** n) / (2 * n + 1)
    return pi
############################################

def start():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    intervalo = receive(client)

    print(f'Intervalo recebido: {intervalo}') 

    inicio = int(intervalo.split(',')[0][1:])
    fim = int(intervalo.split(',')[1][:-1])

    soma_pares_intervalo = soma_pares(inicio, fim)
    soma_impares_intervalo = soma_impares(inicio, fim)
    valor_pi = pi(inicio, fim)

    print(f"Soma dos números pares no intervalo [{inicio}, {fim}]: {soma_pares_intervalo}")
    print(f"Soma dos números ímpares no intervalo [{inicio}, {fim}]: {soma_impares_intervalo}")
    try:
        # Enviar os resultados para o servidor SOMA PARES, SOMA IMPARES, PI
        send('[R]' + str(soma_pares_intervalo) + ',' + str(soma_impares_intervalo) + ',' + str(valor_pi), client)
    except ConnectionAbortedError:
        print("A conexão foi abortada. Verifique o servidor e a rede.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


    send(DISCONNECT_MESSAGE, client)

if __name__ == '__main__':
  start()
