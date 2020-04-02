class BaseParser:
    """
    A base class for parsers.
    """

    def __init__(self, *fields):
        """
         The subclasses of Parser should call this method with their required fields.
        """
        if fields is not None:
            self.fields = fields
        else:
            raise ValueError("No fields supplied to parser.")

    def parse(self, message: bytes) -> bytes:
        """
        Implement this method.
        """
        raise NotImplementedError()
