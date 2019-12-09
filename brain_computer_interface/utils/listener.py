import socket

from connection import Connection


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.server = None

    def __repr__(self):
        return f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'

    def start(self):
        server = socket.socket()
        if self.reuseaddr:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(self.backlog)
        self.server = server

    def stop(self):
        self.server.close()

    def accept(self):
        client, _ = self.server.accept()
        return Connection(client)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()
