import os
from datetime import datetime
from pathlib import Path


class Context:
    def __init__(self, directory, user):
        self.directory = Path(directory)
        self.user = user

    def path(self, timestamp, filename):
        dir_path = self.directory / self.user['user_id'] \
                   / f'{datetime.utcfromtimestamp(int(timestamp) / 1000):%Y-%m-%d_%H-%M-%S-%f}'
        os.makedirs(dir_path, exist_ok=True)
        return dir_path / filename
