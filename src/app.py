from flask import Flask, url_for, render_template, request
from server import Results, Server
import subprocess
import time
from client import start
from stop_server import stopServer

app = Flask(__name__)

serverIsRunning = False
createdClients = 0
results = 0

# Rotas
@app.route('/', methods=['GET', 'POST'])
def server(refresh = True):
  global results
  titulo = 'Client-Servidor com threads 🔬🧪'
  if refresh:
    Results.load_results('results.json')
    results = Results.get_results()
    Results.load_results('finalResult.json')
    finalResult = Results.get_results()
  else:
      Results.clear_results()
      results = Results.get_results()
      Results.load_results('finalResult.json')
      finalResult = Results.get_results()
  return render_template('server.html', titulo=titulo, results=results, serverIsRunning=serverIsRunning, createdClients=createdClients, finalResult=finalResult)

@app.route('/create_client')
def create_client():
    global createdClients
    global serverIsRunning
    try:
      # Abrir um novo client
      start()
      # Fazer verificação de quando o ciente não conseguir se conectar ao servidor
      createdClients += 1
      print(createdClients)
      time.sleep(0.4)
    except Exception as e:
      print(f"Ocorreu um erro: {e}")
      if e == "ConnectionRefusedError":
        serverIsRunning = False
    return server(refresh=True)


@app.route('/start_server')
def start_server():
    global serverIsRunning
    if serverIsRunning == False:
        subprocess.Popen(['python', 'src/server.py'])
        serverIsRunning = True
        return server(refresh=False)
    return url_for('server')

@app.route('/stop_server')
def stop_server():
    global serverIsRunning, createdClients
    serverIsRunning = False
    createdClients = 0
    # fechar o servidor
    try:
      stopServer()
    except Exception as e:
      print(f"Ocorreu um erro: {e}")
    return server(refresh=True)


# se o arquivo finalResult.json for modificado, acessar rota que exibirá modal contendo o resultado final
@app.route('/final_result')
def final_result():
    global results, serverIsRunning, createdClients
    
    return render_template('server.html', results=results, serverIsRunning=serverIsRunning, createdClients=createdClients, finalResult=finalResult, finalResultModal=True)


if __name__ == '__main__':
    app.run(debug=True)
