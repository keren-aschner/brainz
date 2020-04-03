import click

from . import version, run_api_server


@click.group()
@click.version_option(version)
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='0.0.0.0', help='The host to listen on. Default is 0.0.0.0.')
@click.option('-p', '--port', default=5000, help='The port to listen on. Default is 5000.')
@click.option('-d', '--database', default='mongodb://mongodb:27017/',
              help='URL to the database to use. Default is mongodb://mongodb:27017/.')
def run(host, port, database):
    """
    Run api-server on `host`:`port` and server the data from the `database`.
    """
    run_api_server(host, port, database)


if __name__ == '__main__':
    cli(prog_name='brainz.api')
