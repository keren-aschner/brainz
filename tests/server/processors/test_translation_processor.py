from datetime import datetime

import pytest
from construct import Container

from brain_computer_interface.server.processors.translation_processor import TranslationProcessor
from brain_computer_interface.thought_layer import Hello, Snapshot

_USER = Hello(id=1, name='Keren Solodkin', birth_date=datetime(1997, 2, 25), gender='f')
_TIMESTAMP_1 = datetime(2019, 10, 25, 15, 12, 5, 228000)
_SNAPSHOT_1 = Snapshot(timestamp=_TIMESTAMP_1, translation=Container(x=0.487, y=0.009, z=-1.13))
_DATA_1 = '{"x": 0.487, "y": 0.009, "z": -1.13}'
_TIMESTAMP_2 = datetime(2019, 10, 25, 15, 15, 2, 304000)
_SNAPSHOT_2 = Snapshot(timestamp=_TIMESTAMP_2, translation=Container(x=0.298, y=0.1, z=-2.97))
_DATA_2 = '{"x": 0.298, "y": 0.1, "z": -2.97}'


@pytest.fixture
def translation_processor(tmp_path):
    return TranslationProcessor(tmp_path, _USER)


def test_processor(translation_processor):
    data_dir = translation_processor.directory

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP_1)
    assert not translation_path.exists()
    translation_processor.process(_SNAPSHOT_1)
    assert translation_path.read_text() == _DATA_1

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP_2)
    assert not translation_path.exists()
    translation_processor.process(_SNAPSHOT_2)
    assert translation_path.read_text() == _DATA_2


def _get_path(data_dir, user, timestamp):
    return data_dir / f'{user.id}/{timestamp:%Y-%m-%d_%H-%M-%S-%f}/translation.json'
