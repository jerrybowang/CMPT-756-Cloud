import tensorflow as tf
import numpy as np
import cv2

from transformers import pipeline

local_path = "/app/blip-image-captioning-base"
captioner = pipeline("image-to-text", model=local_path)

def predict(image_path: str) -> str:
    """
    Predict the caption of an image using the BLIP image captioning model.

    Parameters:
    image_path (str): The file path of the image to caption.

    Returns:
    str: The generated caption for the image.
    """

    # Use the BLIP model to generate a caption for the image
    result = captioner(image_path)

    # Extract the generated text from the results
    generated_text = result[0]["generated_text"]
    return generated_text