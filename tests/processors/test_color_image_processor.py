import pathlib
import pickle
from datetime import datetime

import pytest
from construct import Container

from brain_computer_interface.processors.color_image_processor import ColorImageProcessor
from brain_computer_interface.thought_layer import Hello, Snapshot

_USER = Hello(id=1, name='Keren Solodkin', birth_date=datetime(1997, 2, 25), gender='f')
_TIMESTAMP_1 = datetime(2019, 10, 25, 15, 12, 5, 228000)
with open(pathlib.Path(__file__).absolute().parent / 'resources' / 'color_image.pickle', 'rb') as f:
    image = pickle.load(f)
_SNAPSHOT_1 = Snapshot(timestamp=_TIMESTAMP_1, color_image=Container(height=1080, width=1920, image=image))
with open(pathlib.Path(__file__).absolute().parent / 'resources' / 'color_image.jpg', 'rb') as f:
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
    return data_dir / f'{user.id}/{timestamp:%Y-%m-%d_%H-%M-%S-%f}/color_image.jpg'
