import os
import sys
import traceback

import click

import brain_computer_interface


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
@click.option('--address', help='The address to upload the thought to.')
@click.option('--user', help='The use id.')
@click.option('--thought', help='The thought to upload.')
def upload_thought(address, user, thought):
    brain_computer_interface.upload_thought(address, user, thought)


@main.command()
@click.option('--address', help='The address to run the server on.')
@click.option('--data', help='The data directory')
def run_server(address, data):
    brain_computer_interface.run_server(address, data)


@main.command()
@click.option('--address', help='The address of the webserver.')
@click.option('--data-dir', help='The data dir to expose on the website.')
def run_webserver(address, data_dir):
    brain_computer_interface.run_webserver(address, data_dir)


if __name__ == '__main__':
    try:
        main(prog_name='brain_computer_interface', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
