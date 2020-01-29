import logging

import requests

from .reader import Reader

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


# TODO: handle errors

def upload_sample(host, port, path, protobuf=True):
    reader = Reader(path, protobuf)
    logger.info('Initialized reader, starting uploading snapshots.')
    for snapshot in reader:
        upload_snapshot(host, port, reader.user, snapshot)
    logger.info('Uploaded all snapshots.')


def upload_snapshot(host, port, user, snapshot):
    config = requests.get(f'http://{host}:{port}/config').json()['config']
    logger.debug('Got config.')
    snapshot = {field: snapshot[field] for field in config}
    requests.post(f'http://{host}:{port}/snapshot', json={'user': user, 'snapshot': snapshot})
    logger.debug('Uploaded snapshot.')
