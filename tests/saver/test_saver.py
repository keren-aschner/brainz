from unittest.mock import patch

from brain_computer_interface.saver import Saver
from brain_computer_interface.protocol.parsers_saver import serialize

DATA = {'data': 'data'}


@patch('pymongo.collection.Collection.insert_one')
def test_saver(insert_mock):
    saver = Saver('mongodb://127.0.0.1:27017')
    saver.save('topic', serialize(DATA))
    assert insert_mock.call_args.args[0] == DATA
