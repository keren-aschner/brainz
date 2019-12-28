import logging

from .reader import Reader
from ..thought_layer import Hello, Config, Snapshot
from ..utils import Connection

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def upload_sample(address, path):
    reader = Reader(path)
    logger.info('Initialized reader, starting uploading snapshots.')
    for snapshot in reader:
        upload_snapshot(address, reader.user, snapshot)
    logger.info('Uploaded all snapshots')


def upload_snapshot(address, user, snapshot):
    with Connection.connect(address) as connection:
        connection.send(Hello(**user).serialize())
        config = Config.deserialize(connection.receive())
        snapshot = create_snapshot_message(config, snapshot)
        connection.send(snapshot.serialize())

    logger.info('Uploaded snapshot')


def create_snapshot_message(config, snapshot):
    fields_data = {}
    for field in config.fields:
        fields_data[field] = snapshot[field]
    return Snapshot(**fields_data)
