import logging

import requests

from .reader import Reader

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def upload_sample(address, path):
    reader = Reader(path)
    logger.info('Initialized reader, starting uploading snapshots.')
    for snapshot in reader:
        upload_snapshot(address, reader.user, snapshot)
    logger.info('Uploaded all snapshots.')


def upload_snapshot(address, user, snapshot):
    config = requests.get(f'http://{address}/config').json()['config']
    logger.debug('Got config.')
    snapshot = {field: snapshot[field] for field in config}
    requests.post(f'http://{address}/snapshot', json={'user': user, 'snapshot': snapshot})
    logger.info('Uploaded snapshot.')
