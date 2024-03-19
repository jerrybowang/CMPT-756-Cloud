import functions_framework
from flask import make_response
import requests
import sklearn
from google.cloud import storage
from datasets import load_from_disk, Dataset
import os
import torch
from transformers import AutoProcessor, AutoModelForTextToSpectrogram, pipeline
import base64
from flask import jsonify

storage_client = storage.Client()


@functions_framework.http
def hello_http(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)    
    print("111Headers:", request)
    print("222Headers:", request.headers)
    print("333Body:", request.get_data(as_text=True))
    request_json = request.get_json(silent=True)
    request_args = request.args
    input = request_json['input']


    # Environment variables for the GCS bucket and model directory
    MODEL_DIR = '/tmp'
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
    dataset_files = ["data-00000-of-00001.arrow", "state.json","dataset_info.json"]  
    if not os.path.exists("/tmp/pytorch_model.bin"):
        for file_name in model_files:
            download_model_files('cmpt-756-group-bucket', f"speecht5_tts/{file_name}",os.path.join(MODEL_DIR, file_name))
        for i in dataset_files:
            download_model_files('cmpt-756-group-bucket', f"speecht5_tts/dataset/{i}",os.path.join(DATASET_DIR, i))
                
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
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allows all domains
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    
    # Return the response
    return response    

# Function to download model files from GCS
def download_model_files(bucket_name, source_blob_name, destination_file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"{source_blob_name} downloaded to {destination_file_name}.")



# functions-framework==3.*
# google-cloud-storage==1.25.0
# scikit-learn==1.2.2
# transformers==4.38.2
# datasets==2.4.0
# sentencepiece
# tensorflow
# torch
# Flask

     