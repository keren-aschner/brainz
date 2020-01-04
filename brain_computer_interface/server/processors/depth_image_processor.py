import numpy as np
from matplotlib import pyplot

from ..context import Context


def process_depth_image(context, snapshot):
    path = context.path(snapshot[context.TIMESTAMP], 'depth_image.jpg')
    depth_image = snapshot[context.DEPTH_IMAGE]
    data = np.array(depth_image['data']).reshape((depth_image['height'], depth_image['width']))
    pyplot.imsave(path, data)


process_depth_image.fields = [Context.TIMESTAMP, Context.DEPTH_IMAGE]
