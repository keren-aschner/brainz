import json
import os
import pathlib
import time
from datetime import datetime, timezone

import pytest
from bson.json_util import dumps

from brainz.protocol.fields import *
from brainz.server.server import get_app

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / "resources" / "server"
_SERVER_HOST = "127.0.0.1"
_SERVER_PORT = 5000

_CONFIG = {TIMESTAMP, POSE}

_USER = {
    USER_ID: 1,
    USERNAME: "Keren Solodkin",
    BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
    GENDER: "FEMALE",
}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)
_SNAPSHOT = {
    TIMESTAMP: _TIMESTAMP.timestamp() * 1000,
    POSE: {TRANSLATION: {"x": 0.487, "y": 0.009, "z": -1.13}, ROTATION: {"x": 0.487, "y": 0.009, "z": -1.13, "w": 2.5}},
}


@pytest.fixture
def client(tmp_path):
    def publish_message(message):
        with open(tmp_path / "file", "w") as f:
            f.write(message)

    cwd = os.getcwd()

    os.chdir(RESOURCES)
    app = get_app(publish_message)
    with app.test_client() as client:
        yield client, tmp_path

    os.chdir(cwd)


def test_config(client):
    client, _ = client
    config = client.get("/config").json["config"]
    assert set(config) == _CONFIG


def test_snapshot(client):
    client, data_dir = client
    time.sleep(0.5)
    response = client.post("/snapshot", data=dumps({USER: _USER, SNAPSHOT: _SNAPSHOT}))
    assert response.status_code == 200
    f = data_dir / "file"
    assert f.read_text() == json.dumps({USER: _USER, SNAPSHOT: _SNAPSHOT})
