import socket
from datetime import datetime

from .utils.thought import Thought


def upload_thought(address, user, thought):
    host, port = address.split(':')
    msg = Thought(int(user), datetime.now(), thought).serialize()

    with socket.socket() as conn:
        conn.connect((host, int(port)))
        conn.sendall(msg)
    print('done')
