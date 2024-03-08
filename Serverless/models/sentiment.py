import functions_framework
from flask import make_response
import requests
import pickle
import sklearn
from google.cloud import storage


@functions_framework.http
def sentiment(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
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
        return(f"The input string {string_to_predict} is : {review}")    
    else:
        return ("Invalid or missing JSON payload")



# requirement.txt
# functions-framework==3.*
# google-cloud-storage==1.25.0
# scikit-learn==1.2.2


# https://us-east1-nice-beanbag-416418.cloudfunctions.net/sentiment

# Sample Input
# {string:"I love this"}

