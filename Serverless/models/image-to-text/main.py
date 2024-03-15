import functions_framework
from google.cloud import storage
from transformers import pipeline
import os

# Function to download model files from GCS
def download_model_files(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"{source_blob_name} downloaded to {destination_file_name}.")

@functions_framework.http
def image_to_text(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    # Main request handling
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    
    image = request.files['image']
    image_name = image.filename
    image.save(f"/tmp/{image_name}")

    bucket_name = "cmpt756-project-model-image-to-text"
    file_names = ["config.json", "generation_config.json", "model.safetensors", "preprocessor_config.json", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json", "vocab.txt"]
    # file_names = ["test.png", "config.json", "generation_config.json", "model.safetensors", "preprocessor_config.json", "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json", "vocab.txt"]
    local_dir_name = "/tmp"
    os.makedirs(local_dir_name, exist_ok=True)

    print(os.listdir(local_dir_name))
    
    if not os.path.exists(f"{local_dir_name}/model.safetensors"): # This checks if the directory is empty
        for file_name in file_names:
            download_model_files(bucket_name, f"test_to_image_model/{file_name}", os.path.join(local_dir_name, file_name))

    captioner = pipeline("image-to-text",local_dir_name)
    # result = captioner(f"{local_dir_name}/test.png")[0]['generated_text']
    result = captioner(f"/tmp/{image_name}")[0]['generated_text']
    return (result, 200, headers)