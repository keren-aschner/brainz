import socket
from datetime import datetime

from .utils.thought import Thought


def upload_thought(address, user, thought):
    msg = Thought(user, datetime.now(), thought).serialize()

    with socket.socket() as conn:
        conn.connect(address)
        conn.sendall(msg)
    print('done')
