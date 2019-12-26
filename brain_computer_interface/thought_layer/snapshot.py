from abc import ABC
from datetime import datetime, timezone

from construct import Struct, Int32ul, Int64ul, Float64l, Array, this, Byte, Float32l, Container, Adapter

from .protocol_message import ProtocolMessage


class TimestampAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return datetime.utcfromtimestamp(obj / 1000)

    def _encode(self, obj, context, path):
        return int(obj.replace(tzinfo=timezone.utc).timestamp() * 1000)


class Snapshot(ProtocolMessage):
    snapshot_timestamp = TimestampAdapter(Int64ul)
    translation = Struct(x=Float64l, y=Float64l, z=Float64l)
    rotation = Struct(x=Float64l, y=Float64l, z=Float64l, w=Float64l)
    color_image = Struct(height=Int32ul, width=Int32ul, image=Array(this.height * this.width, Byte[3]))
    depth_image = Struct(height=Int32ul, width=Int32ul, image=Array(this.height * this.width, Float32l))
    feelings = Struct(hunger=Float32l, thirst=Float32l, exhaustion=Float32l, happiness=Float32l)

    protocol = Struct(timestamp=snapshot_timestamp, translation=translation, rotation=rotation, color_image=color_image,
                      depth_image=depth_image, feelings=feelings)

    def __init__(self, timestamp=0, translation=None, rotation=None, color_image=None, depth_image=None, feelings=None,
                 **kwargs):

        if translation is None:
            translation = Container(x=0, y=0, z=0)
        if rotation is None:
            rotation = Container(x=0, y=0, z=0, w=0)
        if color_image is None:
            color_image = Container(height=0, width=0, image=[])
        if depth_image is None:
            depth_image = Container(height=0, width=0, image=[])
        if feelings is None:
            feelings = Container(hunger=0, thirst=0, exhaustion=0, happiness=0)
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __eq__(self, other):
        return isinstance(other, Snapshot) and self.timestamp == other.timestamp \
               and self.translation == other.translation and self.rotation == other.rotation \
               and self.color_image == other.color_image and self.depth_image == other.depth_image \
               and self.feelings == other.feelings

    def serialize(self):
        return self.protocol.build(dict(timestamp=self.timestamp, translation=self.translation, rotation=self.rotation,
                                        color_image=self.color_image, depth_image=self.depth_image,
                                        feelings=self.feelings))
