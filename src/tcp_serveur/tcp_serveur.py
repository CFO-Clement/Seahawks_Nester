import socket
import threading
import time

from logger import Log

from .tcp_base import TCPBase

log = Log("tcp_server")


class TCPServer(TCPBase):
    def __init__(self, host, port, stop_event):
        super().__init__(stop_event)
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_list = {}

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            log.info(f"Server listening on {self.host}:{self.port}")
        except Exception as e:
            log.error(f"Error while starting server: {e}")
            self._critical_fail(f"Error while starting server: {e}")

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                log.info(f"New connection from {client_address}")
                client_id = self._process_recv(client_socket).decode('utf-8')
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
                client_thread.start()
            except OSError as e:
                log.error(f"Error while accepting client: {e}")
                self._critical_fail(f"Error while accepting client: {e}")
                return

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
        log.debug(f"Sending {message} to {client_id} -> {self.client_list[client_id]['socket'].getpeername()}")
        if client_id in self.client_list:
            client_socket = self.client_list[client_id]['socket']
            client_socket.sendall(self._preprocess_send(message))
            log.debug(f"Message sent")
        else:
            log.error(f"Client {client_id} not found in {self.client_list}")

    def recieve_message(self, client_id, timeout=5000):
        log.debug(f"Waiting for message from {client_id}")
        if client_id in self.client_list:
            client_socket = self.client_list[client_id]['socket']
            client_socket.settimeout(timeout)
            try:
                data = self._process_recv(client_socket)
                log.debug(f"Received message from {client_id}")
                data = data.decode('utf-8')
                log.debug(f"Decoded message: {data}")
                return data
            except socket.timeout:
                log.warning(f"Timeout reached")
                return None
            except Exception:
                log.warning(f"Exception occurred, empty message ?")
                return None

    def broadcast_message(self, message):
        log.debug(f"Broadcasting message")
        for client in self.client_list.values():
            log.debug(f"Sending message to {client['socket'].getpeername()}")
            client['socket'].sendall(self._preprocess_send(message))

    def close_client(self, client_id):
        log.debug(f"Closing client {client_id}")
        if client_id in self.client_list:
            self.send_message(client_id, 'CLOSE')
            self.client_list[client_id]['socket'].close()
            del self.client_list[client_id]

    def heartbeat_client(self, client_id):
        if client_id in self.client_list:
            try:
                self.client_list[client_id]['socket'].sendall(self._preprocess_send('HEARTBEAT'))
                self.client_list[client_id]['last_heartbeat'] = time.time()
            except socket.error:
                self.close_client(client_id)

    def handle_heartbeats(self):
        dead_clients = []
        while True:
            for client_id in list(self.client_list.keys()):
                self.heartbeat_client(client_id)
                if time.time() - self.client_list[client_id]['last_heartbeat'] > 120:
                    dead_clients.append(client_id)
            time.sleep(30)
            if dead_clients:
                log.error(f"Dead client(s) detected: {dead_clients}")
                dead_clients = []

    def start_heartbeat_thread(self):
        log.debug(f"Starting heartbeat thread")
        heartbeat_thread = threading.Thread(target=self.handle_heartbeats)
        heartbeat_thread.start()
        log.debug(f"Heartbeat thread started")
        return heartbeat_thread
