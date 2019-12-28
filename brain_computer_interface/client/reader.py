from .mind.binary_parser import BinaryParser
from .mind.parser import ParsingError


class Reader:
    def __init__(self, file_path):
        self.parser = BinaryParser()
        self.file_path = file_path
        with open(file_path, 'rb') as f:
            self.user = self.parser.parse_user(f)
            self.pos = f.tell()

    def __iter__(self):
        while True:
            with open(self.file_path, 'rb') as f:
                f.seek(self.pos)
                try:
                    s = self.parser.parse_snapshot(f)
                except ParsingError:
                    break
                self.pos = f.tell()
            yield s
