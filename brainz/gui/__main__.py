import click

from . import version, run_server


@click.group()
@click.version_option(version)
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='0.0.0.0', help='The host to listen on. Default is 0.0.0.0.')
@click.option('-p', '--port', default=8080, help='The port to listen on. Default is 8080.')
@click.option('-H', '--api-host', default='127.0.0.1', help='The ip of the api host. Default is 127.0.0.1.')
@click.option('-P', '--api-port', default=5000, help='The port of the api host. Default is 5000.')
def run(host, port, api_host, api_port):
    """
    Run gui-server on `host`:`port` and visualize the data from `api-host`:`api-port`.
    """
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    cli(prog_name='brainz.gui')
