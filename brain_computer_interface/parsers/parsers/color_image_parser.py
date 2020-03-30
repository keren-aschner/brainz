import base64

from PIL import Image

from ..context import Context
from ...protocol.fields import COLOR_IMAGE, DATA, HEIGHT, WIDTH


def parse_color_image(message: bytes) -> bytes:
    """
    Extract the RGB color image from each snapshot and save it as a jpg image.
    """
    context = Context(message)
    color_image_path = context.path('color_image.jpg')

    color_image = context.snapshot[COLOR_IMAGE]
    image = Image.new('RGB', (color_image[WIDTH], color_image[HEIGHT]))
    data = base64.b64decode(color_image[DATA])
    data = [(data[i], data[i + 1], data[i + 2]) for i in range(0, len(data), 3)]
    image.putdata(data)
    image.save(color_image_path)

    return context.serialize({'path': str(color_image_path.absolute())})


parse_color_image.fields = [COLOR_IMAGE]
