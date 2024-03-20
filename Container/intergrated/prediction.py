from transformers import pipeline, AutoTokenizer, TFAutoModelForSeq2SeqLM
from datasets import load_from_disk
import torch
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


def translation_eng(text: str) -> str:
    local_model_directory = "opus-mt-zh-en/"

    model = TFAutoModelForSeq2SeqLM.from_pretrained(local_model_directory)
    tokenizer = AutoTokenizer.from_pretrained(local_model_directory)
    # Assuming 'tokenizer' and 'model' are already initialized and suitable for translation

    input_ids = tokenizer.encode(text, return_tensors="tf")
    output = model.generate(input_ids)
    decoded_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return decoded_text


def text_to_speech(text: str):


    local_path = "speecht5_tts/"
    synthesiser = pipeline("text-to-speech", model=local_path)
    embeddings_dataset = load_from_disk("embeddings_dataset/")
    speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})

    return speech["audio"], speech["sampling_rate"]