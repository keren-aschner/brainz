from abc import ABC
from datetime import datetime

from construct import Struct, Int32ul, Int64ul, PascalString, PaddedString, Float64l, Array, this, Byte, Float32l, \
    StreamError, Adapter


class ParsingError(Exception):
    pass


class DateAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return datetime.fromtimestamp(obj)

    def _encode(self, obj, context, path):
        return obj.timestamp()


class SnapshotTimestampAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return obj / 1000

    def _encode(self, obj, context, path):
        return obj * 1000


class ColorImageAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return list(map(lambda bgr: bgr[::-1], obj))

    def _encode(self, obj, context, path):
        return list(map(lambda bgr: bgr[::-1], obj))


def parse_user(stream):
    birth_date = DateAdapter(Int32ul)
    user = Struct(id=Int64ul, name=PascalString(Int32ul, 'utf-8'), birth_date=birth_date,
                  gender=PaddedString(1, 'utf-8'))
    return user.parse_stream(stream)


def parse_snapshot(stream):
    snapshot_timestamp = DateAdapter(SnapshotTimestampAdapter(Int64ul))
    translation = Struct(x=Float64l, y=Float64l, z=Float64l)
    rotation = Struct(x=Float64l, y=Float64l, z=Float64l, w=Float64l)
    color_image = Struct(height=Int32ul, width=Int32ul,
                         image=ColorImageAdapter(Array(this.height * this.width, Byte[3])))
    depth_image = Struct(height=Int32ul, width=Int32ul, image=Array(this.height * this.width, Float32l))
    feelings = Struct(hunger=Float32l, thirst=Float32l, exhaustion=Float32l, happiness=Float32l)
    snapshot = Struct(timestamp=snapshot_timestamp, translation=translation, rotation=rotation, color_image=color_image,
                      depth_image=depth_image, feelings=feelings)

    try:
        return snapshot.parse_stream(stream)
    except StreamError:
        raise ParsingError
