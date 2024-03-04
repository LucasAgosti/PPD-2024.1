import socket
import threading
import random

clientes = []

def handle_client(conn, addr):
    print(f"Nova conexão de {addr}")
    # Aqui pode ser implementada a lógica de comunicação durante o jogo
    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.10.125', 12453))
    server.listen()
    print("Servidor aguardando conexões...")

    while len(clientes) < 2:
        conn, addr = server.accept()
        clientes.append(conn)
        if len(clientes) == 2:
            # Notifica os clientes que o jogo pode começar
            for client in clientes:
                client.send("O jogo vai começar".encode())
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Conexão de {addr} aceita. Aguardando mais {2 - len(clientes)} jogadores.")

if __name__ == "__main__":
    main()
