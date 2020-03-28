import json
import pathlib
from datetime import datetime, timezone

import pytest

from brain_computer_interface.client.mind.protobuf_parser import ProtobufParser, ParsingError

RESOURCES = pathlib.Path(__file__).absolute().parent.parent.parent / 'resources' / 'client' / 'mind'
with open(RESOURCES / 'color_image.data', 'r') as f:
    COLOR_IMAGE = f.read()

with open(RESOURCES / 'depth_image.json', 'r') as f:
    DEPTH_IMAGE = json.load(f)


@pytest.fixture
def parser():
    return ProtobufParser()


def test_parse_user(parser):
    user_file = open(RESOURCES / 'user.proto', 'rb')
    user = parser.parse_user(user_file)
    user_file.close()
    assert user['user_id'] == '42'
    assert user['username'] == 'Dan Gittik'
    assert user['birthday'] == datetime(1992, 3, 4, 22, tzinfo=timezone.utc).timestamp()
    assert user['gender'] == 'MALE'


def test_parse_snapshot(parser):
    snapshot_file = open(RESOURCES / 'snapshot.proto', 'rb')
    snapshot = parser.parse_snapshot(snapshot_file)
    snapshot_file.close()
    assert snapshot['timestamp'] == '1575446887339'
    pose = snapshot['pose']
    translation = pose['translation']
    assert translation['x'] == 0.4873843491077423
    assert translation['y'] == 0.007090016733855009
    assert translation['z'] == -1.1306129693984985
    rotation = pose['rotation']
    assert rotation['x'] == -0.10888676356214629
    assert rotation['y'] == -0.26755994585035286
    assert rotation['z'] == -0.021271118915446748
    assert rotation['w'] == 0.9571326384559261
    feelings = snapshot['feelings']
    assert feelings['hunger'] == 0
    assert feelings['thirst'] == 0
    assert feelings['exhaustion'] == 0
    assert feelings['happiness'] == 0
    color_image = snapshot['color_image']
    assert color_image['height'] == 1080
    assert color_image['width'] == 1920
    assert color_image['data'] == COLOR_IMAGE
    depth_image = snapshot['depth_image']
    assert depth_image['height'] == 172
    assert depth_image['width'] == 224
    assert depth_image['data'] == DEPTH_IMAGE


def test_not_enough_data(parser):
    user_file = open(RESOURCES / 'user.proto', 'rb')
    with pytest.raises(ParsingError):
        parser.parse_snapshot(user_file)
    user_file.close()
