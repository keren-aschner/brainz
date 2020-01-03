import inspect
import logging

from flask import Flask, request
from flask_restful import Resource, Api

from .context import Context

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

TIMESTAMP = 'timestamp'
POSE = 'pose'
COLOR_IMAGE = 'color_image'
DEPTH_IMAGE = 'depth_image'
FEELINGS = 'feelings'


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


api.add_resource(Config, '/config')
api.add_resource(Snapshot, '/snapshot')


def run_server(address, data):
    Server.data_dir = data
    host, port = address
    app.run(host=host, port=port)


class Server:
    fields = set()
    processors = []
    data_dir = ''

    @classmethod
    def process(cls, user, snapshot):
        context = Context(cls.data_dir, user)
        for process in cls.processors:
            process(context, snapshot)
        logger.info('Processed snapshot.')

    @classmethod
    def processor(cls, *fields):
        cls.fields.update(fields)

        def decorator(f):
            if inspect.isclass(f):
                obj = f()
                cls.processors.append(obj.process)
            else:
                cls.processors.append(f)
            return f

        return decorator
