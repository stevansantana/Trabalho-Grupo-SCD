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
        pass       
    