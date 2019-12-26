from .thought_layer import Hello, Config, Snapshot
from .utils import Connection, Reader


def upload_sample(address, path):
    reader = Reader(path)
    for snapshot in reader:
        upload_snapshot(address, reader.user, snapshot)


def upload_snapshot(address, user, snapshot):
    with Connection.connect(address) as connection:
        connection.send(Hello(**user).serialize())
        config = Config.deserialize(connection.receive())
        snapshot = create_snapshot_message(config, snapshot)
        connection.send(snapshot.serialize())

    print('done')


def create_snapshot_message(config, snapshot):
    fields_data = {}
    for field in config.fields:
        fields_data[field] = snapshot[field]
    return Snapshot(**fields_data)
