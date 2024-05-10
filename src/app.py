from flask import Flask, url_for, render_template, request
from server import Results, Server
import subprocess
import platform
import os

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
  if request.method == 'POST' and request.form['submit_button'] == 'Iniciar servidor':
    server = Server()
  return render_template('server.html', titulo=titulo, results=results, serverIsRunning=serverIsRunning)

@app.route('/clients', methods=['GET', 'POST'])
def client():
  titulo = 'Cliente 🛠'
  print(createdClients)
  return render_template('clients.html', titulo=titulo, createdClients=createdClients)

@app.route('/create_client')
def create_client():
    global createdClients
    createdClients += 1
    current_directory = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(current_directory, 'client.py')
    os_name = platform.system().lower()

    if os_name == 'windows':
        command = ['cmd', '/K', 'python', script_path]
    elif os_name == 'darwin':
        command = ['open', '-a', 'Terminal.app', '-n', '-t', 'python', script_path]
    else:
        command = ['gnome-terminal', '--', 'python', script_path]

    # Abrir um novo terminal e rodar o script client.py
    subprocess.Popen(command, shell=True)
    print(createdClients)
    return render_template('clients.html', createdClients=createdClients)


@app.route('/start_server')
def start_server():
    # Obter localização da pasta atual
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Construir o caminho completo para o script server.py
    script_path = os.path.join(current_directory, 'server.py')
    
    # Identificar o sistema operacional
    os_name = platform.system().lower()
    
    # Comando para abrir um novo terminal e rodar o script server.py
    if os_name == 'windows':
        command = ['cmd', '/K', 'python', script_path]
    elif os_name == 'darwin':  # macOS
        command = ['open', '-a', 'Terminal.app', '-n', '-t', 'python', script_path]
    else:  # Linux
        command = ['gnome-terminal', '--', 'python', script_path]
    
    # Abrir um novo terminal e rodar o script server.py
    subprocess.Popen(command, shell=True)
    global serverIsRunning
    serverIsRunning = True
    return render_template('serverRunning.html', serverIsRunning=serverIsRunning)

@app.route('/stop_server')
def stop_server():
    global serverIsRunning, createdClients
    # kill all terminals
    os_name = platform.system().lower()
    if os_name == 'windows':
        os.system("taskkill /f /im cmd.exe")
    elif os_name == 'darwin':
        os.system("killall Terminal")
    else:
        os.system("killall gnome-terminal")
    serverIsRunning = False
    createdClients = 0
    return render_template('server.html', serverIsRunning=serverIsRunning)
       


if __name__ == '__main__':
    app.run(debug=True)
