from datetime import datetime

import pytest

from brain_computer_interface.thought_layer import Hello

user_id = 42
name = 'Dan Gittik'
birth_date = datetime(1992, 3, 4, 22)
gender = 'm'

bin_data = b'*\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00Dan Gittik`H\xb5)m'


@pytest.fixture
def hello():
    return Hello(user_id, name, birth_date, gender)


def test_serialize(hello):
    assert hello.serialize() == bin_data


def test_deserialize(hello):
    assert Hello.deserialize(bin_data) == hello


def test_symmetry(hello):
    assert Hello.deserialize(hello.serialize()) == hello
