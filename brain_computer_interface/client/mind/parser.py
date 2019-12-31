class ParsingError(Exception):
    pass


class Parser:
    def parse_user(self, stream):
        raise NotImplementedError

    def parse_snapshot(self, stream):
        raise NotImplementedError

    @classmethod
    def open(cls, *args, **kwargs):
        return open(*args, **kwargs)
