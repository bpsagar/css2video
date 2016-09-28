
class RenderNotImplemented(Exception):
    """Exception raised when a renderer class has not implemented the render
    function"""


class BaseVideoRenderer(object):
    """Base Video Renderer class that accepts a sequence of images, framerate
    and outputs a video

    Public attributes
        - image_sequence: Sequence of image to be used
        - output_path: Path where the output video needs to be saved
        - framerate: No of images per second of the video
    """

    def __init__(self, image_sequence, output_path, framerate):
        super(BaseVideoRenderer, self).__init__()
        self.image_sequence = image_sequence
        self.output_path = output_path
        self.framerate = framerate

    def render(self):
        """Renders the video. Subclasses should override this method"""
        raise RenderNotImplemented('Render function is not implemented.')
