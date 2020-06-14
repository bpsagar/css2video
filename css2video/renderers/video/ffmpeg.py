import subprocess
import shlex

from .base import BaseVideoRenderer


class FFMpegRenderer(BaseVideoRenderer):
    """Video renderer that uses ffmpeg command"""

    def __init__(self, *args, **kwargs):
        super(FFMpegRenderer, self).__init__(*args, **kwargs)

    def render(self):
        """Render the video"""

        command_args = {
            'i': self.image_sequence,
            'r': '%d' % self.framerate
        }
        args = ' '.join(
            ['-%s %s' % (key, value) for key, value in command_args.items()])
        command = 'ffmpeg %s %s' % (args, self.output_path)

        process = subprocess.Popen(
            shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

