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
        self.processos_atendidos = set()
        self.mensagens_log = []
        self.blocked = False
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor_socket.bind((self.host, self.porta))
        self.executando = True
        self.threads = []

    def iniciar_comunicacao(self):
        threads = [
            threading.Thread(target=self.receber_mensagens),
            threading.Thread(target=self.processar_pedidos),
            threading.Thread(target=self.interface_comando)
        ]
        for thread in threads:
            thread.start()
            self.threads.append(thread)

    def receber_mensagens(self):
        while self.executando:
            try:
                self.servidor_socket.settimeout(1)
                pedido, cliente = self.servidor_socket.recvfrom(1024)
                self.mensagens_log.append(pedido.decode('utf-8'))
                pedido = (pedido.decode('utf-8')).split('|')
                if pedido[0] == '1':
                    self.adicionar_fila((pedido[1], cliente))
                elif pedido[0] == '3':
                    self.blocked = False
                    print(f'Processo {pedido[1]} liberado.')
                else:
                    print(f'MENSAGEM INVALIDA: {pedido}')
                self.processos_atendidos.add(pedido[1])
            except socket.timeout:
                continue
            except OSError:
                break

    def adicionar_fila(self, processo):
        if processo not in list(self.pedidos.queue):
            self.pedidos.put(processo)
            print(f'Processo {processo[0]} adicionado a fila.')

    def numerar_atendimentos(self):
        for pr in self.processos_atendidos:
            processo = int(pr)
            request = grant = release = 0
            for m in self.mensagens_log:
                msg = m.split('|')
                if int(msg[1]) == processo:
                    if msg[0] == '1':
                        request += 1
                    if msg[0] == '2':
                        grant += 1
                    if msg[0] == '3':
                        release += 1
            print(f'Processo {processo}: REQUEST:{request}    GRANT:{grant}    RELEASE:{release}')

    def processar_pedidos(self):
        while self.executando:
            if not self.blocked and not self.pedidos.empty():
                id, cliente = self.pedidos.get()
                self.blocked = True
                mensagem = f"2|{id}|".ljust(10, '0')
                self.servidor_socket.sendto(mensagem.encode('utf-8'), cliente)
                self.mensagens_log.append(mensagem)

    def limpar_tela(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')

    def interface_comando(self):
        while self.executando:
            self.limpar_tela()
            comando = input("Digite um comando\n\n1: imprimir a fila de pedidos atual.\n2: imprimir quantas vezes cada processo foi atendido.\n3: encerrar a execução.\n\n")
            if comando == '1':
                self.limpar_tela()
                print("Fila de pedidos atual:", list(self.pedidos.queue))
                input("\nPressione Enter para continuar...")
            elif comando == '2':
                self.limpar_tela()
                print("Quantidade de vezes que cada processo foi atendido:")
                self.numerar_atendimentos()
                input("\nPressione Enter para continuar...")
            elif comando == '3':
                self.limpar_tela()
                print("Encerrando execução.")
                self.executando = False
                self.servidor_socket.close()
                break

        # Esperar as threads terminarem, exceto a thread atual (interface_comando)
        for thread in self.threads:
            if thread != threading.current_thread():
                thread.join()

coordenador = Coordenador('localhost', 8080)
coordenador.iniciar_comunicacao()
