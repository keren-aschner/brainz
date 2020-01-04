from datetime import datetime, timezone

import pytest

from brain_computer_interface.server.processors.translation_processor import process_translation
from brain_computer_interface.server.server import Context

_USER = {'user_id': '1', 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
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
def context(tmp_path):
    return Context(tmp_path, _USER)


def test_processor(context):
    data_dir = context.directory

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP_1)
    assert not translation_path.exists()
    process_translation(context, _SNAPSHOT_1)
    assert translation_path.read_text() == _DATA_1

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP_2)
    assert not translation_path.exists()
    process_translation(context, _SNAPSHOT_2)
    assert translation_path.read_text() == _DATA_2


def _get_path(data_dir, user, timestamp):
    return data_dir / user['user_id'] / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/translation.json'
