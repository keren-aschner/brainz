import inspect
import re
from typing import Callable, Union, List

from .base_parser import BaseParser


class Parser:
    def __init__(self, parser: Union[Callable[[], BaseParser], Callable[[bytes], bytes]]):
        self.name = get_name(parser)
        self.fields = get_fields(parser)
        self.parse = get_method(parser)


def get_name(parser: Union[Callable[[], BaseParser], Callable[[bytes], bytes]]) -> str:
    """
    Get the name of a parser.
    If it's a method, remove the `parse_` from the beginning of the name.
    If it's a class, turn it from CamelCase to snake_case and remove the `Parser` from the end of the name.
    """
    name = parser.__name__
    if inspect.isclass(parser):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", re.search("(.*)Parser", name).group(1)).lower()
    else:
        return re.search("parse_(.*)", name).group(1)


def get_fields(parser: Union[Callable[[], BaseParser], Callable[[str], str]]) -> List[str]:
    """
    Get the parser's required fields.
    """
    if inspect.isclass(parser):
        return parser().fields
    else:
        return parser.fields


def get_method(parser: Union[Callable[[], BaseParser], Callable[[bytes], bytes]]) -> Callable[[bytes], bytes]:
    """
    Get the parsing method.
    If it's a method, return itself.
    If it's a class, return it's parse method.
    """
    if inspect.isclass(parser):
        return parser().parse
    else:
        return parser
