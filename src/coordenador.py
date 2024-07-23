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
        self.blocked = False
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor_socket.bind((self.host, self.porta))
        
    def iniciar_comunicacao(self):
        threading.Thread(target=self.receber_mensagens).start()
        threading.Thread(target=self.processar_pedidos).start()
        threading.Thread(target=self.interface_comando).start()

    def receber_mensagens(self):
        while True:
            pedido, cliente = self.servidor_socket.recvfrom(1024)
            pedido = (pedido.decode('utf-8')).split('|')

            if pedido[0] == '1':
                self.adicionar_fila((pedido[1],cliente))            
            elif pedido[0] == '3':
                self.blocked = False
                print(f'Processo {pedido[1]} liberado.')
            else:
                print(f'MENSAGEM INVALIDA: {pedido}')

    def adicionar_fila(self,processo):
        if processo not in list(self.pedidos.queue):
            self.pedidos.put(processo)
            print(f'Processo {processo[0]} adicionado a fila.')
    
    def processar_pedidos(self):
        while True:
            if not self.blocked:
                id, cliente= self.pedidos.get()
                self.blocked = True
                mensagem = f"2|{id}|".ljust(10, '0')
                self.servidor_socket.sendto(mensagem.encode('utf-8'), (cliente))
    
    def limpar_tela(self):
        # Para Unix/Linux/Mac
        if os.name == 'posix':
            os.system('clear')
        # Para Windows
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