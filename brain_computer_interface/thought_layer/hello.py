from abc import ABC
from datetime import datetime, timezone

from construct import Struct, Int64ul, PascalString, Int32ul, PaddedString, Adapter

from .protocol_message import ProtocolMessage


class DateAdapter(Adapter, ABC):
    def _decode(self, obj, context, path):
        return datetime.utcfromtimestamp(obj)

    def _encode(self, obj, context, path):
        return int(obj.replace(tzinfo=timezone.utc).timestamp())


class Hello(ProtocolMessage):
    protocol = Struct(id=Int64ul, name=PascalString(Int32ul, 'utf-8'), birth_date=DateAdapter(Int32ul),
                      gender=PaddedString(1, 'utf-8'))

    def __init__(self, id, name, birth_date, gender, **kwargs):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.gender = gender

    def __eq__(self, other):
        return isinstance(other, Hello) and self.id == other.id and self.name == other.name \
               and self.birth_date == other.birth_date and self.gender == other.gender

    def serialize(self):
        return self.protocol.build(dict(id=self.id, name=self.name, birth_date=self.birth_date, gender=self.gender))
