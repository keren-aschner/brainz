import gzip
import struct
from typing import BinaryIO
from typing.io import IO

from google.protobuf.json_format import MessageToDict

from .parser import Parser, ParsingError
from ...protocol.mind_pb2 import User, Snapshot


class ProtobufParser(Parser):
    """
    A parser for the protobuf format.
    """

    def parse_user(self, stream: BinaryIO) -> dict:
        """
        Parse a user from the given stream using the protobuf protocol.
        Return the parsed User object as a dict.
        """
        user = User()
        user.ParseFromString(self._read(stream))
        return MessageToDict(user, including_default_value_fields=True, preserving_proto_field_name=True)

    def parse_snapshot(self, stream: BinaryIO) -> dict:
        """
        Parse a snapshot from the given stream using the protobuf protocol.
        Return the parsed Snapshot object as a dict.
        """
        try:
            snapshot = Snapshot()
            snapshot.ParseFromString(self._read(stream))
            return MessageToDict(snapshot, including_default_value_fields=True, preserving_proto_field_name=True)
        except Exception as e:
            raise ParsingError(e)

    @classmethod
    def open(cls, *args, **kwargs) -> IO:
        """
        Open a gzip-compressed file in binary or text mode.
        """
        return gzip.open(*args, **kwargs)

    @classmethod
    def _read(cls, stream: BinaryIO) -> bytes:
        """
        Get size to read from the first 4 bytes, and then read `size` bytes.
        """
        size = struct.unpack('I', stream.read(4))[0]
        return stream.read(size)
