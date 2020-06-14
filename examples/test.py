"""
Use this example file to render your own HTML CSS to MPEG video.
"""
import os
from css2video.renderers import render_animation


directory = os.path.dirname(__file__)
html_path = os.path.join(directory, 'test.html')
css_path = os.path.join(directory, 'test.css')
output_path = os.path.join(directory, 'test.mp4')


render_animation(
    html_path=html_path,
    css_path=css_path,
    output_path=output_path,
    duration=1,
    framerate=60,
    width=300,
    height=300,
)

