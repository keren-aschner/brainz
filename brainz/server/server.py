import logging
from typing import Callable, List, Dict

from flask import Flask, request
from flask_restful import Resource, Api

from ..parsers import get_all_fields
from ..protocol.client_server import deserialize
from ..protocol.server_parsers import serialize

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def run_server(host: str, port: int, publish: Callable[[bytes], None]) -> None:
    """
    Run the server and call the `publish` method on received messages.

    :param host: The server's host.
    :param port: The server's port.
    :param publish: The publish method to use.
    """
    app = get_app(publish)
    app.run(host=host, port=port)


class Config(Resource):
    """
     Return the server's required fields using GET method.
    """

    def __init__(self, parsers_fields):
        self.fields = parsers_fields

    def get(self) -> Dict[str, List[str]]:
        logger.info('Sending config specification')
        return {'config': self.fields}


class Snapshot(Resource):
    """
    Accept a message using POST method and publish it.
    """

    def __init__(self, publish_method):
        self.publish = publish_method

    def post(self):
        client_server_serialized = request.get_data()
        server_parsers_serialized = serialize(*deserialize(client_server_serialized))
        self.publish(server_parsers_serialized)
        logger.info('Published message')
        return {}, 200


def get_app(publish: Callable[[bytes], None]) -> Flask:
    """
    Get the server's flask app.
    """
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Config, '/config', resource_class_args=(get_all_fields(),))
    api.add_resource(Snapshot, '/snapshot', resource_class_args=(publish,))
    return app
