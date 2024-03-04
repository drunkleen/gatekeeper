import qrcode
import base64
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import random
import string


def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Create a BytesIO object to hold the image data in memory
    img_byte_array = BytesIO()

    # Save the image to the BytesIO object without saving to a file
    qr.make_image(fill_color="black", back_color="white").save(img_byte_array, format='PNG')

    # Get the image data as bytes
    img_data = img_byte_array.getvalue()

    # Encode the image data to Base64
    img_data_base64 = base64.b64encode(img_data).decode('utf-8')

    return img_data_base64


def link_scraper(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            return soup.prettify()
        else:
            return f"Failed to fetch the page. Status code: {response.status_code}"

    except requests.RequestException as e:
        return e


def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=126))
