# css2video

A tool to convert CSS animations to an MPEG video

## Usage

```
# Clone the repository
git clone https://github.com/bpsagar/css2video.git

# Build the docker image
docker build -t css2video .

# Run the example, it should create a test.mp4 file in the examples folder
docker run -v $PWD:/app css2video python examples/test.py

# Make any changes to the test.py or add your own python script and run the
# script inside the css2video container

```

## Quirks

- The animation doesn't get captured in the video if the CSS is linked in the HTML page. So don't add the link tag (that would point to the CSS file) in the HTML file.
- Keyframe CSS should be explicit:
    - Explicitly define the default values.
    - Avoid short hand CSS values.
- Each frames take a second to render so the whole rendering process is a bit slow.

**Note**: Feel free to notify me about any issues

