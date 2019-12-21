import struct

from datetime import datetime


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        return f'[{self.timestamp}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        return isinstance(other, Thought) and self.user_id == other.user_id \
               and self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self):
        return struct.pack('LL', self.user_id, int(self.timestamp.timestamp())) + self.thought.encode()

    @classmethod
    def deserialize(cls, data):
        user_id, timestamp = struct.unpack('LL', data[:16])
        thought = data[16:].decode('utf-8')
        return Thought(user_id, datetime.fromtimestamp(timestamp), thought)
