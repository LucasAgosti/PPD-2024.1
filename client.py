import socket
import tkinter as tk


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.10.125', 12453))

    # Espera por uma mensagem para iniciar ou esperar
    while True:
        message = client.recv(1024).decode()
        if message == "start":
            print("É a sua vez de jogar.")
            # Código para iniciar a jogada
            break
        elif message == "wait":
            print("Aguarde a sua vez.")
            # Código para aguardar
            break

def create_game_window():
    window = tk.Tk()
    window.title("Resta Um")
    # Configurações adicionais da janela
    window.mainloop()

if __name__ == "__main__":
    main()
    create_game_window()
