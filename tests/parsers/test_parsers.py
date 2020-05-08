import os
import pathlib
from datetime import datetime, timezone

import pytest
from click.testing import CliRunner

from brainz.parsers import get_all_fields, parse
from brainz.parsers.__main__ import cli
from brainz.protocol.fields import *
from brainz.protocol.parsers_saver import deserialize
from brainz.protocol.server_parsers import serialize

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / "resources" / "parsers"
_USER = {
    USER_ID: 1,
    USERNAME: "Keren Solodkin",
    BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
    GENDER: "f",
}
_POSE = {TRANSLATION: {"x": 0.487, "y": 0.009, "z": -1.13}, ROTATION: {"x": 0.487, "y": 0.009, "z": -1.13, "w": 2.5}}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {TIMESTAMP: _TIMESTAMP.timestamp() * 1000, POSE: _POSE}


@pytest.fixture(autouse=True)
def cd_resources():
    cwd = os.getcwd()
    os.chdir(RESOURCES)
    yield
    os.chdir(cwd)


def test_get_all_fields():
    assert set(get_all_fields()) == {COLOR_IMAGE, POSE, TIMESTAMP}


def test_parse():
    result = deserialize(parse(POSE, serialize(_USER, _SNAPSHOT)))
    assert result[USER] == _USER
    assert result[TIMESTAMP] == _TIMESTAMP.timestamp()
    assert result[DATA] == _POSE


def test_cli_parse():
    result = deserialize(CliRunner().invoke(cli, ["parse", POSE, "pose.data"]).output)

    assert result[USER] == _USER
    assert result[TIMESTAMP] == _TIMESTAMP.timestamp()
    assert result[DATA] == _POSE


def test_run_parser_exception():
    result = CliRunner().invoke(cli, ["run-parser", POSE, "notrmq://127.0.0.1:1234"])
    assert result.exc_info[0] == NotImplementedError
