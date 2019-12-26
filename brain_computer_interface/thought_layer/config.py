from construct import Struct, Int32ul, PascalString, Array, this

from .protocol_message import ProtocolMessage


class Config(ProtocolMessage):
    protocol = Struct(fields_num=Int32ul, fields=Array(this.fields_num, PascalString(Int32ul, 'utf-8')))

    def __init__(self, fields, **kwargs):
        self.fields = fields

    def __eq__(self, other):
        return isinstance(other, Config) and self.fields == other.fields

    def serialize(self):
        return self.protocol.build(dict(fields_num=len(self.fields), fields=self.fields))
