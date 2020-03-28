import json

from ..context import Context


def parse_pose(context, snapshot):
    context.save('pose.json', json.dumps(snapshot[context.POSE]))


parse_pose.field = Context.POSE
