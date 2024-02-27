# CMPT-756-Cloud: Containerized or Serverless Learning
Group member
- David He: [@dhe090](https://github.com/dhe090)
- Jason Mu: [@MuyunSai0920](https://github.com/MuyunSai0920)
- Jerry Wang: [@jerrybowang](https://github.com/jerrybowang)
- Roy Zhong: [@royroyzhong](https://github.com/royroyzhong)
- Barry Zhao: [@Barry7043](https://github.com/Barry7043)

## Project Description
We plan to leverage Google Cloud's Cloud Functions (serverless) and Cloud Run (containerized) to develop a straightforward web application for image recognition using the TensorFlow framework.

We will either utilize pretrained models or train the model using datasets provided by the TensorFlow framework. The model's accuracy should be above 65% based on training and testing data.

Once we obtain the model, we will integrate it into our application. The application will simply load the model and make predictions based on the input. Then, the application will send the predicted results back to the client.

The programming language for the application will be Python, utilizing the Flask library.

For containerized testing, we will test the application locally before deploying the image to the cloud. For serverless testing,  we will use Google Colab to mimic the request before deploying the function.

Our primary performance metric for comparison will be latency.
