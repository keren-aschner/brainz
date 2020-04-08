import io
import logging

from bson import ObjectId
from flask import send_file
from flask_restful import Resource, abort

from ..protocol.fields import USER_ID, USERNAME, TIMESTAMP, COLOR_IMAGE, DEPTH_IMAGE, FEELINGS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)

ID = '_id'
SNAPSHOT_ID = 'snapshot_id'


class ApiResource(Resource):
    def __init__(self, db):
        self.db = db


class Users(ApiResource):
    def get(self):
        """
         Return the user ids and names from the db.
        """
        return [{USER_ID: user[USER_ID], USERNAME: user[USERNAME]} for user in self.db.users.find()]


class User(ApiResource):
    def get(self, user_id):
        """
         Return the details of the specific user.
        """
        user = self.db.users.find_one({USER_ID: user_id})
        del user[ID]
        return user


class Snapshots(ApiResource):
    def get(self, user_id):
        """
         Return the snapshot ids and timestamps for a specific user.
        """
        return [{SNAPSHOT_ID: str(snapshot[ID]), TIMESTAMP: snapshot[TIMESTAMP]} for snapshot in
                self.db.snapshots.find({USER_ID: user_id})]


class Feelings(ApiResource):

    def get(self, user_id):
        """
        Return the user's feelings over time.
        """
        return [{TIMESTAMP: snapshot[TIMESTAMP], FEELINGS: snapshot[FEELINGS]} for snapshot in
                self.db.snapshots.find({USER_ID: user_id})]


class Snapshot(ApiResource):
    def get(self, user_id, snapshot_id):
        """
         Return the details of a specific snapshot.
        """
        snapshot = self.db.snapshots.find_one({USER_ID: user_id, ID: ObjectId(snapshot_id)})
        del snapshot[USER_ID]
        del snapshot[ID]
        timestamp = snapshot.pop(TIMESTAMP)
        return {SNAPSHOT_ID: snapshot_id, TIMESTAMP: timestamp, 'fields': list(snapshot.keys())}


class Result(ApiResource):
    def get(self, user_id, snapshot_id, result_name):
        """
        Return the specified snapshot's result.
        """
        snapshot = self.db.snapshots.find_one({USER_ID: user_id, ID: ObjectId(snapshot_id)})
        return snapshot[result_name]


class ResultData(ApiResource):
    representations = {'image/jpeg': lambda data, code, headers: send_file(io.BytesIO(data), mimetype='image/jpeg')}

    def get(self, user_id, snapshot_id, result_name):
        """
        Return the specified snapshot's result data.
        """
        if result_name not in [COLOR_IMAGE, DEPTH_IMAGE]:
            abort(404)

        snapshot = self.db.snapshots.find_one({USER_ID: user_id, ID: ObjectId(snapshot_id)})
        with open(snapshot[result_name]['path'], 'rb') as f:
            return f.read()
