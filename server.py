import socket
import threading
import pickle

class GameServer:
    def __init__(self, host='192.168.0.7', port=22222):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.current_turn = 0  # 0 para o primeiro jogador, 1 para o segundo

    def accept_connections(self):
        print("Servidor iniciado, aguardando conexões...")
        while True:
            if len(self.clients) < 2:  # Permite apenas duas conexões
                client, addr = self.server_socket.accept()
                print(f"Conexão recebida de {addr}")
                self.clients.append(client)

                if len(self.clients) == 1:
                    print("Você é o jogador 1")
                    client.send(pickle.dumps({"action": "set_turn", "turn": True}))
                elif len(self.clients) == 2:
                    print("Você é o jogador 2")
                    for index, client in enumerate(self.clients):
                        threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
                        turn_message = {"action": "set_turn", "turn": index == 0}
                        client.send(pickle.dumps(turn_message))

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(4096)
                if data:
                    action_data = pickle.loads(data)
                    print(f"Ação recebida: {action_data}")

                    if action_data['action'] == 'give_up':
                        (print("venceu"))
                        winner_socket = next(sock for sock in self.clients if sock != client)
                        winner_message = {'action': 'win'}
                        winner_socket.send(pickle.dumps(winner_message))
                        break
                    elif action_data['action'] == 'chat':
                        for c in self.clients:
                            if c != client:
                                c.send(pickle.dumps(action_data))

                    for c in self.clients:
                        if c != client:
                            try:
                                c.send(pickle.dumps(action_data))
                            except Exception as e:
                                print(f"Erro ao enviar dados para o cliente: {e}")
                                self.clients.remove(c)

            except Exception as e:
                print(f"Erro ao gerenciar cliente: {e}")
                self.clients.remove(client)
                break

if __name__ == '__main__':
    server = GameServer()
    server.accept_connections()

