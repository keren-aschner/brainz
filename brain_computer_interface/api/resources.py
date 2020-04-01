from datetime import datetime

from flask_restful import Resource, abort

from ..protocol.fields import USER_ID, USERNAME, TIMESTAMP, COLOR_IMAGE, DEPTH_IMAGE


class ApiResource(Resource):
    def __init__(self, db):
        self.db = db


class Users(ApiResource):
    def get(self):
        """
         Return the user ids and names from the db.
        """
        return [{user[USER_ID]: user[USERNAME]} for user in self.db.users.find()]


class User(ApiResource):
    def get(self, user_id):
        """
         Return the details of the specific user.
        """
        return self.db.users.find_one({USER_ID: user_id})


class Snapshots(ApiResource):
    def get(self, user_id):
        """
         Return the snapshot ids and timestamps for a specific user.
        """
        return [{snapshot[TIMESTAMP]: datetime.utcfromtimestamp(snapshot[TIMESTAMP])} for snapshot in
                self.db.snapshots.find({USER_ID: user_id})]


class Snapshot(ApiResource):
    def get(self, user_id, snapshot_id):
        """
         Return the details of a specific snapshot.
        """
        snapshot = self.db.snapshots.find_one({USER_ID: user_id, TIMESTAMP: snapshot_id})
        del snapshot[USER_ID]
        timestamp = snapshot.pop(TIMESTAMP)
        return {'snapshot_id': timestamp, TIMESTAMP: datetime.utcfromtimestamp(timestamp), 'fields': snapshot.keys()}


class Result(ApiResource):
    def get(self, user_id, snapshot_id, result_name):
        """
        Return the specified snapshot's result.
        """
        snapshot = self.db.snapshots.find_one({USER_ID: user_id, TIMESTAMP: snapshot_id})
        return snapshot[result_name]


class ResultData(ApiResource):
    def get(self, user_id, snapshot_id, result_name):
        """
        Return the specified snapshot's result data.
        """
        if result_name not in [COLOR_IMAGE, DEPTH_IMAGE]:
            abort(404)

        snapshot = self.db.snapshots.find_one({USER_ID: user_id, TIMESTAMP: snapshot_id})
        with open(snapshot[result_name]['path'], 'rb') as f:
            data = f.read()
        return data, 200, {'Content-Type': 'image/jpeg'}
