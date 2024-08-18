import threading
import queue
import socket
import os
from datetime import datetime

def iniciar_terminal():
    global executando
    
    while executando:
        comando = input("\nDigite um comando\n\n1: imprimir a fila de pedidos atual.\n2: imprimir quantas vezes cada processo foi atendido.\n3: encerrar a execução.\n\n")
        os.system("clear") if os.name == "posix" else os.system("cls")

        match comando:
            case "1":
                lista_pedidos = list(fila_pedidos.queue)
                if len(lista_pedidos) == 0:
                    print("Fila vazia")
                else:
                    print("Fila de pedidos atual:")
                    for id_processo, _ in lista_pedidos:
                        print(f"Processo {id_processo}")
            case "2":
                if not processos_atendidos:
                    print("Nenhum processo atendido até o momento")
                else:
                    print("Quantidade de vezes que cada processo foi atendido:")
                    for id_processo, qtd_atendimentos in processos_atendidos.items():
                        print(f"Processo {id_processo}: {qtd_atendimentos}")  
            case "3":
                print("Encerrando execução...")
                executando = False
            case _:
                print("Opção inválida")
        
        print("_________________________________________________________")

def receber_mensagens():
    global recebido_release

    while executando:
        try:
            socket_coordenador.settimeout(1)
            mensagem, processo = socket_coordenador.recvfrom(10)
            [tipo_mensagem, id_processo, _] = mensagem.decode().split("|")
            match tipo_mensagem:
                case "1":
                    with lock_log:
                        with open("log.txt", "a") as log:
                            log.write(f"{datetime.now()} -- REQUEST -- Processo {id_processo}\n")
                    fila_pedidos.put((id_processo, processo))
                case "3":
                    if id_processo in processos_atendidos:
                        processos_atendidos[id_processo] += 1
                    else:
                        processos_atendidos[id_processo] = 1
                    with lock_log:
                        with open("log.txt", "a") as log:
                            log.write(f"{datetime.now()} -- RELEASE -- Processo {id_processo}\n")
                    recebido_release = True
                case _:
                    print(f"Mensagem inválida: {mensagem}")
        except socket.timeout:
            continue
        except OSError:
            break

def garantir_exclusao_mutua():
    global recebido_release
    lock_resultado = threading.Lock()

    while executando:
        if not fila_pedidos.empty():
            with lock_resultado:
                id_processo, processo = fila_pedidos.get()
                mensagem = f"2|{id_processo}|".ljust(10, "0")
                socket_coordenador.sendto(mensagem.encode(), processo)
                recebido_release = False
                with lock_log:
                    with open("log.txt", "a") as log:
                        log.write(f"{datetime.now()} -- GRANT   -- Processo {id_processo}\n")
                while not recebido_release:
                    continue

if __name__ == "__main__":
    fila_pedidos = queue.Queue()
    processos_atendidos = {}
    socket_coordenador = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    lock_log = threading.Lock()
    executando = True
    recebido_release = False

    for arquivo in ["log.txt", "resultado.txt"]:
        os.remove(arquivo) if os.path.isfile(arquivo) else None

    with socket_coordenador:
        socket_coordenador.bind(("localhost", 8080))

        threads = [
            threading.Thread(target=iniciar_terminal),
            threading.Thread(target=receber_mensagens),
            threading.Thread(target=garantir_exclusao_mutua)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()