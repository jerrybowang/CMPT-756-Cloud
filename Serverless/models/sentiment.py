import functions_framework
from flask import make_response
import requests
import pickle
import sklearn
from google.cloud import storage
import os

@functions_framework.http
def sentiment(request):
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
    # This checks if the directory is empty
    os.makedirs("/tmp", exist_ok=True)
    if not os.path.exists("/tmp/textclassifier_sentiment.pickle"): 
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('cmpt-756-group-bucket')
        blob_classifier = bucket.blob('models/textclassifier_sentiment.pickle')
        blob_scaler = bucket.blob('models/tfidfmodel.pickle')
        blob_classifier.download_to_filename('/tmp/textclassifier_sentiment.pickle')
        blob_scaler.download_to_filename('/tmp/tfidfmodel.pickle')


    serverless_classifier = pickle.load(open('/tmp/textclassifier_sentiment.pickle', 'rb'))
    serverless_scaler = pickle.load(open('/tmp/tfidfmodel.pickle', 'rb'))
    request_json = request.get_json(silent=True)
    if request_json and 'string' in request_json:

        string_to_predict = request_json['string']

        # Convert the preprocessed string into a numerical representation
        numerical_representation = serverless_scaler.transform([string_to_predict])

        # Predict the sentiment of the string
        predicted_sentiment = serverless_classifier.predict(numerical_representation)
        review="Bad Review" if predicted_sentiment[0] == 0 else "Good Review"

        # Print the predicted sentiment
        return(f"The input string {string_to_predict} is : {review}",200,headers)    
    else:
        return ("Invalid or missing JSON payload",400,headers)




# requirement.txt
# functions-framework==3.*
# google-cloud-storage==1.25.0
# scikit-learn==1.2.2


# https://us-east1-nice-beanbag-416418.cloudfunctions.net/sentiment

# Sample Input
# {string:"I love this"}

