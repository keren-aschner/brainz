from ..context import Context
from ...protocol.fields import POSE


def parse_pose(message: bytes) -> bytes:
    """
    Extract the pose from each snapshot.
    """
    context = Context(message)
    return context.serialize({'pose': context.snapshot[POSE]})


parse_pose.fields = [POSE]
