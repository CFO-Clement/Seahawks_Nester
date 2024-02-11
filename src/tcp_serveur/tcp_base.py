import struct

from logger import Log

log = Log("tcp_base")


class TCPBase:
    """
    Base class for TCPClient and TCPServer
    """

    def __init__(self, stop_event):
        """
        Initialize the TCPBase
        :param stop_event: The stop event
        """
        log.debug(f"Initializing TCPBase")
        self.socket = None
        self.stop_event = stop_event
        log.debug(f"TCPBase initialized")

    @staticmethod
    def _preprocess_send(message):
        """
        Preprocess a message to be sent over TCP
        :param message: The message to preprocess
        :return: The preprocessed message
        """
        log.debug(f"Preprocessing message")
        message = str(message).encode('utf-8')
        return struct.pack('>I', len(message)) + message

    def _recvall(self, n, sock):
        """
        Receive a certain amount of bytes from a socket
        :param n: The amount of bytes to receive
        :param sock: The socket to receive from
        :return: The received data
        """
        log.debug(f"Receiving {n} bytes")
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def _process_recv(self, sock):
        """
        Process the received data
        :param sock: The socket to receive from
        :return: The received data
        """
        log.debug(f"Processing received data")
        raw_msglen = self._recvall(4, sock)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self._recvall(msglen, sock)

    def _critical_fail(self, message):
        """
        Handle a critical failure
        :param message: The message to log
        :return: None
        """
        log.critical(message)
        self.stop_event.set()
