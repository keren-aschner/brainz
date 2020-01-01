import os
from pathlib import Path
from datetime import datetime


class Processor:
    def __init__(self, directory, user):
        self.directory = Path(directory)
        self.user = user

    def process(self, snapshot):
        raise NotImplementedError

    def get_dir(self, timestamp):
        dir_path = self.directory / str(
            self.user['userId']) / f'{datetime.utcfromtimestamp(int(timestamp) / 1000):%Y-%m-%d_%H-%M-%S-%f}'
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
