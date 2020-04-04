from ..context import Context
from ...protocol.fields import POSE


def parse_pose(message: bytes) -> bytes:
    """
    Extract the pose from each snapshot.
    """
    context = Context(message)
    return context.serialize(context.snapshot[POSE])


parse_pose.fields = [POSE]
