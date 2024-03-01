# robo.py

# Traz a ferramenta serial para apresentar quais portas estão disponíveis
from serial.tools import list_ports
import inquirer
import pydobot
from yaspin import yaspin


class InteliArm(pydobot.Dobot):
    def __init__(self, port=None, verbose=False):
        super().__init__(port=port, verbose=verbose)
    
    def movej_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVJ_XYZ, wait=wait)

    def movel_to(self, x, y, z, r, wait=True):
        super()._set_ptp_cmd(x, y, z, r, mode=pydobot.enums.PTPMode.MOVL_XYZ, wait=wait)
    
    def home(self):
        self.movej_to(240, 0, 150, 0, wait=True)

# Traz o spinner para apresentar uma animação enquanto o robô está se movendo
spinner = yaspin(text="Processando...", color="yellow")

# Listas as portas seriais disponíveis
available_ports = list_ports.comports()


# Pede para o usuário escolher uma das portas disponíveis
porta_escolhida = inquirer.prompt([
    inquirer.List("porta", message="Escolha a porta serial", choices=[x.device for x in available_ports])
])["porta"]

# Cria uma instância do robô
robo = InteliArm(port=porta_escolhida, verbose=False)



choices = [
    inquirer.List("opcao", message="Seja bem vindo, escolha uma das funções abaixo", choices=["Mover para posição inicial", "Mover para um ponto", "Mover distância", "Ligar ventosa", "Desligar ventosa", "Posição atual", "Sair"])]

robo.home()

while True:
    menu = inquirer.prompt(choices)["opcao"]

    match menu:
        case "Mover para posição inicial":
            loading = yaspin(text="Movendo para a posição inicial...", color="green")
            loading.start()
            robo.home()
            loading.stop()
        case "Mover para um ponto":
            x = float(input("Digite a posição X: "))
            y = float(input("Digite a posição Y: "))
            z = float(input("Digite a posição Z: "))
            spinner.start()
            robo.move_to(x, y, z, 0)
            spinner.stop()
        case "Mover distância":
            x = float(input("Digite a distância em X: "))
            y = float(input("Digite a distância em Y: "))
            z = float(input("Digite a distância em Z: "))
            spinner.start()
            posicao = robo.pose()
            x += posicao[0]
            y += posicao[1]
            z += posicao[2]
            robo.movej_to(x, y, z, 0)
            spinner.stop()
        case "Ligar ventosa":
            spinner.start()
            robo.suck(True)
            spinner.stop()
        case "Desligar ventosa":
            spinner.start()
            robo.suck(False)
            spinner.stop()
        case "Posição atual":
            posicao_atual = robo.pose()
            print(f"A posição atual é: {posicao_atual}")
        case "Sair":
            print("Programa finalizado!")
            robo.suck(False)
            robo.close()
            break