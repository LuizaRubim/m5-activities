from pydobot import Dobot
import time

class DobotMoves():
    def __init__(self):
        pass
    
    def conectar(self,port):
        self.device = Dobot(port=port, verbose=False)

    def home(self):
        self.mover_para_ponto(240, 0, 150, 0)
        time.sleep(1)

    def mover_para_ponto(self, x, y, z, r):
        self.device.move_to(x, y, z, r)
        time.sleep(1)

    def mover_distancia(self, x, y, z, r):
        posicao = self.device.pose()
        print(posicao)
        self.device.move_to(posicao[0]+ float(x), posicao[1]+ float(y), posicao[2] + float(z), posicao[3]+ float(r))
        time.sleep(1)

    def desconectar(self):
        self.device.close()