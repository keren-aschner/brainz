from construct import Struct, Int32ul, Int64ul, PascalString, PaddedString, Float64l, Array, this, Byte, Float32l, \
    StreamError
from datetime import datetime

user = Struct(id=Int64ul, name=PascalString(Int32ul, 'utf-8'), birth_date=Int32ul, gender=PaddedString(1, 'utf-8'))
translation = Struct(x=Float64l, y=Float64l, z=Float64l)
rotation = Struct(x=Float64l, y=Float64l, z=Float64l, w=Float64l)
color_image = Struct(height=Int32ul, width=Int32ul, image=Array(this.height * this.width, Byte[3]))
depth_image = Struct(height=Int32ul, width=Int32ul, image=Array(this.height * this.width, Float32l))
feelings = Struct(hunger=Float32l, thirst=Float32l, exhaustion=Float32l, happiness=Float32l)
snapshot = Struct(timestamp=Int64ul, translation=translation, rotation=rotation, color_image=color_image,
                  depth_image=depth_image, feelings=feelings)


class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'rb') as f:
            self.user = user.parse_stream(f)
            self.pos = f.tell()
        self.user.birth_date = datetime.fromtimestamp(self.user.birth_date)

    def __iter__(self):
        while True:
            with open(self.file_path, 'rb') as f:
                f.seek(self.pos)
                try:
                    s = snapshot.parse_stream(f)
                except StreamError:
                    raise StopIteration
                self.pos = f.tell()
            s.timestamp = datetime.fromtimestamp(s.timestamp / 1000)
            s.color_image.image = list(map(lambda bgr: bgr[::-1], s.color_image.image))
            yield s
