from construct import Struct


class ProtocolMessage:
    protocol = Struct()

    def serialize(self):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data):
        return cls(**cls.protocol.parse(data))
