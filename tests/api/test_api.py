import pathlib
from datetime import datetime, timezone

import pytest

from brainz.api.api import get_app
from brainz.api.resources import ResultData
from brainz.protocol.fields import *

RESOURCES = pathlib.Path(__file__).absolute().parent.parent / "resources" / "api"
COLOR_IMAGE_PATH = RESOURCES / "color_image.jpg"

SNAPSHOT_ID = "snapshot_id"

_USER = {
    USER_ID: 1,
    USERNAME: "Keren Solodkin",
    BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
    GENDER: "FEMALE",
}

_SNAPSHOT_1 = {
    USER_ID: 1,
    TIMESTAMP: 1588784115.516298,
    FEELINGS: {HAPPINESS: 0.6, THIRST: 0.15, HUNGER: -0.7, EXHAUSTION: -0.24},
    POSE: {TRANSLATION: {"x": 0.487, "y": 0.009, "z": -1.13}, ROTATION: {"x": 0.487, "y": 0.009, "z": -1.13, "w": 2.5}},
    COLOR_IMAGE: {"path": str(COLOR_IMAGE_PATH)},
}

_SNAPSHOT_2 = {
    USER_ID: 1,
    TIMESTAMP: 1588784116.916836,
    FEELINGS: {HAPPINESS: 0.5, THIRST: 0.1, HUNGER: -0.5, EXHAUSTION: -0.1},
}


@pytest.fixture
def client(mongodb):
    mongodb.snapshots.update_one(
        {TIMESTAMP: _SNAPSHOT_1[TIMESTAMP]}, {"$set": {COLOR_IMAGE: _SNAPSHOT_1[COLOR_IMAGE]}}, upsert=True
    )
    app = get_app(mongodb)
    with app.test_client() as client:
        yield client


def test_users(client):
    assert client.get("/users").json == [{USER_ID: _USER[USER_ID], USERNAME: _USER[USERNAME]}]


def test_user(client):
    assert client.get("/users/1").json == _USER


def test_snapshots(client):
    snapshots = client.get("/users/1/snapshots").json
    assert snapshots[0][TIMESTAMP] == _SNAPSHOT_1[TIMESTAMP]
    assert snapshots[1][TIMESTAMP] == _SNAPSHOT_2[TIMESTAMP]


def test_feelings(client):
    feelings_list = client.get("/users/1/feelings").json
    for feelings in feelings_list:
        if feelings[TIMESTAMP] == _SNAPSHOT_1[TIMESTAMP]:
            assert feelings[FEELINGS] == _SNAPSHOT_1[FEELINGS]
        else:
            assert feelings[FEELINGS] == _SNAPSHOT_2[FEELINGS]


def test_snapshot(client):
    snapshot_id = client.get("/users/1/snapshots").json[0][SNAPSHOT_ID]
    snapshot = client.get(f"/users/1/snapshots/{snapshot_id}").json
    assert snapshot == {
        SNAPSHOT_ID: snapshot_id,
        TIMESTAMP: _SNAPSHOT_1[TIMESTAMP],
        "fields": [FEELINGS, POSE, COLOR_IMAGE],
    }


def test_results_feelings(client):
    result(client, FEELINGS)
    result(client, POSE)
    result(client, COLOR_IMAGE)


def result(client, result_name):
    snapshot_id = client.get("/users/1/snapshots").json[0][SNAPSHOT_ID]
    result = client.get(f"/users/1/snapshots/{snapshot_id}/{result_name}").json
    assert result == _SNAPSHOT_1[result_name]


def test_result_data(client, mongodb):
    snapshot_id = client.get("/users/1/snapshots").json[0][SNAPSHOT_ID]
    # color_image = client.get(f"/users/1/snapshots/{snapshot_id}/color_image/data")
    color_image = ResultData(mongodb).get(1, snapshot_id, "color_image")
    with open(COLOR_IMAGE_PATH, "rb") as f:
        data = f.read()
    assert color_image == data


def test_result_data_exception(client):
    snapshot_id = client.get("/users/1/snapshots").json[0][SNAPSHOT_ID]
    response = client.get(f"/users/1/snapshots/{snapshot_id}/pose/data")
    assert response.status_code == 404
