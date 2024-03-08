import functions_framework
import sklearn
import os
import torch
import base64
from transformers import pipeline
from google.cloud import storage
from datasets import load_from_disk
from flask import make_response,jsonify


storage_client = storage.Client()


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    input = request_json['input']


    # Environment variables for the GCS bucket and model directory
    MODEL_DIR = '/tmp/model'
    DATASET_DIR = '/tmp/dataset'
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(DATASET_DIR, exist_ok=True)
    # Model and tokenizer file names
    model_files = [
        "config.json",
        "pytorch_model.bin",
        "added_tokens.json",
        "preprocessor_config.json",
        "special_tokens_map.json",
        "spm_char.model",
        "tokenizer_config.json"
    ]     
    if not os.listdir(MODEL_DIR):  # This checks if the directory is empty
        for file_name in model_files:
            download_model_files('cmpt-756-group-bucket', f"speecht5_tts/{file_name}",os.path.join(MODEL_DIR, file_name))
    dataset_files = ["data-00000-of-00001.arrow", "state.json","dataset_info.json"]
    
    if not os.listdir(DATASET_DIR):  # This checks if the directory is empty
        for file_name in dataset_files:
            download_model_files('cmpt-756-group-bucket', f"speecht5_tts/dataset/{file_name}",os.path.join(DATASET_DIR, file_name))
                
    # processor = AutoProcessor.from_pretrained(MODEL_DIR)
    # model = AutoModelForTextToSpectrogram.from_pretrained(MODEL_DIR)
    dataset = load_from_disk(DATASET_DIR)
    synthesiser = pipeline("text-to-speech", MODEL_DIR)
    speaker_embedding = torch.tensor(dataset[7306]["xvector"]).unsqueeze(0)
    speech = synthesiser(input, forward_params={"speaker_embeddings": speaker_embedding})    
    audio_base64 = base64.b64encode(speech["audio"]).decode("utf-8")

    # Prepare the response with appropriate headers
    response = jsonify({
        "audio_content": audio_base64,
        "content_type": "audio/wav",
        "sampling_rate": speech["sampling_rate"]
    })
    response.headers.set('Content-Type', 'application/json')
    
    # Return the response
    return response    

# Function to download model files from GCS
def download_model_files(bucket_name, source_blob_name, destination_file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"{source_blob_name} downloaded to {destination_file_name}.")

# def download_dataset(bucket_name, prefix, local_path):
#     """Download all files in the specified prefix from the bucket to the local path."""
#     blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
#     # os.makedirs(local_path, exist_ok=True)
#     for blob in blobs:
#         local_file_path = os.path.join(local_path, os.path.basename(blob.name))
#         download_model_files(bucket_name, blob.name, local_file_path)
        

 

# functions-framework==3.*
# google-cloud-storage==1.25.0
# scikit-learn==1.2.2
# transformers==4.38.2
# datasets==2.4.0
# sentencepiece
# tensorflow
# torch
# Flask
     
     
# https://us-central1-nice-beanbag-416418.cloudfunctions.net/function-2     

# Sample Input
# {input:"I love this"}