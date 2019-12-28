import json

from .processor import Processor
from ..server import Server


@Server.processor('timestamp', 'translation')
class TranslationProcessor(Processor):
    def process(self, snapshot):
        translation = dict(snapshot.translation)
        translation.pop('_io', None)
        with open(self.get_dir(snapshot.timestamp) / 'translation.json', 'w+') as f:
            json.dump(translation, f)
