import subprocess

from .base import BaseImageRenderer


class CutyCaptRenderer(BaseImageRenderer):
    """Renderer which uses to CutyCapt to convert HTML, CSS to image"""

    def __init__(self, *args, **kwargs):
        super(CutyCaptRenderer, self).__init__(*args, **kwargs)

    def render(self):
        """Render the HTML and CSS as an image"""
        command_args = {
            'url': 'file:%s' % self.html_path,
            'user-style-path': self.css_path,
            'out': self.output_path,
            'min-width': int(self.width),
            'min-height': int(self.height)
        }
        args = ' '.join(
            ['--%s=%s' % (key, value) for key, value in command_args.items()])
        command = 'cutycapt %s' % args

        process = subprocess.Popen(
            command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
