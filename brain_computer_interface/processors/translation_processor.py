import json

from .processor import Processor
from ..server import Server
from ..thought_layer import Snapshot


@Server.processor('timestamp', 'translation')
class TranslationProcessor(Processor):
    def process(self, snapshot: Snapshot):
        with open(self.get_dir(snapshot.timestamp) / 'translation.json', 'w+') as f:
            json.dump(snapshot.translation, f)
