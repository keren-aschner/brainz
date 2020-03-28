import logging
from typing import Union, List

import requests

from .reader import Reader
from ..protocol.client_server import serialize

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def upload_sample(host: str, port: Union[str, int], path: str, protobuf: bool = True) -> None:
    """
    Upload the given sample's data to the server.

    :param host: The server's host.
    :param port: The server's port.
    :param path: The path to the sample file.
    :param protobuf: Whether to use a protobuf or binary format.
    """
    reader = Reader(path, protobuf)
    logger.info('Initialized reader, starting uploading snapshots')
    config = requests.get(f'http://{host}:{port}/config').json()['config']
    logger.debug('Got config from server')
    for snapshot in reader:
        upload_snapshot(host, port, reader.user, snapshot, config)
    logger.info('Uploaded all snapshots')


def upload_snapshot(host: str, port: Union[str, int], user: dict, snapshot: dict, config: List[str]) -> None:
    """
    Upload the given snapshot to the server.

    :param host: The server's host.
    :param port: The server's port.
    :param user: The user of the given snapshot.
    :param snapshot: The snapshot to upload.
    :param config: The configurations from the server with the required fields.
    """
    try:
        snapshot = {field: snapshot[field] for field in config}
        requests.post(f'http://{host}:{port}/snapshot', json={'message': serialize(user, snapshot)})
        logger.debug('Uploaded snapshot')
    except Exception:
        logger.exception("Error during uploading snapshot")
