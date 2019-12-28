class ParsingError(Exception):
    pass


class Parser:
    def parse_user(self, stream):
        raise NotImplementedError

    def parse_snapshot(self, stream):
        raise NotImplementedError
