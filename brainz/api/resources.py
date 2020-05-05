import io
import logging

from bson import ObjectId
from flask import send_file
from flask_restful import Resource, abort
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database

from ..protocol.fields import USER_ID, USERNAME, TIMESTAMP, COLOR_IMAGE, DEPTH_IMAGE, FEELINGS

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%d-%m-%y %H:%M:%S"
)

logger = logging.getLogger(__name__)

ID = "_id"
SNAPSHOT_ID = "snapshot_id"


class ApiResource(Resource):
    def __init__(self, db: Database):
        self.users: Collection = db.users
        self.snapshots: Collection = db.snapshots


class Users(ApiResource):
    def get(self):
        """
         Return the user ids and names from the db.
        """
        return list(self.users.find({}, {USER_ID: 1, USERNAME: 1, ID: 0}))


class User(ApiResource):
    def get(self, user_id):
        """
         Return the details of the specific user.
        """
        return self.users.find_one({USER_ID: user_id}, {ID: 0})


class Snapshots(ApiResource):
    def get(self, user_id):
        """
         Return the snapshot ids and timestamps for a specific user.
        """
        return [
            {SNAPSHOT_ID: str(snapshot[ID]), TIMESTAMP: snapshot[TIMESTAMP]}
            for snapshot in self.snapshots.find({USER_ID: user_id}).sort(TIMESTAMP, ASCENDING)
        ]


class Feelings(ApiResource):
    def get(self, user_id):
        """
        Return the user's feelings over time.
        """
        return [
            {SNAPSHOT_ID: str(snapshot[ID]), TIMESTAMP: snapshot[TIMESTAMP], FEELINGS: snapshot[FEELINGS]}
            for snapshot in self.snapshots.find({USER_ID: user_id})
        ]


class Snapshot(ApiResource):
    def get(self, user_id, snapshot_id):
        """
         Return the details of a specific snapshot.
        """
        snapshot = self.snapshots.find_one({USER_ID: user_id, ID: ObjectId(snapshot_id)}, {USER_ID: 0, ID: 0})
        timestamp = snapshot.pop(TIMESTAMP)
        return {SNAPSHOT_ID: snapshot_id, TIMESTAMP: timestamp, "fields": list(snapshot.keys())}


class Result(ApiResource):
    def get(self, user_id, snapshot_id, result_name):
        """
        Return the specified snapshot's result.
        """
        snapshot = self.snapshots.find_one({USER_ID: user_id, ID: ObjectId(snapshot_id)})
        return snapshot[result_name]


class ResultData(ApiResource):
    representations = {"image/jpeg": lambda data, code, headers: send_file(io.BytesIO(data), mimetype="image/jpeg")}

    def get(self, user_id, snapshot_id, result_name):
        """
        Return the specified snapshot's result data.
        """
        if result_name not in [COLOR_IMAGE, DEPTH_IMAGE]:
            abort(404)

        snapshot = self.snapshots.find_one({USER_ID: user_id, ID: ObjectId(snapshot_id)})
        with open(snapshot[result_name]["path"], "rb") as f:
            return f.read()
