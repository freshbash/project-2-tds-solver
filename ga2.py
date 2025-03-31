import base64
import os
from PIL import Image
from io import BytesIO
import numpy as np
import colorsys

def q2(file, max_size=1500):
    """Compress PNG file losslessly and return base64-encoded content."""
    
    # Open image
    image = Image.open(file)

    # Save with optimization to an in-memory buffer
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)

    # Check size
    if buffer.tell() < max_size:
        pass  # Image is already small enough
    else:
        # Try further compression
        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True, compress_level=9)

    # Convert to base64
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.read()).decode("utf-8")

    return base64_image


def q5(file, brightness):
    image = Image.open(file)

    rgb = np.array(image) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    light_pixels = int(np.sum(lightness > brightness))
    return light_pixels
