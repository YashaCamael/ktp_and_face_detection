# KTP and Face Detection API

This API allows you to detect and process images of KTP (Indonesian ID cards) and faces. The API supports three types of image inputs: image file path, Base64-encoded image, and image URL.

## API Endpoint

**POST** `/process-image`

This endpoint processes the image and returns the cropped image, along with the bounding box coordinates and confidence scores for KTP and face detections.

## Request Payload

The API accepts a JSON payload with one of the following fields:

- `image_path`: Path to the image file on the server.
- `image_base64`: Base64-encoded image data.
- `image_link`: URL of the image to be processed.

**Note**: Only one of these fields should be provided at a time.

## Example `curl` Commands

### 1. Using `image_path`

If you have the image file located on the server, you can send the file path:

```bash
curl -X POST http://127.0.0.1:5000/process-image \
-H "Content-Type: application/json" \
-d '{"image_path": "path/to/your/image.png"}'
```

### 2. Using `image_base64`

First, encode your image in Base64:

```bash
base64 path/to/your/image.png > encoded_image.txt
```

Then, use the Base64 string in your request:

```bash
curl -X POST http://127.0.0.1:5000/process-image \
-H "Content-Type: application/json" \
-d '{"image_base64": "your_base64_encoded_string_here"}'
```

Replace `"your_base64_encoded_string_here"` with the actual Base64 string from the `encoded_image.txt` file.

### 3. Using `image_link`

If the image is hosted online, you can provide a direct link to the image:

```bash
curl -X POST http://127.0.0.1:5000/process-image \
-H "Content-Type: application/json" \
-d '{"image_link": "https://example.com/path/to/image.png"}'
```

### Response

The API returns a JSON object with the following structure:

```json
{
    "cropped_image_path": "output/cropped_ktp.png",
    "ktp_box": [100, 200, 300, 400],
    "ktp_confidence": 0.98,
    "wajah_box": [150, 250, 200, 300],
    "wajah_confidence": 0.95
}
```

- cropped_image_path: Path to the saved cropped image.
- ktp_box: Bounding box coordinates for the KTP in the format [x_min, y_min, x_max, y_max].
- ktp_confidence: Confidence score for the KTP detection.
- wajah_box: Bounding box coordinates for the face in the format [x_min, y_min, x_max, y_max].
- wajah_confidence: Confidence score for the face detection.

### Error Handling

If the request payload is invalid or more than one image input type is provided, the API will return an error:

```bash
{
    "error": "You must provide exactly one of image_path, image_base64, or image_link."
}
```

