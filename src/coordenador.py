import threading
import socket
import queue
import os

mensagens_tamanho = 10

class Coordenador:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.pedidos = queue.Queue()
        self.processos_atendidos = {}
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
    
    def limpar_tela(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
    
    def interface_comando(self):
        while True:
            self.limpar_tela()
            comando = input("Digite um comando\n\n1: imprimir a fila de pedidos atual.\n2: imprimir quantas vezes cada processo foi atendido.\n3: encerrar a execução.\n\n")
            if comando == '1':
                self.limpar_tela()
                print("Fila de pedidos atual:", list(self.pedidos.queue))
                input("Pressione Enter para continuar...")
            elif comando == '2':
                self.limpar_tela()
                print("Quantidade de vezes que cada processo foi atendido:", self.processos_atendidos)
                input("Pressione Enter para continuar...")
            elif comando == '3':
                self.limpar_tela()
                print("Encerrando execução.")
                self.servidor_socket.close()
                break       

coordenador = Coordenador('localhost', 8080)
coordenador.iniciar_comunicacao()