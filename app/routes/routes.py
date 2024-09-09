from flask import request, jsonify
from app.services.services import process_image
from app.utils.utils import decode_base64_image, download_image_from_link
import os

def configure_routes(app):
    @app.route('/api/v1/AI/crop-ktp', methods=['POST'])
    def process_image_route():
        data = request.get_json()  # Parse JSON payload

        # Extract the instances array
        instances = data.get('instances', [])
        if len(instances) != 1:
            return jsonify({"error": "Invalid input format. Expected a single instance in 'instances' array."}), 400
        
        instance = instances[0]
        image_base64 = instance.get('image_base64')
        image_link = instance.get('image_link')

        # Validate that only one of image_base64 or image_link is provided
        if bool(image_base64) == bool(image_link):
            return jsonify({"error": "You must provide exactly one of 'image_base64' or 'image_link'."}), 400

        # Process the image based on the provided input
        if image_base64:
            try:
                image_file = decode_base64_image(image_base64)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        elif image_link:
            try:
                image_file = download_image_from_link(image_link)
            except Exception as e:
                return jsonify({"error": f"Failed to download image: {str(e)}"}), 400

        # Process the image
        output_dir = "output"  # You can make this configurable
        try:
            result = process_image(image_file, output_dir)
            
            # Wrap the result in a "prediction" field
            wrapped_result = {
                "prediction": [result]
            }
            return jsonify(wrapped_result), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        finally:
            # Clean up temporary file
            os.remove(image_file)

    @app.route('/api/v1/AI/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok", "message": "Service is up and running"}), 200
