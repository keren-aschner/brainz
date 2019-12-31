from abc import ABC
from datetime import datetime

from construct import Struct, Int32ul, Int64ul, PascalString, PaddedString, Float64l, Array, this, Byte, Float32l, \
    StreamError, Adapter

from .parser import Parser, ParsingError


# TODO adjust to new impl

class BinaryParser(Parser):
    def parse_user(self, stream):
        birthday = DateAdapter(Int32ul)
        user = Struct(user_id=Int64ul, username=PascalString(Int32ul, 'utf-8'), birthday=birthday,
                      gender=PaddedString(1, 'utf-8'))
        return user.parse_stream(stream)

    def parse_snapshot(self, stream):
        snapshot_timestamp = DateAdapter(SnapshotTimestampAdapter(Int64ul))
        translation = Struct(x=Float64l, y=Float64l, z=Float64l)
        rotation = Struct(x=Float64l, y=Float64l, z=Float64l, w=Float64l)
        pose = Struct(translation=translation, rotation=rotation)
        color_image = Struct(height=Int32ul, width=Int32ul,
                             image=ColorImageAdapter(Array(this.height * this.width, Byte[3])))
        depth_image = Struct(height=Int32ul, width=Int32ul, image=Array(this.height * this.width, Float32l))
        feelings = Struct(hunger=Float32l, thirst=Float32l, exhaustion=Float32l, happiness=Float32l)
        snapshot = Struct(timestamp=snapshot_timestamp, pose=pose, color_image=color_image, depth_image=depth_image,
                          feelings=feelings)

        try:
            return snapshot.parse_stream(stream)
        except StreamError:
            raise ParsingError


class DateAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return datetime.utcfromtimestamp(obj)


class SnapshotTimestampAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return obj / 1000


class ColorImageAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return list(map(lambda bgr: bgr[::-1], obj))
