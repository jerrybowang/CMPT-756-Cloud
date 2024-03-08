import functions_framework
from flask import make_response
import requests
import pickle
from google.cloud import storage
import numpy as np
import sklearn

@functions_framework.http
def hello_http(request):
    # Preflight request handling for CORS
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

    request_json = request.get_json(silent=True)
    
    # Ensure request_json is not None and has all required keys
    if request_json and all(key in request_json for key in ['male', 'age', 'salary', 'price']):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('myfirstbucketr_royzhong')
        blob_classifier = bucket.blob('models/knn_model.pickle')
        blob_scaler = bucket.blob('models/scaler.pickle')
        blob_classifier.download_to_filename('/tmp/knn_model.pickle')
        blob_scaler.download_to_filename('/tmp/scaler.pickle')
        
        serverless_classifier = pickle.load(open('/tmp/knn_model.pickle', 'rb'))
        serverless_scaler = pickle.load(open('/tmp/scaler.pickle', 'rb'))

        male = request_json['male']
        age = request_json['age']
        salary = request_json['salary']
        price = request_json['price']

        row_values = [male, age, salary, price]
        x_new = np.array(row_values).reshape(1, -1)
        x_new_scaled = serverless_scaler.transform(x_new)
        y_new_pred = serverless_classifier.predict(x_new_scaled)
        prediction = str(y_new_pred[0])

        return (f"The prediction is {prediction}", 200, headers)
    else:
        return ("Invalid or missing JSON payload", 400, headers)
