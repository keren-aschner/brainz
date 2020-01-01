import base64
from abc import ABC

from construct import Struct, Int32ul, Int64ul, PascalString, PaddedString, Float64l, Array, this, Byte, Float32l, \
    StreamError, Adapter, Enum, Container

from .parser import Parser, ParsingError


class BinaryParser(Parser):
    def parse_user(self, stream):
        user = Struct(user_id=Int64ul, username=PascalString(Int32ul, 'utf-8'), birthday=Int32ul,
                      gender=Enum(PaddedString(1, 'utf-8'), MALE='m', FEMALE='f', OTHER='o'))
        return container_to_dict(user.parse_stream(stream))

    def parse_snapshot(self, stream):
        translation = Struct(x=Float64l, y=Float64l, z=Float64l)
        rotation = Struct(x=Float64l, y=Float64l, z=Float64l, w=Float64l)
        pose = Struct(translation=translation, rotation=rotation)
        color_image = Struct(height=Int32ul, width=Int32ul,
                             data=ColorImageAdapter(Array(this.height * this.width, Byte[3])))
        depth_image = Struct(height=Int32ul, width=Int32ul, data=Array(this.height * this.width, Float32l))
        feelings = Struct(hunger=Float32l, thirst=Float32l, exhaustion=Float32l, happiness=Float32l)
        snapshot = Struct(timestamp=Int64ul, pose=pose, color_image=color_image, depth_image=depth_image,
                          feelings=feelings)

        try:
            return container_to_dict(snapshot.parse_stream(stream))
        except StreamError:
            raise ParsingError


class ColorImageAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return base64.b64encode(b''.join(map(lambda bgr: bytes(bgr[::-1]), obj))).decode()


def container_to_dict(container):
    if not isinstance(container, Container):
        return container

    dic = {}
    for key in container.keys():
        dic[key] = container_to_dict(container[key])

    dic.pop('_io', None)
    return dic
