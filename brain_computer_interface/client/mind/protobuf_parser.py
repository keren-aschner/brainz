import gzip
import struct

from .mind_pb2 import User, Snapshot
from .parser import Parser


class ProtobufParser(Parser):
    def parse_user(self, stream):
        user = User()
        user.ParseFromString(self._read(stream))
        return user

    def parse_snapshot(self, stream):
        snapshot = Snapshot()
        snapshot.ParseFromString(self._read(stream))
        return snapshot

    @classmethod
    def open(cls, *args, **kwargs):
        return gzip.open(*args, **kwargs)

    @classmethod
    def _read(cls, stream):
        size = struct.unpack('I', stream.read(4))[0]
        return stream.read(size)
