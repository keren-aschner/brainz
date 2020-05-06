import logging

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from furl import furl
from pymongo import MongoClient
from pymongo.database import Database

from .resources import Users, User, Snapshots, Feelings, Snapshot, Result, ResultData

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%d-%m-%y %H:%M:%S"
)

logger = logging.getLogger(__name__)


def run_api_server(host: str, port: int, database_url: str):
    """
    Run the server and call the `publish` method on received messages.

    :param host: The server's host.
    :param port: The server's port.
    :param database_url: The db to use for reading.
    """
    url = furl(database_url)
    if not url.scheme == "mongodb":
        raise NotImplementedError(f"Not supported scheme {url.scheme}.")

    db = MongoClient(database_url).brainz
    app = get_app(db)
    app.run(host=host, port=port)


def get_app(db: Database):
    app = Flask(__name__)
    CORS(app)

    api = Api(app)
    api.add_resource(Users, "/users", resource_class_args=(db,))
    api.add_resource(User, "/users/<int:user_id>", resource_class_args=(db,))
    api.add_resource(Snapshots, "/users/<int:user_id>/snapshots", resource_class_args=(db,))
    api.add_resource(Feelings, "/users/<int:user_id>/feelings", resource_class_args=(db,))
    api.add_resource(Snapshot, "/users/<int:user_id>/snapshots/<string:snapshot_id>", resource_class_args=(db,))
    api.add_resource(
        Result, "/users/<int:user_id>/snapshots/<string:snapshot_id>/<string:result_name>", resource_class_args=(db,)
    )
    api.add_resource(
        ResultData,
        "/users/<int:user_id>/snapshots/<string:snapshot_id>/<string:result_name>/data",
        resource_class_args=(db,),
    )

    return app
