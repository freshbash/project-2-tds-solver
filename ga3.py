import base64

def q4(file):

    image_bytes = file.read()
    # Open the image file in binary mode
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    # Create the base64 URL
    image_url = f"data:image/png;base64,{encoded_image}"

    return image_url