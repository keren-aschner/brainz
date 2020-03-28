import importlib
import inspect
import logging
from pathlib import Path
from typing import Callable, List, Dict, Any

from flask import Flask, request
from flask_restful import Resource, Api

from .context import Context
from ..protocol.client_server import deserialize
from ..protocol.server_parsers import serialize

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def run_server(host: str, port: int, publish: Callable[[str], None]) -> None:
    """
    Run the server and call the `publish` method on received messages.

    :param host: The server's host.
    :param port: The server's port.
    :param publish: The publish method to use.
    """
    Server.load_modules('brain_computer_interface/server/parsers')
    app = get_app(publish)
    app.run(host=host, port=port)


def get_app(publish: Callable[[str], None]) -> Flask:
    """
    Create an flask app, that uses the `publish` method on received messages.
    :param publish: The publish method to use.
    :return: The created app.
    """

    class Config(Resource):
        """
         Return the server's required fields using GET method.
        """

        def get(self) -> Dict[str, List[str]]:
            logger.info('Sending config specification')
            return {'config': list(Server.fields)}

    class Snapshot(Resource):
        """
        Accept a message using POST method and publish it.
        """

        def post(self):
            message = request.get_json()['message']
            publish(prepare_to_publish(message))
            logger.info('Published message')
            return {}, 201

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Config, '/config')
    api.add_resource(Snapshot, '/snapshot')
    return app


def prepare_to_publish(message: bytes) -> str:
    """
    Deserialize the message using the client-server protocol and then serialize it using the server-parsers protocol.

    :param message: The message to prepare.
    :return: The message to be published.
    """
    return serialize(*deserialize(message))


class Server:
    """
    Holds the fields required by the parsers.
    """
    fields = {Context.TIMESTAMP}

    @classmethod
    def load_modules(cls, root: str) -> None:
        """
        Load all the modules in the given package and add the parsers in it.

        :param root: The root path of the package to load.
        """
        root = Path(root).absolute()
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            logger.debug(f'loading brain_computer_interface.server.{root.name}.{path.stem}')
            module = importlib.import_module(f'.server.{root.name}.{path.stem}', package='brain_computer_interface')
            cls.add_parsers(module)
        logger.info('done loading modules')

    @classmethod
    def add_parsers(cls, module) -> None:
        """
        Add fields for parsers from the given module.

        :param module: The module to use.
        """
        for name, parser in inspect.getmembers(module, is_parser):
            logger.debug(f'adding parser "{name}"')
            if hasattr(object, 'fields'):
                cls.fields.update(parser.fields)
            else:
                cls.fields.add(parser.field)


def is_parser(obj: Any) -> bool:
    """
    Check whether a given object is a parser.

    :param obj: The object to check.
    :return: True if it is a parser, False otherwise.
    """
    if inspect.isclass(obj):
        return obj.__name__.endswith('Parser') and hasattr(obj, 'parse') and has_fields(obj)
    if inspect.isfunction(obj):
        return obj.__name__.startswith('parse') and has_fields(obj)
    return False


def has_fields(obj: Any) -> bool:
    """
    Check whether a given object has a `field` or `fields` attribute.

    :param obj: The object to check.
    :return: True if it is a a field ot fields attribute, False otherwise.
    """
    return hasattr(obj, 'field') or hasattr(obj, 'fields')
