import socket
import threading
import sys
from datetime import datetime
from random import randint
from time import sleep

def iniciar_processo():
    socket_processo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    execucoes = 0

    with socket_processo:
        while execucoes < REPETICOES:
            mensagem_request = f"1|{threading.current_thread().name}|".ljust(10, "0")
            socket_processo.sendto(mensagem_request.encode(), ("localhost", 8080))

            mensagem_coordenador, _ = socket_processo.recvfrom(10)
            tipo_mensagem = mensagem_coordenador.decode().split("|")[0]

            if tipo_mensagem == "2":
                with open("resultado.txt", "a") as resultado:
                    resultado.write(f"{datetime.now()} -- Processo {threading.current_thread().name}\n")
                    sleep(randint(1, 4))
                mensagem_release = f"3|{threading.current_thread().name}|".ljust(10, "0")
                socket_processo.sendto(mensagem_release.encode(), ("localhost", 8080))
                execucoes += 1
            
            sleep(randint(1, 4))
            

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Erro nos argumentos, utilizar <Num de Processos> <Repeticoes>")
        sys.exit(1)

    NUM_PROCESSOS = int(sys.argv[1])
    REPETICOES = int(sys.argv[2])
    processos = []

    for id_processo in range(NUM_PROCESSOS):
        processo = threading.Thread(target=iniciar_processo, name=str(id_processo + 1))
        processos.append(processo)
        processo.start()

    for processo in processos:
        processo.join()