from .mind.binary_parser import BinaryParser
from .mind.parser import ParsingError
from .mind.protobuf_parser import ProtobufParser


def _get_parser(protobuf):
    if protobuf:
        return ProtobufParser()
    return BinaryParser()


class Reader:
    def __init__(self, file_path, protobuf=True):
        self.parser = _get_parser(protobuf)
        self.file_path = file_path
        with self.parser.open(file_path, 'rb') as f:
            self.user = self.parser.parse_user(f)
            self.pos = f.tell()

    def __iter__(self):
        while True:
            with self.parser.open(self.file_path, 'rb') as f:
                f.seek(self.pos)
                try:
                    s = self.parser.parse_snapshot(f)
                except ParsingError:
                    break
                self.pos = f.tell()
            yield s
