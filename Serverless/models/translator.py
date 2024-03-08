import functions_framework
import sklearn
import os
from transformers import pipeline
from google.cloud import storage


storage_client = storage.Client()
@functions_framework.http
def translator(request):
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
    os.makedirs(MODEL_DIR, exist_ok=True)
    # Model and tokenizer file names
    model_files = [
        "config.json",
        "generation_config.json",
        "model.safetensors",
        "source.spm",
        "special_tokens_map.json",
        "target.spm",
        "tokenizer_config.json",
        "vocab.json"
    ]     
    if not os.listdir(MODEL_DIR):  # This checks if the directory is empty
        for file_name in model_files:
            download_model_files('cmpt-756-group-bucket', f"translator/{file_name}",os.path.join(MODEL_DIR, file_name))
    model = pipeline("translation", MODEL_DIR)
    output =model(input)[0].get("translation_text")
    print(output)

    return output

# Function to download model files from GCS
def download_model_files(bucket_name, source_blob_name, destination_file_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"{source_blob_name} downloaded to {destination_file_name}.")
    
    
# requirement.txt
# functions-framework==3.*
# google-cloud-storage==1.25.0
# scikit-learn==1.2.2
# transformers==4.38.2
# tensorflow
# sentencepiece

# https://us-central1-nice-beanbag-416418.cloudfunctions.net/translator    

# Sample Input
# {input:"你好吗？"}