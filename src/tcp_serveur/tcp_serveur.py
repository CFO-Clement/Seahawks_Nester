import socket
import threading


class TCPServer:
    def __init__(self, host='0.0.0.0', port=5001):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_counter = 1

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address[0]}:{client_address[1]}")

            client_id = self.client_counter
            self.client_counter += 1

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
            client_thread.start()

    def handle_client(self, client_socket, client_id):
        try:
            # Envoyer l'ID unique au client lorsqu'il se connecte
            client_socket.sendall(str(client_id).encode('utf-8'))

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"Received message from client{client_id}: {message}")

                # Traitez la commande ici et envoyez une réponse au client si nécessaire
                response = f"Server received: {message}"
                client_socket.sendall(response.encode('utf-8'))

        finally:
            print(f"Closing connection for client{client_id}")
            client_socket.close()