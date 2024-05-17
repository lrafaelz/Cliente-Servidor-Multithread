import socket
import threading
import sys
import time
import json

class Results:
    data = []
    finalResult = {}

    @classmethod
    def add_result(cls, result):
        cls.data.append(result)

    @classmethod
    def get_results(cls):
        return cls.data

    @classmethod
    def save_results(cls, file):
        json.dump(cls.data, file, indent=4)

    @classmethod
    def load_results(cls, filename):
        with open(filename, 'r') as f:
            cls.data = json.load(f)

    @classmethod
    def clear_results(cls):
        cls.data = []
        json.dump(cls.data, open('results.json', 'w'), indent=4)

    @classmethod
    def save_final_result(cls, finalResult, file):
        cls.finalResult = finalResult
        json.dump(cls.finalResult, file, indent=4)


class Server:
    # Configurações do servidor
    def set(self):
        self.HEADER = 256 # Quantidade limite de bytes para cada mensagem
        self.PORT = 5050 # Porta para conexão
        self.SERVER = socket.gethostbyname(socket.gethostname()) # Endereço IP do servidor local
        self.ADDR = (self.SERVER, self.PORT) # Tupla com o endereço e porta
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '!DESCONECTADO'
        self.SHUTDOWN_MESSAGE = '!ENCERRAR'
        self.client_counter = 0
        # Criação do socket TCP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associa o socket com o endereço e porta
        self.server.bind(self.ADDR)
        self.server.settimeout(15) # fechar após 15 segundos sem conexão
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
               print('[ENCERRANDO] O servidor foi encerrado por inatividade')
               self.final_result()
               self.stop()
    
    def stop(self):
        print('[ENCERRANDO] O servidor está encerrando...')
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

          # Salva os resultados em um arquivo JSON na pasta raiz (Cliente-Servidor-Multithread/results.json)
          file = open('results.json', 'w')
          self.results.save_results(file)
          file.close()

          print(f'[RESULTADOS] {self.results.get_results()}')
  
        if received_msg == self.DISCONNECT_MESSAGE:
          connected = False
          conn.send('msg recebida corretamente'.encode(self.FORMAT))
          print(f'[{addr}] {received_msg}')
        
        if received_msg == self.SHUTDOWN_MESSAGE:
            connected = False
            conn.send('msg recebida corretamente'.encode(self.FORMAT))
            print(f'[{addr}] {received_msg}')
            self.stop()
           
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

    # Gerar resultado final a partir do resultado calculado em cada cliente
    def final_result(self):
        # obter e realizar operações com os resultados de cada cliente
        results = self.results.get_results()
        self.results.finalResult = {
            'soma_pares': 0,
            'soma_impares': 0,
            'pi': 0
        }
        for result in results:
            self.results.finalResult['soma_pares'] += int(result['soma_pares'])
            self.results.finalResult['soma_impares'] += int(result['soma_impares'])
            self.results.finalResult['pi'] += float(result['pi'])
        # salvar resultado final
        print('[RESULTADO FINAL] ', self.results.finalResult)
        self.results.save_final_result(self.results.finalResult, open('finalResult.json', 'w'))



if __name__ == '__main__':
  print('[INICIANDO] O servidor está iniciando...')
  s = Server()
  try:
      s.set()
      s.start()
  except KeyboardInterrupt:
      s.stop()  
