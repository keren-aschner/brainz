from furl import furl
from pymongo import MongoClient

from ..protocol.fields import USER, USER_ID, TIMESTAMP
from ..protocol.parsers_saver import deserialize


class Saver:
    def __init__(self, database_url: str):
        url = furl(database_url)
        if not url.scheme == 'mongodb':
            raise NotImplementedError(f'Not supported scheme {url.scheme}.')

        self.db = MongoClient(database_url).brain_computer_interface

    def save(self, topic: str, data: bytes) -> None:
        """
        Save the data in the relevant collection in the db.

        :param topic: The topic of the given data.
        :param data: The data to save.
        """
        data = deserialize(data)
        user = data.pop(USER)
        user_id = user.pop(USER_ID)
        timestamp = data.pop(TIMESTAMP)
        self.db.users.update_one({USER_ID: user_id}, {'$set': {**user}}, upsert=True)
        self.db.snapshots.update_one({USER_ID: user_id, TIMESTAMP: timestamp},
                                     {'$set': {topic: data}}, upsert=True)
