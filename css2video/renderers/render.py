import os
import shutil
import tempfile
from tqdm import tqdm

from .image import render_image
from .video import render_video
from css2video.interpolators import interpolate_stylesheet
from css2video.parsers.stylesheet import StyleSheet
from css2video.outputters import output_stylesheet


def _get_image_sequence(total_frames):
    return '%0{digits}d.jpg'.format(digits=len(str(total_frames)))


def _get_frame_image_name(frame, total_frames):
    image_sequence = _get_image_sequence(total_frames=total_frames)
    return image_sequence % frame


def render_animation(
        html_path, css_path, output_path, duration, framerate=30, width=800,
        height=600, image_renderer='CUTYCAPT', video_renderer='FFMPEG'):

    with open(css_path, 'r') as fd:
        css = fd.read()

    html_path = os.path.abspath(html_path)
    output_path = os.path.abspath(output_path)

    stylesheet_dict = StyleSheet.parse(css)
    total_frames = framerate * duration
    duration_per_frame = float(duration) / total_frames

    temp_dir = tempfile.mkdtemp()

    for frame in tqdm(range(total_frames)):
        time = frame * duration_per_frame
        filename = _get_frame_image_name(
            frame=frame, total_frames=total_frames)

        temp_stylesheet_dict = interpolate_stylesheet(
            stylesheet_dict=stylesheet_dict, time=time)
        temp_css = output_stylesheet(stylesheet_dict=temp_stylesheet_dict)
        temp_css_path = os.path.join(temp_dir, 'temp.css')
        with open(temp_css_path, 'w') as fd:
            fd.write(temp_css)

        temp_output_path = os.path.join(temp_dir, filename)

        render_image(
            html_path=html_path, css_path=temp_css_path,
            output_path=temp_output_path, width=width, height=height,
            renderer=image_renderer
        )

    input_image_sequence = os.path.join(
        temp_dir, _get_image_sequence(total_frames=total_frames))
    render_video(
        image_sequence=input_image_sequence, output_path=output_path,
        framerate=framerate, renderer=video_renderer
    )
    shutil.rmtree(temp_dir)
