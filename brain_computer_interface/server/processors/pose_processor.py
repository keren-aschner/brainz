import json

from ..context import Context


def process_pose(context, snapshot):
    path = context.path(snapshot[context.TIMESTAMP], 'pose.json')
    with open(path, 'w+') as f:
        json.dump(snapshot[context.POSE], f)


process_pose.fields = [Context.TIMESTAMP, Context.POSE]
