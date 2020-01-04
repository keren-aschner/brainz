import base64

from PIL import Image

from ..context import Context


def process_color_image(context, snapshot):
    color_image = snapshot[context.COLOR_IMAGE]
    image = Image.new('RGB', (color_image['width'], color_image['height']))
    data = base64.b64decode(color_image['data'])
    data = [(data[i], data[i + 1], data[i + 2]) for i in range(0, len(data), 3)]
    image.putdata(data)
    path = context.path(snapshot[context.TIMESTAMP], 'color_image.jpg')
    image.save(path)


process_color_image.fields = [Context.TIMESTAMP, Context.COLOR_IMAGE]
