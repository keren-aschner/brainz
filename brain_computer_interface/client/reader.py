from .mind import Parser, BinaryParser, ProtobufParser, ParsingError


def _get_parser(protobuf: bool) -> Parser:
    """
    :param protobuf: Whether to return the protobuf parser.
    :return: The relevant parser according to `protobuf`.
    """
    if protobuf:
        return ProtobufParser()
    return BinaryParser()


class Reader:
    """
    A reader used to extracting user information and snapshots from sample files.
    """

    def __init__(self, file_path: str, protobuf: bool) -> None:
        """
        Parse the user from the given sample and initiate the data members of the class.

        :param file_path: The path to the sample file.
        :param protobuf: Whether to use a protobuf or binary format.
        """
        self.parser = _get_parser(protobuf)
        self.file_path = file_path
        with self.parser.open(file_path, 'rb') as f:
            self.user = self.parser.parse_user(f)
            self.pos = f.tell()

    def __iter__(self):
        """
        Iterate over and parse the snapshots in the sample file.
        """
        while True:
            with self.parser.open(self.file_path, 'rb') as f:
                f.seek(self.pos)
                try:
                    s = self.parser.parse_snapshot(f)
                except ParsingError:
                    break
                self.pos = f.tell()
            yield s
