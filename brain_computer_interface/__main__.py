import os
import sys
import traceback

import click

import brain_computer_interface


# TODO use configurations
# TODO color logs?

class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.version_option(brain_computer_interface.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command()
@click.option('--address', required=True, help='The address to upload the snapshots to.')
@click.option('--sample', required=True, help='the sample file path.')
@click.option('--binary', is_flag=True, help='Use binary sample.')
def upload_sample(address, sample, binary):
    brain_computer_interface.upload_sample(address, sample, not binary)


@main.command()
@click.option('--address', required=True, help='The address to run the server on.')
@click.option('--data', required=True, help='The data directory')
def run_server(address, data):
    host, port = address.split(':')
    brain_computer_interface.run_server((host, int(port)), data)


@main.command()
@click.option('--address', required=True, help='The address of the webserver.')
@click.option('--data-dir', required=True, help='The data dir to expose on the website.')
def run_webserver(address, data_dir):
    host, port = address.split(':')
    brain_computer_interface.run_webserver((host, int(port)), data_dir)


if __name__ == '__main__':
    try:
        main(prog_name='brain_computer_interface', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
