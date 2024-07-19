import threading
import socket

mensagens_tamanho = 10

class Coordenador:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor_socket.bind((self.host, self.porta))
        
    def iniciar_comunicacao(self):
        threading.Thread(target=self.receber_mensagens).start()
        threading.Thread(target=self.processar_pedidos).start()
        threading.Thread(target=self.interface_comando).start()

    def receber_mensagens(self):
        pass
    
    def processar_pedidos(self):
        pass 
    
    def interface_comando(self):
        while True:
            comando = input("Digite um comando\n\n1: imprimir a fila de pedidos atual.\n2: imprimir quantas vezes cada processo foi atendido.\n3: encerrar a execução.\n\n")
            if comando == '1':
                print("Fila de pedidos atual:", list(self.pedidos.queue))
            elif comando == '2':
                print("Quantidade de vezes que cada processo foi atendido:", self.processos_atendidos)
            elif comando == '3':
                print("Encerrando execução.")
                self.servidor_socket.close()
                break       

coordenador = Coordenador('localhost', 8080)
coordenador.iniciar_comunicacao()