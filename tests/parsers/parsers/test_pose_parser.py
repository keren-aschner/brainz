from datetime import datetime, timezone

from brain_computer_interface.parsers.parsers.pose_parser import parse_pose
from brain_computer_interface.protocol.parsers_saver import deserialize
from brain_computer_interface.protocol.server_parsers import serialize

_USER = {'user_id': '1', 'name': 'Keren Solodkin', 'birthday': datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         'gender': 'f'}
_POSE = {'translation': {'x': 0.487, 'y': 0.009, 'z': -1.13},
         'rotation': {'x': 0.487, 'y': 0.009, 'z': -1.13, 'w': 2.5}}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {'timestamp': _TIMESTAMP.timestamp() * 1000, 'pose': _POSE}


def test_parser():
    result = deserialize(parse_pose(serialize(_USER, _SNAPSHOT)))
    assert result['user'] == _USER
    assert result['timestamp'] == _TIMESTAMP.timestamp()
    assert result['pose'] == _POSE
