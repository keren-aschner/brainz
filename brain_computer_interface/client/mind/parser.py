from typing import IO


class ParsingError(Exception):
    """
    Exception raised upon errors in parsing.
    """
    pass


class Parser:
    def parse_user(self, stream: IO) -> dict:
        """
        Parse a user from the given stream.
        """
        raise NotImplementedError

    def parse_snapshot(self, stream: IO) -> dict:
        """
        Parser a snapshot from the given stream.
        """
        raise NotImplementedError

    @classmethod
    def open(cls, *args, **kwargs) -> IO:
        """
        Open file and return a stream.
        """
        return open(*args, **kwargs)
