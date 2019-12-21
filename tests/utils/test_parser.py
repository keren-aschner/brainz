import pathlib
from datetime import datetime, timezone, timedelta

import pytest

from brain_computer_interface.utils.parser import parse_user, parse_snapshot, ParsingError

RESOURCES = pathlib.Path(__file__).absolute().parent / 'resources'

UTC2 = timezone(timedelta(hours=2))


def test_parse_user():
    f = open(RESOURCES / 'user.bin', 'rb')
    user = parse_user(f)
    f.close()
    assert user.id == 42
    assert user.name == 'Dan Gittik'
    assert user.birth_date == datetime(1992, 3, 5, tzinfo=UTC2)
    assert user.gender == 'm'


def test_parse_snapshot():
    f = open(RESOURCES / 'snapshot.bin', 'rb')
    snapshot = parse_snapshot(f)
    f.close()
    assert snapshot.timestamp == datetime(2019, 12, 4, 10, 8, 7, 339000, tzinfo=UTC2)
    assert snapshot.translation.x == 0.4873843491077423
    assert snapshot.translation.y == 0.007090016733855009
    assert snapshot.translation.z == -1.1306129693984985
    assert snapshot.rotation.x == -0.10888676356214629
    assert snapshot.rotation.y == -0.26755994585035286
    assert snapshot.rotation.z == -0.021271118915446748
    assert snapshot.rotation.w == 0.9571326384559261
    assert snapshot.feelings.hunger == 0
    assert snapshot.feelings.thirst == 0
    assert snapshot.feelings.exhaustion == 0
    assert snapshot.feelings.happiness == 0
    assert snapshot.color_image.height == 1080
    assert snapshot.color_image.width == 1920
    assert len(snapshot.color_image.image) == 1080 * 1920
    assert snapshot.color_image.image[0] == [149, 174, 108]
    assert snapshot.depth_image.height == 172
    assert snapshot.depth_image.width == 224
    assert len(snapshot.depth_image.image) == 172 * 224
    assert snapshot.depth_image.image[0] == 0.0


def test_not_enough_data():
    f = open(RESOURCES / 'user.bin', 'rb')
    with pytest.raises(ParsingError):
        parse_snapshot(f)
    f.close()
