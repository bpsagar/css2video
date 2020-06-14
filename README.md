# css2video

A tool to convert CSS animations to an MPEG video

## Usage

```
docker build -t css2video .

# Make any changes to the test.py or add your own python script and run the
# script inside the css2video container
docker run -v $PWD:/app css2video python examples/test.py
```

## Quirks

- Don't link the CSS file inside the HTML
- Keyframe CSS should be explicit:
    - Explicitly define the default values
    - Avoid short hand CSS values

