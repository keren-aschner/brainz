import importlib
import inspect
import logging
from pathlib import Path

from flask import Flask, request
from flask_restful import Resource, Api

from .context import Context

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


class Config(Resource):
    def get(self):
        logger.info('Sending config specification.')
        return {'config': list(Server.fields)}


class Snapshot(Resource):
    def post(self):
        data = request.get_json()
        user = data['user']
        logger.debug(f'Got user {user}')
        snapshot = data['snapshot']
        logger.info('Got snapshot.')
        Server.process(user, snapshot)
        return {}, 201


def run_server(address, data):
    Server.data_dir = data
    Server.load_modules('brain_computer_interface/server/processors')

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Config, '/config')
    api.add_resource(Snapshot, '/snapshot')

    host, port = address
    app.run(host=host, port=port)


class Server:
    fields = set()
    processors = []
    data_dir = ''

    @classmethod
    def process(cls, user, snapshot):
        context = Context(cls.data_dir, user, snapshot)
        for process in cls.processors:
            try:
                process(context, snapshot)
            except Exception:
                logger.exception(f'Exception on processor {process.__name__}')
        logger.info('Processed snapshot.')

    @classmethod
    def load_modules(cls, root):
        root = Path(root).absolute()
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            logger.debug(f'importing brain_computer_interface.server.{root.name}.{path.stem}')
            module = importlib.import_module(f'.server.{root.name}.{path.stem}', package='brain_computer_interface')
            cls.add_processors(module)
        logger.info('done loading modules')

    @classmethod
    def add_processors(cls, module):
        for name, processor in inspect.getmembers(module, is_processor):
            logger.debug(f'adding processor "{name}"')
            cls.fields.update(processor.fields)
            if inspect.isclass(processor):
                cls.processors.append(processor().process)
            else:
                cls.processors.append(processor)


def is_processor(object):
    if inspect.isclass(object):
        return object.__name__.endswith('Processor') and 'process' in object.__dict__ and 'fields' in object.__dict__
    if inspect.isfunction(object):
        return object.__name__.startswith('process') and 'fields' in object.__dict__
    return False
