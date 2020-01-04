import json

from ..context import Context


def process_translation(context, snapshot):
    path = context.path(snapshot[context.TIMESTAMP], 'translation.json')
    translation = snapshot[context.POSE]['translation']
    with open(path, 'w+') as f:
        json.dump(translation, f)


process_translation.fields = [Context.TIMESTAMP, Context.POSE]
