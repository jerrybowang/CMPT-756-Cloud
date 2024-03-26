# CMPT-756-Cloud: Containerized or Serverless Learning
Group member
- David He: [@dhe090](https://github.com/dhe090)
- Jason Mu: [@MuyunSai0920](https://github.com/MuyunSai0920)
- Jerry Wang: [@jerrybowang](https://github.com/jerrybowang)
- Roy Zhong: [@royroyzhong](https://github.com/royroyzhong)
- Barry Zhao: [@Barry7043](https://github.com/Barry7043)

## Project Description
The application will host four deep-learning models we found online (text translation, text-to-speech, sentiment analysis, image-to-text). Application requires large storage, memory, and computation.

### Solution Design
#### Containerized
System Component:
- Pre-trained Models
- Docker image
- Google Cloud Container (google cloud run)

Communications Among Components:
- All components communicate with corresponding API calls inside the container
- Application inside the container will send the result back to client

Reason for Choice:

We choose google cloud run because easy management and auto scaling

We choose to include models in the image to minimize additional external network traffic. While the recommended practice is to deploy each model as separate containers, doing so would end up with similar implementations from the Serverless team, thereby defeating the purpose of comparison. Furthermore, we aim to assess the impact of large image files on the overall service model.


#### Serverless
System Components:
Google Function

Reason: Google Cloud Functions are designed for event-driven architectures. It is well-suited for reacting to environmental changes without manual scaling.

Storage:  Google Cloud Bucket

Reason: GCS is designed for high throughput and low latency access to object data, which is more suitable for serving deep learning models.

Communication:

Client -> Google Functions -> Google Storage ->  Google Functions -> Client


### Evaluation Plan
For both service models, we will measure their latency, storage usage, internal and external network usage, and conduct a bill analysis to determine which part of the service model uses the most resources. We will conduct three tests/scenarios: idle, evenly distributed service requests, and skewed service requests. After obtaining the results, we will evaluate the pros and cons of each service model to decide which one better suits our application needs.