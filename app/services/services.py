import os
import base64
from io import BytesIO
from ultralytics import YOLO
from PIL import Image, ImageOps
from app.utils.utils import rotate_image_until_correct

# Define the model path relative to the current file
model_path = os.path.join(os.path.dirname(__file__), '../models/ktp_and_face.pt')

# Initialize a YOLO model
model = YOLO(model_path)  # Load your custom model

# Define a mapping from class index to class name
class_mapping = {0: "ktp", 1: "wajah"}

def process_image(image_path, output_dir, max_resolution=(800, 800)):
    # Execute prediction for specified categories on an image
    results = model.predict(image_path)

    # Load the original image and correct its orientation
    image = Image.open(image_path)
    image = ImageOps.exif_transpose(image)

    # Extract the boxes and confidence scores
    ktp_box = None
    wajah_box = None
    ktp_confidence = None
    wajah_confidence = None

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # class index
            xyxy = box.xyxy[0].tolist()  # xyxy format: [x_min, y_min, x_max, y_max]
            conf = box.conf[0].item()  # confidence score
            
            if class_mapping.get(cls) == "ktp":
                ktp_box = list(map(int, xyxy))
                ktp_confidence = conf
            elif class_mapping.get(cls) == "wajah":
                wajah_box = list(map(int, xyxy))
                wajah_confidence = conf

    if ktp_box and wajah_box:
        # Rotate the image if needed
        image, ktp_box, wajah_box = rotate_image_until_correct(image, ktp_box, wajah_box)

        # Crop the rotated image using the ktp bounding box
        x_min, y_min, x_max, y_max = ktp_box
        cropped_image = image.crop((x_min, y_min, x_max, y_max))

        # Scale down the resolution
        cropped_image.thumbnail(max_resolution, Image.Resampling.LANCZOS)

        # Convert the cropped image to Base64 without saving locally
        buffered = BytesIO()
        cropped_image.save(buffered, format="PNG")
        base64_cropped_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return {
            "cropped_image_base64": base64_cropped_image,
            "ktp_box": ktp_box,
            "ktp_confidence": ktp_confidence,
            "wajah_box": wajah_box,
            "wajah_confidence": wajah_confidence
        }
    else:
        raise ValueError("Both 'ktp' and 'wajah' must be detected in the image.")
