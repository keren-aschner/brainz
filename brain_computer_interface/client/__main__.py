import click

from . import upload_sample, version


@click.group('client')
@click.version_option(version)
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', default='127.0.0.1', help='The host to upload the snapshots to.')
@click.option('-p', '--port', default=8000, help='The port of the host to upload the snapshots to.')
@click.argument('sample')
@click.option('--binary', is_flag=True, help='Use binary sample.')
def upload_sample(host, port, sample, binary):
    """
    Upload the given sample to the server on `host`:`port`.
    """
    upload_sample(host, port, sample, not binary)


if __name__ == '__main__':
    cli(prog_name='brain_computer_interface.client')
