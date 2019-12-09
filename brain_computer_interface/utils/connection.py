import socket


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        fr = self.socket.getsockname()
        to = self.socket.getpeername()
        return f'<Connection from {fr[0]}:{fr[1]} to {to[0]}:{to[1]}>'

    @classmethod
    def connect(cls, host, port):
        s = socket.socket()
        s.connect((host, port))
        return cls(s)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b''
        while len(data) < size:
            received = self.socket.recv(size - len(data))
            if not len(received):
                raise Exception('Connection closed')
            data += received
        return data

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()
