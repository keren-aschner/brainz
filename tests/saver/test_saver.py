from datetime import datetime, timezone

import mongomock
import pytest
from click.testing import CliRunner

from brainz.protocol.fields import *
from brainz.protocol.parsers_saver import serialize

_USER = {
    USER_ID: 1,
    USERNAME: "Keren Solodkin",
    BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
    GENDER: "f",
}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)

_DATA = {DATA: "data"}
_DATA2 = {DATA: "data2"}


@pytest.fixture(autouse=True)
def mongodb():
    with mongomock.patch(servers=["localhost", "mongodb"]):
        yield


def test_cli_save():
    from pymongo import MongoClient
    from brainz.saver.__main__ import cli

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("data", "w") as f:
            f.write(serialize({USER: _USER, TIMESTAMP: _TIMESTAMP.timestamp(), **_DATA}))

        with open("data2", "w") as f:
            f.write(serialize({USER: _USER, TIMESTAMP: _TIMESTAMP.timestamp(), **_DATA2}))

        runner.invoke(cli, ["save", "topic", "data"])
        runner.invoke(cli, ["save", "topic2", "data2"])

    check_results(MongoClient("mongodb://mongodb:27017").brainz)


def test_saver():
    from brainz.saver import Saver

    saver = Saver("mongodb://localhost:27017")

    saver.save("topic", serialize({USER: _USER, TIMESTAMP: _TIMESTAMP.timestamp(), **_DATA}))
    saver.save("topic2", serialize({USER: _USER, TIMESTAMP: _TIMESTAMP.timestamp(), **_DATA2}))

    check_results(saver.db)


def check_results(db):
    assert db.users.count_documents({}) == 1
    assert db.users.find_one({}, {"_id": 0}) == _USER

    assert db.snapshots.count_documents({}) == 1
    assert db.snapshots.find_one({}, {"_id": 0}) == {
        USER_ID: 1,
        TIMESTAMP: 1572016325.228,
        "topic": _DATA[DATA],
        "topic2": _DATA2[DATA],
    }


def test_not_mongo():
    from brainz.saver import Saver

    with pytest.raises(NotImplementedError):
        Saver("postgresql://127.0.0.1:5432")
