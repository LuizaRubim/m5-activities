from flask import Flask, render_template, request
from datetime import datetime
from tinydb import TinyDB, Query
from pydobot import Dobot
from serial.tools import list_ports
from dobot import DobotMoves
# Cria a instância do Flask no App
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
# Banco em memória
banco = TinyDB('logs.json')

robo=DobotMoves()
# Rota de teste
@app.route('/')
def ola():
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "acessou a pagina inicial",
    })
    return render_template('index.html')

# rota para connectar com o robô
@app.route('/conectar')
def connect():
    print(list_ports.comports())
    port = list_ports.comports()[0].device
    robo.conectar(port)
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "acao": "conectar robô",
    "hora":str(datetime.now()),
    })
    
    return 'Conectado com sucesso'

# Rota para desconectar
@app.route('/desconectar')
def disconnect():
    robo.desconectar()
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "acao": "desconectar robô",
    "hora":str(datetime.now()),
    })
    return 'Desconectado com sucesso'

# Rota para mover para a posição inicial
@app.route('/home')
def home():
    robo.home()
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "posicao_home",
    "posicao_atual": str(robo.device.pose())
    })
    return ("", 204)

@app.route("/posicao_atual")
def posicao_atual():
    posicao_atual = robo.device.pose()
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "posicao_atual",
    "posicao_atual": robo.device.pose()
    })
    return f'Posicao atual:{posicao_atual}'

@app.route('/mover_distancia', methods=['POST'])
def mover_distancia():
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']
    r = request.form['r']
    robo.mover_distancia(x, y, z, r)
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "mover_distancia",
    "posicao_atual": str(robo.device.pose()),
    'x': x,
    'y': y,
    'z': z,
    'r': r
    })
    return 'Movido com sucesso'

@app.route('/mover_para_ponto', methods=['POST'])
def mover_para_ponto():
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']
    r = request.form['r']
    robo.mover_para_ponto(x, y, z, r)
    banco.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "mover para ponto",
    "posicao_atual": str(robo.device.pose()),
    })
    return 'Movido com sucesso'

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/atualiza-logs')
def retorna_acessos():
    return render_template('item-log.html', itens=banco)

@app.route('/conexao')
def conexao():
    return render_template('connect-button.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)