from .ffmpeg import FFMpegRenderer


def render_video(image_sequence, output_path, framerate=30, renderer='FFMPEG'):
    if renderer == 'FFMPEG':
        renderer = FFMpegRenderer(image_sequence, output_path, framerate)
    renderer.render()
