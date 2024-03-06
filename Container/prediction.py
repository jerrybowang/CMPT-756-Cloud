import tensorflow as tf
import numpy as np
import cv2


# Load the model
model = tf.keras.models.load_model('model/model.keras')

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

def predict(image_path: str):
    # load and preprocess the image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (32, 32))
    image = image.astype('float32') / 255.0

    # make a prediction
    prediction = model.predict(image.reshape(1, 32, 32, 3))
    class_name = class_names[np.argmax(prediction)]
    return class_name

