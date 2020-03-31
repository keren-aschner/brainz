from datetime import datetime, timezone

from brain_computer_interface.parsers.parsers.pose_parser import parse_pose
from brain_computer_interface.protocol.fields import *
from brain_computer_interface.protocol.parsers_saver import deserialize
from brain_computer_interface.protocol.server_parsers import serialize

_USER = {USER_ID: '1', USERNAME: 'Keren Solodkin', BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         GENDER: 'f'}
_POSE = {TRANSLATION: {'x': 0.487, 'y': 0.009, 'z': -1.13},
         ROTATION: {'x': 0.487, 'y': 0.009, 'z': -1.13, 'w': 2.5}}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {TIMESTAMP: _TIMESTAMP.timestamp() * 1000, POSE: _POSE}


def test_parser():
    result = deserialize(parse_pose(serialize(_USER, _SNAPSHOT)))
    assert result[USER] == _USER
    assert result[TIMESTAMP] == _TIMESTAMP.timestamp()
    assert result[POSE] == _POSE
