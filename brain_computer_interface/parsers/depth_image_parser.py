import numpy as np
from matplotlib import pyplot

from .context import Context


def parse_depth_image(context, snapshot):
    path = context.path('depth_image.jpg')
    depth_image = snapshot[context.DEPTH_IMAGE]
    data = np.array(depth_image['data']).reshape((depth_image['height'], depth_image['width']))
    pyplot.imsave(path, data)


parse_depth_image.field = Context.DEPTH_IMAGE
