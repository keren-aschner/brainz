import os
from datetime import datetime
from pathlib import Path


class Context:
    TIMESTAMP = 'timestamp'
    POSE = 'pose'
    COLOR_IMAGE = 'color_image'
    DEPTH_IMAGE = 'depth_image'
    FEELINGS = 'feelings'

    def __init__(self, directory, user):
        self.directory = Path(directory)
        self.user = user

    def path(self, timestamp, filename):
        dir_path = self.directory / self.user['user_id'] \
                   / f'{datetime.utcfromtimestamp(int(timestamp) / 1000):%Y-%m-%d_%H-%M-%S-%f}'
        os.makedirs(dir_path, exist_ok=True)
        return dir_path / filename
