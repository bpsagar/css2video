import subprocess
import shlex
import time

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
        xvfb_command = (
            'xvfb-run --server-args="-screen 0, {width}x{height}x24"'.format(
                width=self.width, height=self.height
            )
        )
        command = '{xvfb} cutycapt {args}'.format(args=args, xvfb=xvfb_command)

        process = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        okay, errors = process.communicate()
        # If we run without sleeping, it skips a few frames
        time.sleep(1)

