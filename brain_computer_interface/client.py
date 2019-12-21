from datetime import datetime

from .utils import Connection
from .utils.thought import Thought


def upload_thought(address, user, thought):
    msg = Thought(user, datetime.now(), thought).serialize()

    with Connection.connect(address) as conn:
        conn.send(msg)

    print('done')
