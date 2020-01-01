import gzip
import struct

from .mind_pb2 import User, Snapshot
from .parser import Parser, ParsingError
from google.protobuf.json_format import MessageToDict


class ProtobufParser(Parser):
    def parse_user(self, stream):
        user = User()
        user.ParseFromString(self._read(stream))
        return MessageToDict(user, including_default_value_fields=True, preserving_proto_field_name=True)

    def parse_snapshot(self, stream):
        try:
            snapshot = Snapshot()
            snapshot.ParseFromString(self._read(stream))
            return MessageToDict(snapshot, including_default_value_fields=True, preserving_proto_field_name=True)
        except Exception as e:
            raise ParsingError(e)

    @classmethod
    def open(cls, *args, **kwargs):
        return gzip.open(*args, **kwargs)

    @classmethod
    def _read(cls, stream):
        size = struct.unpack('I', stream.read(4))[0]
        return stream.read(size)
