import numpy as np
from matplotlib import pyplot

from ..context import Context
from ...protocol.fields import DEPTH_IMAGE, HEIGHT, WIDTH, DATA


def parse_depth_image(message: bytes) -> bytes:
    """
     Save the depth image data as a jpg image.
    """
    context = Context(message)
    depth_image_path = context.path('depth_image.jpg')

    depth_image = context.snapshot[DEPTH_IMAGE]
    data = np.array(depth_image[DATA]).reshape((depth_image[HEIGHT], depth_image[WIDTH]))
    pyplot.imsave(depth_image_path, data)
    return context.serialize({'path': str(depth_image_path.absolute())})


parse_depth_image.fields = [DEPTH_IMAGE]
