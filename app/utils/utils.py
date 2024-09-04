import base64
import os
import requests
from uuid import uuid4

def decode_base64_image(image_base64):
    """Decode a base64 string into an image and save it as a temporary file."""
    try:
        image_data = base64.b64decode(image_base64)
        temp_file_path = f"/tmp/{uuid4().hex}.png"
        with open(temp_file_path, "wb") as f:
            f.write(image_data)
        return temp_file_path
    except Exception as e:
        raise ValueError("Invalid base64 image data")

def download_image_from_link(image_link):
    """Download an image from a link and save it as a temporary file."""
    try:
        response = requests.get(image_link)
        response.raise_for_status()
        temp_file_path = f"/tmp/{uuid4().hex}.png"
        with open(temp_file_path, "wb") as f:
            f.write(response.content)
        return temp_file_path
    except Exception as e:
        raise ValueError(f"Failed to download image from link: {str(e)}")

def rotate_image_until_correct(image, ktp_box, wajah_box):
    """Rotate the image until wajah is correctly positioned inside the ktp box."""
    for angle in [90, -90, 180]:
        # Rotate the image
        image_rotated = image.rotate(angle, expand=True)
        
        # Rotate the bounding boxes
        wajah_box_rotated = rotate_box(wajah_box, image.size, angle)
        ktp_box_rotated = rotate_box(ktp_box, image.size, angle)

        # Check if the wajah is now correctly positioned
        if is_wajah_on_right_side(ktp_box_rotated, wajah_box_rotated):
            return image_rotated, ktp_box_rotated, wajah_box_rotated

    return image, ktp_box, wajah_box  # Return original if no correct rotation found

def rotate_box(box, image_size, angle):
    """Rotate the bounding box coordinates according to the given angle."""
    x_min, y_min, x_max, y_max = box
    width, height = image_size
    
    if angle == 90:
        return [y_min, width - x_max, y_max, width - x_min]
    elif angle == -90:
        return [height - y_max, x_min, height - y_min, x_max]
    elif angle == 180:
        return [width - x_max, height - y_max, width - x_min, height - y_min]
    else:
        return box  # No rotation

def is_wajah_on_right_side(ktp_box, wajah_box):
    """Check if the wajah box is on the right side inside the ktp box."""
    ktp_x_min, ktp_y_min, ktp_x_max, ktp_y_max = ktp_box
    wajah_x_min, wajah_y_min, wajah_x_max, wajah_y_max = wajah_box
    
    # Check if wajah is within the boundaries of ktp
    if (wajah_x_min > ktp_x_min) and (wajah_x_max < ktp_x_max) and (wajah_y_min > ktp_y_min) and (wajah_y_max < ktp_y_max):
        # Check if wajah is on the right half of the ktp
        ktp_center_x = (ktp_x_min + ktp_x_max) / 2
        return wajah_x_min > ktp_center_x
    return False
