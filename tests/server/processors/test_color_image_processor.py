import pathlib
from datetime import datetime, timezone

import pytest

from brain_computer_interface.server.processors.color_image_processor import ColorImageProcessor

RESOURCES = pathlib.Path(__file__).absolute().parent.parent.parent / 'resources' / 'server' / 'processors'
_USER = {'userId': 1, 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'f'}
_TIMESTAMP_1 = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)

with open(RESOURCES / 'color_image', 'rb+') as f:
    image = f.read()
_SNAPSHOT_1 = {'timestamp': _TIMESTAMP_1.timestamp() * 1000,
               'colorImage': dict(height=1080, width=1920, data=image)}
with open(RESOURCES / 'color_image.jpg', 'rb') as f:
    _DATA_1 = f.read()


@pytest.fixture
def color_image_processor(tmp_path):
    return ColorImageProcessor(tmp_path, _USER)


def test_processor(color_image_processor):
    data_dir = color_image_processor.directory

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP_1)
    assert not translation_path.exists()
    color_image_processor.process(_SNAPSHOT_1)
    assert translation_path.read_bytes() == _DATA_1


def _get_path(data_dir, user, timestamp):
    return data_dir / str(user['userId']) / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/color_image.jpg'
