import socket
import threading # Importa a biblioteca de threads
import sys
import time
import json

class Results:
    data = []  # Variável de classe

    @classmethod
    def add_result(cls, result):
        cls.data.append(result)

    @classmethod
    def get_results(cls):
        return cls.data

    @classmethod
    def save_results(cls, filename):
        with open(filename, 'w') as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def load_results(cls, filename):
        with open(filename, 'r') as f:
            cls.data = json.load(f)

class Server:
    # Configurações do servidor
    def __init__(self):
        self.HEADER = 256 # Quantidade limite de bytes para cada mensagem
        self.PORT = 5050 # Porta para conexão
        self.SERVER = socket.gethostbyname(socket.gethostname()) # Endereço IP do servidor local
        self.ADDR = (self.SERVER, self.PORT) # Tupla com o endereço e porta
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '!DESCONECTADO'
        self.client_counter = 0
        # Criação do socket TCP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associa o socket com o endereço e porta
        self.server.bind(self.ADDR)
        self.server.settimeout(5) # fechar após 5 segundos sem conexão
        self.results = Results()
        self.serverIsRunning = True

    # Inicia o servidor
    def start(self):
        self.server.listen()
        print(f'[AGUARDANDO] O servidor está aguardando conexão em {self.SERVER}')
        while self.serverIsRunning:
            try:
              conn, addr = self.server.accept()
              thread = threading.Thread(target=self.handle_client, args=(conn, addr))
              thread.start()
              print(f'[CONEXÕES ATIVAS] {threading.active_count() -1}')
              print(f'[CONEXÕES TOTAIS] {self.client_counter}')
            except socket.timeout:
               self.stop()
    
    def stop(self):
        self.serverIsRunning = False

    # Função para lidar com um cliente
    def handle_client(self, conn, addr):
      print(f'[NOVA CONEXÃO] {addr} conectado.')
      # Gere um intervalo numérico único para o cliente
      intervalo_inicio = self.client_counter * 1000
      intervalo_fim = intervalo_inicio + 999
      intervalo = f'[{intervalo_inicio}, {intervalo_fim}]'
      self.send(conn, intervalo)
      self.client_counter += 1
      connected = True
      while connected:
        received_msg = self.receive(conn)
        if received_msg.startswith('[R]'):
          # Recebeu uma mensagem de resultado
          received_msg = received_msg.replace('[R]', '')
          imp, par, pi = received_msg.split(',')
          print(f'[{addr}] Soma dos pares: {par}')
          print(f'[{addr}] Soma dos ímpares: {imp}')
          print(f'[{addr}] Valor de pi: {pi}')

          # Adiciona os resultados a uma lista
          self.results.add_result({
              # timestamp em DD/MM/YYYY HH:MM:SS
              'timestamp': time.strftime('%d/%m/%Y %H:%M:%S'),
              'cliente': self.client_counter,
              'soma_pares': par,
              'soma_impares': imp,
              'pi': pi
          })

          # Salva os resultados em um arquivo JSON
          self.results.save_results('results.json')

          print(f'[RESULTADOS] {self.results.get_results()}')
  
        if received_msg == self.DISCONNECT_MESSAGE:
          connected = False
          conn.send('msg recebida corretamente'.encode(self.FORMAT))
          print(f'[{addr}] {received_msg}')
      conn.close()


    # Funções send e receive para simplificar o envio e recebimento de mensagens
    def send(self, conn, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def receive(self, conn):
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self.FORMAT)
            print(f'[MENSAGEM RECEBIDA] {msg}')
            return msg
        return ""




if __name__ == '__main__':
  print('[INICIANDO] O servidor está iniciando...')
  s = Server()
  try:
      s.start()
  except KeyboardInterrupt:
      s.stop()
      print('[ENCERRANDO] O servidor foi encerrado.')
  
