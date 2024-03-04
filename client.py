import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.10.125', 12453))
    # Lógica para enviar/receber mensagens ao/do servidor


if __name__ == "__main__":
    main()
