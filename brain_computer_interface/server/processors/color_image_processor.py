from PIL import Image

from .processor import Processor
from ..server import Server


@Server.processor('timestamp', 'color_image')
class ColorImageProcessor(Processor):
    def process(self, snapshot):
        image = Image.new('RGB', (snapshot.color_image.width, snapshot.color_image.height))
        image.putdata(snapshot.color_image.image)
        image.save(self.get_dir(snapshot.timestamp) / 'color_image.jpg')
