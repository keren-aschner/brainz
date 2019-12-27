import threading

from .thought_layer import Hello, Config, Snapshot
from .utils import Listener


def run_server(address, data):
    host, port = address
    with Listener(port, host) as listener:
        while True:
            connection = listener.accept()
            Server(connection, data).start()


class Server(threading.Thread):
    lock = threading.Lock()
    fields = set()
    processors = []

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        user = Hello.deserialize(self.connection.receive())
        self.connection.send(Config(list(self.fields)).serialize())
        snapshot = Snapshot.deserialize(self.connection.receive())
        for processor in self.processors:
            processor(self.data_dir, user).process(snapshot)
        self.connection.close()

    @classmethod
    def processor(cls, *fields):
        def decorator(cl):
            cls.fields.update(fields)
            cls.processors.append(cl)
            return cl

        return decorator
