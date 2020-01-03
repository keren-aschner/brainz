import json

from ..server import Server, TIMESTAMP, POSE


@Server.processor(TIMESTAMP, POSE)
def process(context, snapshot):
    path = context.path(snapshot[TIMESTAMP], 'translation.json')
    translation = snapshot[POSE]['translation']
    with open(path, 'w+') as f:
        json.dump(translation, f)
