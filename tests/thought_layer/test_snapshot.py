import pathlib
from datetime import datetime

import pytest
from construct import Container

from brain_computer_interface.thought_layer import Snapshot

timestamp = datetime(2019, 12, 4, 8, 8, 7, 339000)
translation = Container(x=0.4873843491077423, y=0.007090016733855009, z=-1.1306129693984985)
rotation = Container(x=-0.10888676356214629, y=-0.26755994585035286, z=-0.021271118915446748, w=0.9571326384559261)
color_image = Container(height=10, width=20, image=[(1, 2, 3) for _ in range(10 * 20)])
depth_image = Container(height=12, width=14, image=[0.0 for _ in range(12 * 14)])
feelings = Container(hunger=0, thirst=0, exhaustion=0, happiness=0)

with open(pathlib.Path(__file__).absolute().parent / 'resources' / 'snapshot.bin', 'rb') as f:
    bin_data = f.read()


@pytest.fixture
def snapshot():
    return Snapshot(timestamp, translation, rotation, color_image, depth_image, feelings)


def test_serialize(snapshot):
    assert snapshot.serialize() == bin_data


def test_deserialize(snapshot):
    assert Snapshot.deserialize(bin_data) == snapshot


def test_symmetry(snapshot):
    assert Snapshot.deserialize(snapshot.serialize()) == snapshot

# TODO test creating partial data
