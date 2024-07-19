import socket

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
        pass
    
    def liberar_acesso(self):
        pass
    
        
    