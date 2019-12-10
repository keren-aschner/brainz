import os
import struct
import threading
from pathlib import PurePath

from brain_computer_interface.utils.thought import Thought
from .utils import Listener


def run_server(address, data):
    host, port = address
    listener = Listener(port, host)
    listener.start()
    try:
        while True:
            client = listener.accept()
            handler = Handler(client, data)
            handler.start()
    except KeyboardInterrupt:
        listener.stop()


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        header = self.connection.receive(20)
        thought_size = struct.unpack('I', header[-4:])[0]
        thought = Thought.deserialize(header + self.connection.receive(thought_size))
        self.save_thought(thought)
        self.connection.close()

    def save_thought(self, thought):
        timestamp = str(thought.timestamp).replace(' ', '_').replace(':', '-')
        dir_path = PurePath(self.data_dir, str(thought.user_id))
        file_path = PurePath(dir_path, timestamp + '.txt')
        self.lock.acquire()
        try:
            os.makedirs(dir_path, exist_ok=True)
            if os.path.isfile(file_path):
                thought.thought = '\n' + thought.thought
            with open(file_path, 'a+') as f:
                f.write(thought.thought)
        finally:
            self.lock.release()
