import base64
from abc import ABC
from typing import BinaryIO, Union, Any

from construct import (
    Struct,
    Int32ul,
    Int64ul,
    PascalString,
    PaddedString,
    Float64l,
    Array,
    this,
    Byte,
    Float32l,
    StreamError,
    Adapter,
    Enum,
    Container,
)

from .sample_parser import SampleParser, ParsingError


class BinaryParser(SampleParser):
    """
    A parser for the binary format.
    """

    def parse_user(self, stream: BinaryIO) -> dict:
        """
        Parse a user from the given stream using the binary protocol.
        Return the parsed object as a dict.
        """
        user = Struct(
            user_id=StrAdapter(Int64ul),
            username=PascalString(Int32ul, "utf-8"),
            birthday=Int32ul,
            gender=Enum(PaddedString(1, "utf-8"), MALE="m", FEMALE="f", OTHER="o"),
        )
        return container_to_dict(user.parse_stream(stream))

    def parse_snapshot(self, stream: BinaryIO) -> dict:
        """
        Parse a snapshot from the given stream using the binary protocol.
        Return the parsed object as a dict.
        """
        translation = Struct(x=Float64l, y=Float64l, z=Float64l)
        rotation = Struct(x=Float64l, y=Float64l, z=Float64l, w=Float64l)
        pose = Struct(translation=translation, rotation=rotation)
        color_image = Struct(
            height=Int32ul, width=Int32ul, data=ColorImageAdapter(Array(this.height * this.width, Byte[3]))
        )
        depth_image = Struct(height=Int32ul, width=Int32ul, data=Array(this.height * this.width, Float32l))
        feelings = Struct(hunger=Float32l, thirst=Float32l, exhaustion=Float32l, happiness=Float32l)
        snapshot = Struct(
            timestamp=StrAdapter(Int64ul),
            pose=pose,
            color_image=color_image,
            depth_image=depth_image,
            feelings=feelings,
        )

        try:
            return container_to_dict(snapshot.parse_stream(stream))
        except StreamError:
            raise ParsingError


class ColorImageAdapter(Adapter, ABC):
    """
    An adapter for decoding color image array to an RGB map.
    """

    def _decode(self, obj, context, path):
        return b"".join(map(lambda bgr: bytes(bgr[::-1]), obj))


class StrAdapter(Adapter, ABC):
    """
    An adapter for decoding objects as strings.
    """

    def _decode(self, obj, context, path):
        return str(obj)


def container_to_dict(container: Union[Container, Any]) -> dict:
    """
    Transform a container to a dictionary using recursive calls to this method.

    :param container: The container to transform.
    :return: The transformed dictionary.
    """
    if not isinstance(container, Container):
        return container

    dic = {}
    for key in container.keys():
        dic[key] = container_to_dict(container[key])

    dic.pop("_io", None)
    return dic
