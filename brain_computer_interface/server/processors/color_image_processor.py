from PIL import Image

from .processor import Processor
from ..server import Server, TIMESTAMP, COLOR_IMAGE

import base64


@Server.processor(TIMESTAMP, COLOR_IMAGE)
class ColorImageProcessor(Processor):
    def process(self, snapshot):
        color_image = snapshot[COLOR_IMAGE]
        image = Image.new('RGB', (color_image['width'], color_image['height']))
        data = base64.b64decode(color_image['data'])
        data = [(data[i], data[i + 1], data[i + 2]) for i in range(0, len(data), 3)]
        image.putdata(data)
        image.save(self.get_dir(snapshot[TIMESTAMP]) / 'color_image.jpg')
