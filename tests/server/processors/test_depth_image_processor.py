import pathlib
from datetime import datetime, timezone

import pytest
import json
from brain_computer_interface.server.processors.depth_image_processor import process_depth_image
from brain_computer_interface.server.server import Context

RESOURCES = pathlib.Path(__file__).absolute().parent.parent.parent / 'resources' / 'server' / 'processors'
_USER = {'user_id': '1', 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'f'}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)

with open(RESOURCES / 'depth_image.json', 'rb+') as f:
    image = json.load(f)
_SNAPSHOT = {'timestamp': _TIMESTAMP.timestamp() * 1000, 'depth_image': dict(height=172, width=224, data=image)}
with open(RESOURCES / 'depth_image.jpg', 'rb') as f:
    _DATA = f.read()


@pytest.fixture
def context(tmp_path):
    return Context(tmp_path, _USER, _SNAPSHOT)


def test_processor(context):
    data_dir = context.directory

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP)
    assert not translation_path.exists()
    process_depth_image(context, _SNAPSHOT)
    assert translation_path.read_bytes() == _DATA


def _get_path(data_dir, user, timestamp):
    return data_dir / user['user_id'] / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/depth_image.jpg'
