from datetime import datetime, timezone

import pytest

from brain_computer_interface.parsers.pose_parser import parse_pose
from brain_computer_interface.server.server import Context

_USER = {'user_id': '1', 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'f'}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {'timestamp': _TIMESTAMP.timestamp() * 1000,
             'pose': {'translation': {'x': 0.487, 'y': 0.009, 'z': -1.13},
                      'rotation': {'x': 0.487, 'y': 0.009, 'z': -1.13, 'w': 2.5}}}
_DATA = '{"translation": {"x": 0.487, "y": 0.009, "z": -1.13}, "rotation": {"x": 0.487, "y": 0.009, "z": -1.13, "w": 2.5}}'


@pytest.fixture
def context(tmp_path):
    return Context(tmp_path, _USER, _SNAPSHOT)


def test_parser(context):
    data_dir = context.directory

    translation_path = _get_path(data_dir, _USER, _TIMESTAMP)
    assert not translation_path.exists()
    parse_pose(context, _SNAPSHOT)
    assert translation_path.read_text() == _DATA


def _get_path(data_dir, user, timestamp):
    return data_dir / user['user_id'] / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/pose.json'
