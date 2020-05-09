import importlib
import inspect
from pathlib import Path
from typing import Any, List

from .base_parser import BaseParser
from .parser import Parser
from ..protocol.fields import TIMESTAMP

version = "1.0.0"


def parse(parser_name: str, data: bytes) -> str:
    """
    Parse the data using the correct parser.

    :param parser_name: The name of the parser to use.
    :param data: The data to parse.
    :return: The parsed data.
    """
    return get_parser(parser_name).parse(data)


def get_parser(parser_name: str) -> Parser:
    """
    Get the relevant parser according to parser_name.
    """
    return next(parser for parser in get_parsers() if parser.name == parser_name)


def get_parsers() -> List[Parser]:
    """
    Get all the parsers from brainz.parser package
    """
    parsers = []
    root = Path("brainz/parsers/parsers").absolute()
    for path in root.iterdir():
        if path.name.startswith("_") or not path.suffix == ".py":
            continue
        module = importlib.import_module(f".{path.stem}", package="brainz.parsers.parsers")
        parsers.extend([Parser(parser) for _, parser in inspect.getmembers(module, is_parser)])

    return parsers


def get_all_fields() -> List[str]:
    fields = {field for parser in get_parsers() for field in parser.fields}
    fields.add(TIMESTAMP)
    return list(fields)


def is_parser(obj: Any) -> bool:
    """
    Check whether a given object is a parser.

    :param obj: The object to check.
    :return: True if it is a parser, False otherwise.
    """
    if inspect.isclass(obj):
        return obj.__name__.endswith("Parser") and hasattr(obj, "parse") and hasattr(obj, "fields")
    if inspect.isfunction(obj):
        return obj.__name__.startswith("parse") and hasattr(obj, "fields")
    return False
