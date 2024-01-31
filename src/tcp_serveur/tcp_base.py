import struct

from logger import Log

log = Log("tcp_base")


class TCPBase:
    def __init__(self):
        self.socket = None

    @staticmethod
    def _preprocess_send(message):
        """Prépare le message à envoyer en le codant en bytes et en ajoutant sa taille."""
        log.debug(f"Preprocessing message")
        message = str(message).encode('utf-8')
        return struct.pack('>I', len(message)) + message

    def _recvall(self, n, sock):
        """Reçoit exactement n octets du socket spécifié."""
        log.debug(f"Receiving {n} bytes")
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def _process_recv(self, sock):
        """Traite la réception d'un message en décodant d'abord sa taille puis le message lui-même."""
        log.debug(f"Processing received data")
        raw_msglen = self._recvall(4, sock)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self._recvall(msglen, sock)
