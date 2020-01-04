import json

from ..context import Context


def process_pose(context, snapshot):
    context.save('pose.json', json.dumps(snapshot[context.POSE]))


process_pose.field = Context.POSE
