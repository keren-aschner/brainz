import os
from datetime import datetime
from pathlib import Path


class Context:
    TIMESTAMP = 'timestamp'
    POSE = 'pose'
    COLOR_IMAGE = 'color_image'
    DEPTH_IMAGE = 'depth_image'
    FEELINGS = 'feelings'

    def __init__(self, directory, user, snapshot):
        self.directory = Path(directory)
        self.user = user
        self.snapshot = snapshot
        self.timestamp = int(self.snapshot[self.TIMESTAMP]) / 1000

    def path(self, filename):
        dir_path = self.directory / self.user['user_id'] \
                   / f'{datetime.utcfromtimestamp(self.timestamp):%Y-%m-%d_%H-%M-%S-%f}'
        os.makedirs(dir_path, exist_ok=True)
        return dir_path / filename

    def save(self, filename, data):
        path = self.path(filename)
        with open(path, 'w+') as f:
            f.write(data)
