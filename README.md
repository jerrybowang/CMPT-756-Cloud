# CMPT-756-Cloud: Containerized or Serverless Learning
Group member
- David He: [@dhe090](https://github.com/dhe090)
- Jason Mu: [@MuyunSai0920](https://github.com/MuyunSai0920)
- Jerry Wang: [@jerrybowang](https://github.com/jerrybowang)
- Roy Zhong: [@royroyzhong](https://github.com/royroyzhong)
- Barry Zhao: [@Barry7043](https://github.com/Barry7043)

## Project Description
The purpose of this project is to evaluate the fit of each deployment choice (containerized and serverless environments) for our Machine Learning application.

## System design
The stateless web application will host four deep-learning models we found online: text translation, text-to-speech, sentiment analysis, and image-to-text. We build this application using Python and Flask as our main framework and utilize the corresponding Model APIs (Huggingface, Scikit-learn, TensorFlow, PyTorch) required by the pre-trained models.

Each model service will have its own entry URL or subroute (e.g., 'localhost:8080/translate'). The GET request will show the user a simple HTML form asking for user input. Once the user hits the submit button, the data will be sent to the server via a POST request.

Upon submission of the user's request, the application will load the relevant model and generate predictions based on the input. Then, it will transmit the predicted results back to the client.

The application requires large storage, memory, and computation. After testing the application to ensure it functions properly, we are ready to implement a containerized and serverless version of this application.

## Implementation Details

### Containerized

To implement our application in a containerized environment, we use Docker to containerize this application. For the model storage inside the container, we copy the model files into the Docker image. Once the container is running, the respective model API will directly load the model stored within the Docker image. We uploaded our Docker image onto Docker Hub, enabling access for Google Cloud Run.

For cloud deployment, we chose Google Cloud Run because of its easy management and auto-scaling feature. No manual monitoring or scaling is needed when there is an increase in requests. When a user accesses the application URL, Google Cloud Run will instantiate a container using our Docker image if no running containers are available.

We chose to include all models in the image as an “all in one” implementation. While the recommended practice is to deploy each model as separate containers, doing so would result in a similar approach to the serverless implementation. This would defeat the purpose of comparison. Moreover, we aim to evaluate the effect of large image files on the overall service model.

### Serverless

Unlike traditional server and containerized environments, serverless environments don’t have a central “server” to process user requests. Thus, we need to split each model service into different functions. Each function will have its own entry URL.

When we deploy our functions’ source code to Cloud Functions, Cloud Build automatically builds the code into container images and pushes those images to the Artifact Registry. When Cloud Functions sense a user request for a specific model service via HTTP requests, it accesses the image to run the container in order to execute the corresponding function. This finding leads us to choose the 'all in one' approach for the container side, and also serves as another comparison for “all in one” and “separate” implementation decisions.

As for model storage for each Cloud Function, we manually upload the models to Google Cloud Bucket. During a function cold start, the function downloads model files from Google Cloud Bucket to a local folder. The corresponding model API then loads the model and makes predictions based on the user input, and returns the result to the client. In the warm start scenario, the model API directly accesses the locally stored model, runs it, and provides the result back to the client. This approach optimizes performance by minimizing resource usage during subsequent requests after the initial setup.

## Measurements
For both service models, we will measure their latency, storage usage, and conduct a billing analysis to determine which service model uses the most resources. We will conduct three tests/scenarios: idle, evenly distributed service requests, and targeted service requests.

For idle scenarios, we will deploy the application and do nothing. This scenario aims to assess the cost when we don’t have any requests. During deployment, we will make efforts to avoid incurring unnecessary charges, ensuring that only essential fees are included in our measurements. (eg. Minimum always active instance = 0; Assign CPU only when active; etc)

For evenly distributed service requests, a Python script is used to send five sequential requests for each model service. This means applications need to handle four different requests simultaneously, repeated five times. This test aims to assess service models' latency under normal conditions. All models are included in this test to eliminate biases.

For targeted service requests, a Python script is used to send 20 requests to the translator service. These requests will be conducted in two scenarios: sequential (requests sent one after another) and burst (20 requests sent simultaneously). This test aims to assess service models' latency under long continuous requests and traffic bursts for skewed service requests.

All tests will be conducted using three hardware tiers, each with a different number of CPUs (2/4/8) and fixed 8GB of memory. Maximum concurrent requests per instance for both service models were set to 20 to minimize new instance spawning due to increasing requests.
