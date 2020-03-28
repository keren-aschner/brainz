import pathlib
from datetime import datetime, timezone

import pytest

from brain_computer_interface.parsers.color_image_parser import parse_color_image
from brain_computer_interface.server.server import Context

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / 'resources' / 'parsers'
_USER = {'user_id': '1', 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'f'}
_TIMESTAMP_1 = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)

with open(RESOURCES / 'color_image.data', 'rb+') as f:
    image = f.read()
_SNAPSHOT_1 = {'timestamp': _TIMESTAMP_1.timestamp() * 1000,
               'color_image': dict(height=1080, width=1920, data=image)}
with open(RESOURCES / 'color_image.jpg', 'rb') as f:
    _DATA_1 = f.read()


@pytest.fixture
def context(tmp_path):
    return Context(tmp_path, _USER, _SNAPSHOT_1)


def test_parser(context):
    data_dir = context.directory

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP_1)
    assert not translation_path.exists()
    parse_color_image(context, _SNAPSHOT_1)
    assert translation_path.read_bytes() == _DATA_1


def _get_path(data_dir, user, timestamp):
    return data_dir / user['user_id'] / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/color_image.jpg'
