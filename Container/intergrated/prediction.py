from transformers import pipeline
import pickle


def image_to_text(image_path: str) -> str:
    """
    Predict the caption of an image using the BLIP image captioning model.

    Parameters:
    image_path (str): The file path of the image to caption.

    Returns:
    str: The generated caption for the image.
    """

    local_path = "blip-image-captioning-base/"
    captioner = pipeline("image-to-text", model=local_path)
    # Use the BLIP model to generate a caption for the image
    result = captioner(image_path)

    # Extract the generated text from the results
    generated_text = result[0]["generated_text"]
    return generated_text


def predict_sentiment(text):

    # Load the models
    with open("textclassifier_sentiment.pickle", "rb") as file:
        classifierKNN = pickle.load(file)

    with open("tfidfmodel.pickle", "rb") as file:
        vectorizer = pickle.load(file)

    # Convert the text into a numerical representation
    numerical_representation = vectorizer.transform([text])
    
    # Predict the sentiment of the text
    predicted_sentiment = classifierKNN.predict(numerical_representation)
    
    # Return the predicted sentiment
    return "Positive" if predicted_sentiment[0] == 1 else "Negative"

