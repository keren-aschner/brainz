import pytest

from brain_computer_interface.thought_layer import Config

fields = ['timestamp', 'translation', 'rotation', 'color_image', 'feelings']

bin_data = b'\x05\x00\x00\x00\t\x00\x00\x00timestamp\x0b\x00\x00\x00translation\x08\x00\x00\x00rotation' \
           + b'\x0b\x00\x00\x00color_image\x08\x00\x00\x00feelings'


@pytest.fixture
def config():
    return Config(fields)


def test_serialize(config):
    assert config.serialize() == bin_data


def test_deserialize(config):
    assert Config.deserialize(bin_data) == config


def test_symmetry(config):
    assert Config.deserialize(config.serialize()) == config
