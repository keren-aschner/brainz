import logging
import threading

from ..thought_layer import Hello, Config, Snapshot
from ..utils import Listener

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def run_server(address, data):
    host, port = address
    with Listener(port, host) as listener:
        logger.info('Started listening')
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
        logger.info('got hello')
        self.connection.send(Config(list(self.fields)).serialize())
        logger.info('sent config')
        snapshot = Snapshot.deserialize(self.connection.receive())
        logger.info('got snapshot')
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
