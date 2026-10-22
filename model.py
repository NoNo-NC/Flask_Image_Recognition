"""Image preprocessing and model inference for hand-sign digits."""

from pathlib import Path

from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

MODEL_PATH = Path(__file__).resolve().parent / "digit_model.h5"

model = load_model(str(MODEL_PATH))


def preprocess_img(img_path):
    """Convert an image path or stream into a normalized RGB batch."""
    with Image.open(img_path) as image:
        resized_image = image.convert("RGB").resize((224, 224))
        image_array = img_to_array(resized_image) / 255.0

    return image_array.reshape(1, 224, 224, 3)


def predict_result(image_batch):
    """Return the highest-scoring digit class for one image batch."""
    predictions = model.predict(image_batch)
    return int(np.argmax(predictions[0], axis=-1))