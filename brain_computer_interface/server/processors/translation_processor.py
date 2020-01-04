import json

from ..server import TIMESTAMP, POSE


def process_translation(context, snapshot):
    path = context.path(snapshot[TIMESTAMP], 'translation.json')
    translation = snapshot[POSE]['translation']
    with open(path, 'w+') as f:
        json.dump(translation, f)


process_translation.fields = [TIMESTAMP, POSE]
