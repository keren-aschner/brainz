from parser import parse_user, parse_snapshot, ParsingError


class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'rb') as f:
            self.user = parse_user(f)
            self.pos = f.tell()

    def __iter__(self):
        while True:
            with open(self.file_path, 'rb') as f:
                f.seek(self.pos)
                try:
                    s = parse_snapshot(f)
                except ParsingError:
                    raise StopIteration
                self.pos = f.tell()
            yield s
