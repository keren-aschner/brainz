import click
from requests import get

from . import version


@click.group()
@click.version_option(version)
def cli():
    pass


@cli.command('get-users')
@click.option('-h', '--host', default='127.0.0.1', help='The host of the api. Default is 127.0.0.1.')
@click.option('-p', '--port', default=5000, help='The port of the api. Default is 5000.')
def get_users(host, port):
    """
    Return the user ids and names from the api.
   """
    return get(f'http://{host}:{port}/users').json()


@cli.command('get-user')
@click.option('-h', '--host', default='127.0.0.1', help='The host of the api. Default is 127.0.0.1.')
@click.option('-p', '--port', default=5000, help='The port of the api. Default is 5000.')
@click.argument('user_id')
def get_user(host, port, user_id):
    """
     Return the details of the user with USER_ID.
    """
    return get(f'http://{host}:{port}/users/{user_id}').json()


@cli.command('get-snapshots')
@click.option('-h', '--host', default='127.0.0.1', help='The host of the api. Default is 127.0.0.1.')
@click.option('-p', '--port', default=5000, help='The port of the api. Default is 5000.')
@click.argument('user_id')
def get_snapshots(host, port, user_id):
    """
     Return the snapshot ids and timestamps for user USER_ID.
    """
    return get(f'http://{host}:{port}/users/{user_id}/snapshots').json()


@cli.command('get-snapshot')
@click.option('-h', '--host', default='127.0.0.1', help='The host of the api. Default is 127.0.0.1.')
@click.option('-p', '--port', default=5000, help='The port of the api. Default is 5000.')
@click.argument('user_id')
@click.argument('snapshot_id')
def get_snapshot(host, port, user_id, snapshot_id):
    """
     Return the details of snapshot SNAPSHOT_ID of user USER_ID.
    """
    return get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}').json()


@cli.command('get-result')
@click.option('-h', '--host', default='127.0.0.1', help='The host of the api. Default is 127.0.0.1.')
@click.option('-p', '--port', default=5000, help='The port of the api. Default is 5000.')
@click.option('-s', '--save', default=None, help='Path to saving the result data.', type=click.File('wb'))
@click.argument('user_id')
@click.argument('snapshot_id')
@click.argument('result')
def get_result(host, port, save, user_id, snapshot_id, result):
    """
    Return the RESULT of snapshot SNAPSHOT_ID of user USER_ID.
    """
    if save is not None:
        save.write(get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}/data'))

    return get(f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}').json()


if __name__ == '__main__':
    cli(prog_name='brain_computer_interface.cli')
