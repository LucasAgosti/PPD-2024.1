import socket
import tkinter as tk

class RestaUmGUI:
    def __init__(self, master, client_socket):
        self.master = master
        self.client_socket = client_socket
        master.title("Resta Um")

        self.board = [[None for _ in range(7)] for _ in range(7)]
        self.create_board()

    def create_board(self):
        for i in range(7):
            for j in range(7):
                if (i in [0, 1, 5, 6] and j in [0, 1, 5, 6]):
                    continue
                self.board[i][j] = tk.Button(self.master, bg="white", width=8, height=4, command=lambda i=i, j=j: self.move_piece(i, j))
                self.board[i][j].grid(row=i, column=j)

    def move_piece(self, i, j):
        print(f"Peça selecionada na posição: ({i}, {j})")
        # Aqui será implementada a lógica para mover as peças e comunicar o movimento ao servidor

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.10.125', 12453))
    return client

def main():
    client_socket = connect_to_server()
    # Aguarda mensagem do servidor para iniciar o jogo
    message = client_socket.recv(1024).decode()
    print(message)

    root = tk.Tk()
    gui = RestaUmGUI(root, client_socket)
    root.mainloop()

if __name__ == "__main__":
    main()
