from datetime import datetime, timezone

from brain_computer_interface.parsers.parsers.feelings_parser import parse_feelings
from brain_computer_interface.protocol.fields import *
from brain_computer_interface.protocol.parsers_saver import deserialize
from brain_computer_interface.protocol.server_parsers import serialize

_USER = {USER_ID: '1', USERNAME: 'Keren Solodkin', BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         GENDER: 'f'}
_FEELINGS = {HUNGER: -0.5, HAPPINESS: 0.99, EXHAUSTION: 0.0, THIRST: 0.1}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {TIMESTAMP: _TIMESTAMP.timestamp() * 1000, FEELINGS: _FEELINGS}


def test_parser():
    result = deserialize(parse_feelings(serialize(_USER, _SNAPSHOT)))
    assert result[USER] == _USER
    assert result[TIMESTAMP] == _TIMESTAMP.timestamp()
    assert result[FEELINGS] == _FEELINGS
