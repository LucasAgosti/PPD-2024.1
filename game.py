import tkinter as tk
import tkinter.messagebox as messagebox
import socket
import threading
import pickle  # Para serializar/deserializar objetos para envio através de sockets

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Resta 1')
        self.board = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [ 1,  1, 1, 1, 1,  1,  1],
            [ 1,  1, 1, 0, 1,  1,  1],
            [ 1,  1, 1, 1, 1,  1,  1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1]
        ]
        self.canvas = tk.Canvas(self, width=350, height=350)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.selected_peg = None

    def draw_peg(self, row, col, color='black'):
        x0 = col * 50 + 15
        y0 = row * 50 + 15
        x1 = x0 + 20
        y1 = y0 + 20
        self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags="peg")

    def draw_board(self):
        self.canvas.delete("peg")  # Remove existing pegs before redrawing
        for row in range(7):
            for col in range(7):
                if self.board[row][col] == 1:
                    self.draw_peg(row, col)

    def on_canvas_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if 0 <= row < 7 and 0 <= col < 7:  # Check if click is within bounds
            if self.selected_peg:
                if self.is_valid_move(self.selected_peg, (row, col)):
                    self.make_move(self.selected_peg, (row, col))
                    self.draw_board()
                    if self.check_game_state():  # If game is over, don't reset selected_peg
                        return
                    self.selected_peg = None
                else:
                    self.selected_peg = None  # Deselect if the move is invalid
            elif self.board[row][col] == 1:
                self.selected_peg = (row, col)

    def is_valid_move(self, start_pos, end_pos):
        # Check bounds and ensure end position is empty and the start position has a peg
        if (0 <= end_pos[0] < 7 and 0 <= end_pos[1] < 7 and self.board[end_pos[0]][end_pos[1]] == 0 and
                self.board[start_pos[0]][start_pos[1]] == 1):
            row_diff = end_pos[0] - start_pos[0]
            col_diff = end_pos[1] - start_pos[1]

            if abs(row_diff) == 2 and col_diff == 0:
                return self.board[start_pos[0] + row_diff // 2][start_pos[1]] == 1
            if abs(col_diff) == 2 and row_diff == 0:
                return self.board[start_pos[0]][start_pos[1] + col_diff // 2] == 1
        return False

    def make_move(self, start_pos, end_pos, update_server=True):
        self.board[start_pos[0]][start_pos[1]] = 0
        self.board[end_pos[0]][end_pos[1]] = 1
        self.board[(start_pos[0] + end_pos[0]) // 2][(start_pos[1] + end_pos[1]) // 2] = 0
        if update_server:
            # Enviar detalhes da jogada ao servidor
            move_details = {'action': 'move', 'start_pos': start_pos, 'end_pos': end_pos}
            self.send_data_to_server(move_details)

    def check_game_state(self):
        peg_count = sum(row.count(1) for row in self.board)
        if peg_count == 1:
            print("Parabéns, você venceu!")
            return True
        elif not self.any_valid_moves():
            print("Fim de jogo, não há mais movimentos possíveis")
            return True
        return False

    def any_valid_moves(self):
        for row in range(7):
            for col in range(7):
                if self.board[row][col] == 1:
                    # Check all four possible moves for each peg
                    for drow, dcol in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                        if self.is_valid_move((row, col), (row + drow, col + dcol)):
                            return True
        return False

    def connect_to_server(self, host='172.20.10.10', port=11112):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((host, port))
            threading.Thread(target=self.receive_data_from_server, daemon=True).start()
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")

    def receive_data_from_server(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
                if data:
                    message = pickle.loads(data)
                    # Aqui, trate as mensagens recebidas do servidor
                    if message['action'] == 'move':
                        self.make_move(message['start_pos'], message['end_pos'], update_server=False)
                        self.draw_board()
            except Exception as e:
                print(f"Erro ao receber dados: {e}")
                break

    def send_data_to_server(self, data):
        try:
            self.client_socket.send(pickle.dumps(data))
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    game = Game()
    game.connect_to_server()
    game.run()
