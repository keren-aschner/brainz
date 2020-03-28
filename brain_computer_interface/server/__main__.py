from typing import Callable

import click
import pika
from furl import furl

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
    run_server(host, port, publish_to_url(message_queue_url))


def publish_to_url(url) -> Callable[[str], None]:
    """
    Return a publish method according to the scheme given in the url.

    :param url: The url to publish to.
    :return: The required publish method.
    """
    url = furl(url)
    if url.scheme == 'rabbitmq':
        return publish_to_rmq(url.host, url.port)
    else:
        raise NotImplementedError(f'Not supported scheme {url.scheme}')


def publish_to_rmq(host: str, port: int) -> Callable[[str], None]:
    """
    Return a publish method to RabbitMQ.

    :param host: The RabbitMQ host.
    :param port: The RabbitMQ port.
    :return: The created publish method.
    """

    def publish(message: str) -> None:
        """
        Publish a message to the 'snapshots' exchange on RabbitMQ.

        :param message: The message to publish.
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        channel = connection.channel()
        channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
        channel.basic_publish(exchange='snapshots', routing_key='', body=message)
        connection.close()

    return publish


# TODO: each consumer
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
# channel = connection.channel()
# channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
# queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
# channel.queue_bind(exchange='snapshots', queue=queue_name)
#
# def callback(ch, method, properties, message):
#     print(" [x] %r" % message)
#
# channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
# channel.start_consuming()


if __name__ == '__main__':
    cli(prog_name='brain_computer_interface.server')
