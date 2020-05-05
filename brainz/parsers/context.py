import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

from ..protocol.fields import TIMESTAMP, USER, USER_ID, DATA
from ..protocol.parsers_saver import serialize
from ..protocol.server_parsers import deserialize


class Context:
    BASE_DIR = Path("/opt/brainz/data/")

    def __init__(self, message: bytes):
        self.user, self.snapshot = self.deserialize(message)
        self.timestamp = int(self.snapshot[TIMESTAMP]) / 1000
        self.timestamp_str = f"{datetime.utcfromtimestamp(self.timestamp):%Y-%m-%d_%H-%M-%S-%f}"

    def serialize(self, data) -> bytes:
        """
        Serialize data using the parsers-saver protocol.
        """
        return serialize({DATA: data, USER: self.user, TIMESTAMP: self.timestamp})

    def path(self, filename: str) -> Path:
        """
        Create the path for the given filename.
        """
        dir_path = self.BASE_DIR / str(self.user[USER_ID]) / self.timestamp_str
        os.makedirs(dir_path, exist_ok=True)
        return dir_path / filename

    @classmethod
    def deserialize(cls, message: bytes) -> Tuple[dict, dict]:
        """
        Deserialize using the server-parsers protocol.
        """
        return deserialize(message)
