import json
import pathlib
from datetime import datetime, timezone

import pytest

from brainz.client.mind.protobuf_parser import ProtobufParser, ParsingError
from brainz.protocol.fields import *

RESOURCES = pathlib.Path(__file__).absolute().parent.parent.parent / "resources" / "client" / "mind"
with open(RESOURCES / "color_image.bin", "rb") as f:
    _COLOR_IMAGE = f.read()

with open(RESOURCES / "depth_image.json", "r") as f:
    _DEPTH_IMAGE = json.load(f)


@pytest.fixture
def parser():
    return ProtobufParser()


def test_parse_user(parser):
    user_file = open(RESOURCES / "user.proto", "rb")
    user = parser.parse_user(user_file)
    user_file.close()
    assert user[USER_ID] == "42"
    assert user[USERNAME] == "Dan Gittik"
    assert user[BIRTHDAY] == datetime(1992, 3, 4, 22, tzinfo=timezone.utc).timestamp()
    assert user[GENDER] == "MALE"


def test_parse_snapshot(parser):
    snapshot_file = open(RESOURCES / "snapshot.proto", "rb")
    snapshot = parser.parse_snapshot(snapshot_file)
    snapshot_file.close()
    assert snapshot[TIMESTAMP] == "1575446887339"
    pose = snapshot[POSE]
    translation = pose[TRANSLATION]
    assert translation["x"] == 0.4873843491077423
    assert translation["y"] == 0.007090016733855009
    assert translation["z"] == -1.1306129693984985
    rotation = pose[ROTATION]
    assert rotation["x"] == -0.10888676356214629
    assert rotation["y"] == -0.26755994585035286
    assert rotation["z"] == -0.021271118915446748
    assert rotation["w"] == 0.9571326384559261
    feelings = snapshot[FEELINGS]
    assert feelings[HUNGER] == 0
    assert feelings[THIRST] == 0
    assert feelings[EXHAUSTION] == 0
    assert feelings[HAPPINESS] == 0
    color_image = snapshot[COLOR_IMAGE]
    assert color_image[HEIGHT] == 1080
    assert color_image[WIDTH] == 1920
    assert color_image[DATA] == _COLOR_IMAGE
    depth_image = snapshot[DEPTH_IMAGE]
    assert depth_image[HEIGHT] == 172
    assert depth_image[WIDTH] == 224
    assert depth_image[DATA] == _DEPTH_IMAGE


def test_not_enough_data(parser):
    user_file = open(RESOURCES / "user.proto", "rb")
    with pytest.raises(ParsingError):
        parser.parse_snapshot(user_file)
    user_file.close()
