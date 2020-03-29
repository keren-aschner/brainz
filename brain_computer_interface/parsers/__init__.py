from typing import Callable

version = '0.1.0'


def get_parser(parser_name: str) -> Callable[[bytes], bytes]:
    """
    Get the relevant parser according to parser_name.
    """
    pass


def parse(parser_name: str, data: bytes) -> bytes:
    """
    Parse the data using the correct parser.

    :param parser_name: The name of the parser to use.
    :param data: The data to parse.
    :return: The parsed data.
    """
    parser = get_parser(parser_name)
    return parser(data)
