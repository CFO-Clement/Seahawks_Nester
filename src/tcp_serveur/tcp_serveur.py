import socket
import threading
import time

from logger import Log

log = Log("tcp_server")
class TCPServer:
    def __init__(self, host='0.0.0.0', port=5001):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_list = {}

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        log.info(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            log.info(f"New connection from {client_address}")
            client_id = client_socket.recv(1024).decode('utf-8')

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
            client_thread.start()

    def handle_client(self, client_socket, client_id):
        log.debug(f"Handling client {client_id}")
        self.client_list[client_id] = {'socket': client_socket, 'last_heartbeat': time.time()}

    def run_server(self):
        log.info(f"Starting server on {self.host}:{self.port}")
        server_thread = threading.Thread(target=self.start)
        server_thread.start()

    def get_client_list(self):
        log.debug(f"Getting client list")
        return list(self.client_list.keys())

    def send_message(self, client_id, message):
        log.debug(f"Sending message to {client_id}")
        if client_id in self.client_list:
            client_socket = self.client_list[client_id]['socket']
            client_socket.sendall(message.encode('utf-8'))

    def recieve_message(self, client_id, timeout=5):
        log.debug(f"Waiting for message from {client_id}")
        if client_id in self.client_list:
            client_socket = self.client_list[client_id]['socket']
            client_socket.settimeout(timeout)
            try:
                data = client_socket.recv(1024).decode('utf-8')
                log.debug(f"Received message from {client_id}")
                return data
            except socket.timeout:
                log.debug(f"Timeout reached")
                return None

    def broadcast_message(self, message):
        log.debug(f"Broadcasting message")
        for client in self.client_list.values():
            log.debug(f"Sending message to {client['socket'].getpeername()}")
            client['socket'].sendall(message.encode('utf-8'))

    def close_client(self, client_id):
        log.debug(f"Closing client {client_id}")
        if client_id in self.client_list:
            self.client_list[client_id]['socket'].close()
            del self.client_list[client_id]

    def heartbeat_client(self, client_id):
        log.debug(f"Heartbeating client {client_id}")
        if client_id in self.client_list:
            try:
                self.client_list[client_id]['socket'].sendall(b'HEARTBEAT')
                # Update the last heartbeat time
                self.client_list[client_id]['last_heartbeat'] = time.time()
            except socket.error:
                self.close_client(client_id)

    def start_heartbeats(self):
        dead_clients = []
        while True:
            for client_id in list(self.client_list.keys()):
                self.heartbeat_client(client_id)
                if time.time() - self.client_list[client_id]['last_heartbeat'] > 30:
                    # Client is non-responsive
                    dead_clients.append(client_id)
            time.sleep(5)  # Pause between heartbeat cycles
            return dead_clients