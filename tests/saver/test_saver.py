from datetime import datetime, timezone
from unittest.mock import patch, call

from brainz.protocol.fields import *
from brainz.protocol.parsers_saver import serialize
from brainz.saver import Saver

_USER = {USER_ID: '1', USERNAME: 'Keren Solodkin', BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
         GENDER: 'f'}
_TIMESTAMP = datetime(2019, 10, 25, 15, 12, 5, 228000, tzinfo=timezone.utc)

DATA = {'data': 'data'}


@patch('pymongo.collection.Collection.update_one')
def test_saver(update_mock):
    saver = Saver('mongodb://127.0.0.1:27017')
    saver.save('topic', serialize({USER: _USER, TIMESTAMP: _TIMESTAMP.timestamp(), **DATA}))

    assert update_mock.call_args_list[0] == call({USER_ID: '1'}, {
        '$set': {USERNAME: 'Keren Solodkin', BIRTHDAY: datetime(1997, 2, 25, tzinfo=timezone.utc).timestamp(),
                 GENDER: 'f'}}, upsert=True)

    assert update_mock.call_args_list[1] == call({USER_ID: '1', TIMESTAMP: 1572016325.228},
                                                 {'$set': {'topic': {'data': 'data'}}}, upsert=True)
