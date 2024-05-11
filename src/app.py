from flask import Flask, url_for, render_template, request
from server import Results, Server
import subprocess
from client import start

app = Flask(__name__)

serverIsRunning = False
createdClients = 0

# Rotas
@app.route('/')
def index():
  titulo = 'Client-Servidor com threads 🔬🧪'

  return render_template('index.html', titulo=titulo)

@app.route('/server', methods=['GET', 'POST'])
def server():
  titulo = 'Servidor 🛜'
  Results.load_results('results.json')
  results = Results.get_results()
  print(results)
  if serverIsRunning == False:
      return render_template('server.html', titulo=titulo, results=results, serverIsRunning=serverIsRunning)
  else:
      return render_template('serverRunning.html', serverIsRunning=serverIsRunning)

@app.route('/clients', methods=['GET', 'POST'])
def client():
  titulo = 'Cliente 🛠'
  print(createdClients)
  return render_template('clients.html', titulo=titulo, createdClients=createdClients)

@app.route('/create_client')
def create_client():
    global createdClients
    # Abrir um novo client
    start()
    # Fazer verificação de quando o ciente não conseguir se conectar ao servidor
    createdClients += 1
    print(createdClients)
    return render_template('clients.html', createdClients=createdClients)


@app.route('/start_server')
def start_server():
    global serverIsRunning
    if serverIsRunning == False:
        subprocess.Popen(['python', 'src/server.py'])
        serverIsRunning = True
    return render_template('serverRunning.html', serverIsRunning=serverIsRunning)

@app.route('/stop_server')
def stop_server():
    global serverIsRunning, createdClients
    serverIsRunning = False
    createdClients = 0
    return render_template('server.html', serverIsRunning=serverIsRunning)
       


if __name__ == '__main__':
    app.run(debug=True)
