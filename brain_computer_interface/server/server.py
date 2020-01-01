import logging

from flask import Flask, request
from flask_restful import Resource, Api

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
    fields = set()

    def get(self):
        logger.info('Sending config specification.')
        return {'config': list(self.fields)}

    @classmethod
    def processor(cls, *fields):
        def decorator(cl):
            cls.fields.update(fields)
            Server.processors.append(cl)
            return cl

        return decorator


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
    processors = []
    data_dir = ''

    @classmethod
    def process(cls, user, snapshot):
        for processor in cls.processors:
            processor(cls.data_dir, user).process(snapshot)
        logger.info('Processed snapshot.')
