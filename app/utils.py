import face_recognition
import numpy as np
import base64
import io
from PIL import Image

def image_to_embedding(base64_image: str):
    try:
        # Si la imagen tiene el prefijo data:image/..., sepáralo
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        image_np = np.array(image)

        encodings = face_recognition.face_encodings(image_np)
        if not encodings:
            return None
        return encodings[0]
    except Exception as e:
        print(f"Error al procesar imagen: {e}")
        return None
