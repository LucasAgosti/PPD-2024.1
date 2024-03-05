import socket
import threading
import pickle

class GameServer:
    def __init__(self, host='172.20.10.10', port=11117):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.current_turn = 0  # 0 para o primeiro jogador, 1 para o segundo

    # def accept_connections(self):
    #     print("Servidor iniciado, aguardando conexões...")
    #     while True:
    #         client, addr = self.server_socket.accept()
    #         print(f"Conexão recebida de {addr}")
    #         self.clients.append(client)
    #         threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def accept_connections(self):
        print("Servidor iniciado, aguardando conexões...")
        while True:
            if len(self.clients) < 2:  # Permite apenas duas conexões
                client, addr = self.server_socket.accept()
                print(f"Conexão recebida de {addr}")
                self.clients.append(client)

                if len(self.clients) == 1:
                    # Indica ao primeiro jogador que é sua vez, esperando pelo segundo jogador
                    client.send(pickle.dumps({"action": "set_turn", "turn": True}))
                elif len(self.clients) == 2:
                    # Inicia as threads de comunicação com cada cliente
                    for index, client in enumerate(self.clients):
                        threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
                        # Comunica o estado inicial do turno para cada jogador
                        turn_message = {"action": "set_turn", "turn": index == 0}
                        client.send(pickle.dumps(turn_message))

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(4096)
                if data:
                    # Aqui, trate as mensagens recebidas e possivelmente redirecione-as aos outros clientes
                    # Deserializar os dados recebidos
                    action_data = pickle.loads(data)
                    # Imprimir os dados recebidos no terminal do servidor
                    print(f"Ação recebida: {action_data}")

                    # Aqui, você pode adicionar lógica adicional para redirecionar a ação aos outros clientes, se necessário.
                    #pass

                    for c in self.clients:
                        if c != client:  # Não envia a ação de volta para o remetente
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


# if __name__ == "__main__":
#     #host = '192.168.10.125'
#     host = '172.20.10.10'
#     port = 11111
#     server = GameServer(host, port)

