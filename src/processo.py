import socket
import threading
from datetime import datetime
import time

class Processo:
    def __init__(self, host, porta, id_processo, repeticoes, intervalo):
        self.host = host
        self.porta = porta
        self.id_processo = id_processo
        self.repeticoes = repeticoes
        self.intervalo = intervalo
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def iniciar(self):
        for _ in range(self.repeticoes):
            self.solicitar_acesso()
            self.regiao_critica()
            self.liberar_acesso()
            
    def solicitar_acesso(self):
        mensagem = f"1|{self.id_processo}|".ljust(10, '0')
        self.cliente_socket.sendto(mensagem.encode(), (self.host, self.porta))
        print(f"Processo {self.id_processo} enviou REQUEST para o coordenador")
    
    def regiao_critica(self):
        while True:
            mensagem = (self.cliente_socket.recv(1024).decode('utf-8')).split('|')
            if mensagem[0] == '2':
                print(f"Coordenador enviou GRANT para o Processo {self.id_processo}")
                tempo_atual = (datetime.now()).strftime("%H:%M:%S.%f")

                with open('resultado.txt','a') as arquivo:
                    arquivo.write(f"Processo {self.id_processo} --- {tempo_atual}\n")

                time.sleep(self.intervalo)
                break
    
    def liberar_acesso(self):
        mensagem = f"3|{self.id_processo}|".ljust(10, '0')
        self.cliente_socket.sendto(mensagem.encode(), (self.host, self.porta))
        print(f"Processo {self.id_processo} enviou RELEASE para o coordenador")

def iniciar_processo(id):
    p = Processo('localhost', 8080, id, 10, 5)
    p.iniciar()

threads = []
for f in range(5):
    t = threading.Thread(target=iniciar_processo, args=([f]))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
    
        
    