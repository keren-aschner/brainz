import click
import pika
from furl import furl
from pika.channel import Channel
from pika.spec import Basic, BasicProperties

from . import Saver, version
from ..parsers import get_parsers


@click.group()
@click.version_option(version)
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', default='mongodb://mongodb:27017/',
              help='URL to the database to use. Default is mongodb://mongodb:27017/.')
@click.argument('topic')
@click.argument('data_path', type=click.File('rb'))
def save(database, topic, data):
    """
    Save data from DATA_PATH to TOPIC in the given db.
    """
    saver = Saver(database)
    saver.save(topic, data.read())


@cli.command('run-saver')
@click.argument('database_url')
@click.argument('message_queue_url')
def run_saver(database_url, message_queue_url):
    """
    Save data from MESSAGE_QUEUE_URL to DATABASE_URL.
    """
    consume(message_queue_url, database_url)


def consume(mq_url: str, db_url: str) -> None:
    """
    Consume messages from the message queue on the given url.

    :param mq_url: The url of the message queue.
    :param db_url: The db for saving the consumed data.
    """
    mq_url = furl(mq_url)
    if mq_url.scheme == 'rabbitmq':
        consume_rmq(mq_url.host, mq_url.port, db_url)
    else:
        raise NotImplementedError(f'Not supported scheme {mq_url.scheme}')


def consume_rmq(host: str, port: int, db_url: str):
    """
    Consume messages from the `parsers_data` exchange on the given RabbitMQ host.

    :param host: The RabbitMQ host.
    :param port: The RabbitMQ port.
    :param db_url: The db for saving the consumed data.
    """
    saver = Saver(db_url)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()

    channel.exchange_declare(exchange='parsers_data', exchange_type='topic')
    queue_name = channel.queue_declare('', exclusive=True).method.queue

    for parser in get_parsers():
        channel.queue_bind(exchange='parsers_data', queue=queue_name, routing_key=parser.name) # TODO: routing key # ?

    def callback(ch: Channel, method: Basic.Deliver, properties: BasicProperties, message: bytes) -> None:
        saver.save(method.routing_key, message)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    cli(prog_name='brainz.saver')
