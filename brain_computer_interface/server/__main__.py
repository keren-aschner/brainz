import click

from . import run_server, version


@click.group()
@click.version_option(version)
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', help='The host to listen on.')
@click.option('-p', '--port', default=8000, help='The port to listen on.')
@click.argument('message_queue_url')
def run(host, port, message_queue_url):
    """
    Listen on `host`:`port` and pass received messages to the given message_queue.
    """
    run_server(host, port, publish(message_queue_url))


def publish(url):
    # TODO
    pass


if __name__ == '__main__':
    cli(prog_name='brain_computer_interface.server')
