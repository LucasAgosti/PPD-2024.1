import socket
import threading


def handle_client(conn, addr):
    print(f"Nova conexão de {addr}")
    # Lógica para lidar com comunicação do cliente


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.10.125', 12453))
    server.listen()
    print("Servidor aguardando conexões...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Ativas conexões: {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
