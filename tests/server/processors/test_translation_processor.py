from datetime import datetime, timezone

import pytest

from brain_computer_interface.server.processors.translation_processor import TranslationProcessor

_USER = {'user_id': 1, 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'f'}
_TIMESTAMP_1 = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT_1 = {'timestamp': _TIMESTAMP_1.timestamp() * 1000,
               'pose': {'translation': {'x': 0.487, 'y': 0.009, 'z': -1.13}}}
_DATA_1 = '{"x": 0.487, "y": 0.009, "z": -1.13}'
_TIMESTAMP_2 = datetime(2019, 10, 25, 15, 15, 2, 304000, tzinfo=timezone.utc)
_SNAPSHOT_2 = {'timestamp': _TIMESTAMP_2.timestamp() * 1000,
               'pose': {'translation': {'x': 0.298, 'y': 0.1, 'z': -2.97}}}
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
    return data_dir / str(user['user_id']) / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/translation.json'
