import os
from pathlib import Path


class Processor:
    def __init__(self, directory, user):
        self.directory = Path(directory)
        self.user = user

    def process(self, snapshot):
        raise NotImplementedError

    def get_dir(self, timestamp):
        dir_path = self.directory / str(self.user.id) / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}'
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
