from .cutycapt import CutyCaptRenderer


def render_image(
        html_path, css_path, output_path, width=800, height=600,
        renderer='CUTYCAPT'):
    """Render HTML CSS as an image"""

    if renderer == 'CUTYCAPT':
        renderer = CutyCaptRenderer(
            html_path, css_path, output_path, width, height)

    renderer.render()
