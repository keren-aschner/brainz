import os
import pathlib
from datetime import datetime, timezone

from brainz.parsers.context import Context
from brainz.parsers.parsers.color_image_parser import parse_color_image
from brainz.protocol.fields import *
from brainz.protocol.parsers_saver import deserialize
from brainz.protocol.server_parsers import serialize

RESOURCES = pathlib.Path(__file__).absolute().parent.parent.parent / 'resources' / 'parsers' / 'parsers'
_USER = {USER_ID: 1, USERNAME: 'Keren Solodkin', BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         GENDER: 'f'}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)

with open(RESOURCES / 'color_image.bin', 'rb') as f:
    image = f.read()
_SNAPSHOT = {TIMESTAMP: _TIMESTAMP.timestamp() * 1000, COLOR_IMAGE: dict(height=1080, width=1920, data=image)}
with open(RESOURCES / 'color_image.jpg', 'rb') as f:
    _DATA = f.read()


def test_parser():
    color_image_path = _get_path(Context.BASE_DIR, _USER, _TIMESTAMP)
    if color_image_path.exists():
        os.remove(color_image_path)
    assert not color_image_path.exists()

    result = deserialize(parse_color_image(serialize(_USER, _SNAPSHOT)))

    assert result[USER] == _USER
    assert result[TIMESTAMP] == _TIMESTAMP.timestamp()
    assert result['path'] == str(color_image_path.absolute())
    assert color_image_path.read_bytes() == _DATA

    os.remove(color_image_path)


def _get_path(data_dir, user, timestamp):
    return data_dir / str(user[USER_ID]) / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}/color_image.jpg'
