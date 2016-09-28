
class RenderNotImplemented(Exception):
    """Exception raised when a renderer class has not implemented the render
    function"""


class BaseImageRenderer(object):
    """Base Renderer class that accepts HTML file path and CSS file path

    Public attributes:
        - html_path: path to the HTML file
        - css_path: path to the CSS file
        - output_path: path where the image has to be stored
        - width: width of the image file to be rendered
        - height: height of the image file to be rendered
    """

    def __init__(
            self, html_path, css_path, output_path, width=800, height=600):
        super(BaseImageRenderer, self).__init__()
        self.html_path = html_path
        self.css_path = css_path
        self.output_path = output_path
        self.width = width
        self.height = height

    def render(self):
        """Renders the HTML and CSS as an image. Subclasses should override
        this method"""
        raise RenderNotImplemented('Render function is not implemented.')
