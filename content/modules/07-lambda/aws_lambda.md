# AWS Lambda

## FaaS

**Function as a Service** (FaaS) refers to a *cloud computing* model that allows developers to build and run applications and functions *without having to worry about infrastructure management*.

With **FaaS**, developers are able to deploy their code in the form of stateless functions or event handlers that can be invoked on-demand or in response to events.

!!! info "Info!"
    **FaaS** is considered a form of serverless computing. The **FaaS** platform takes care of:
    
    - Underlying servers
    - Operating systems and platforms
    - Scaling and operating the application
    
    Making it simple for developers to **focus** only on writing code for their specific business logic or tasks.

## Market solutions

The main providers of **FaaS** platforms include:

- **AWS Lambda**

- **Google Cloud Functions**

- **Microsoft Azure Functions**

We will work with AWS Lambda!

## AWS Lambda

**AWS Lambda** is Amazon's flagship serverless computing platform that runs your code on high-availability compute infrastructure and performs all the administration of the compute resources.

The Lambda functions can be *triggered* by various events like changes to an S3 bucket or database tables, calls from API Gateway or third party applications, or on a schedule. 

## Advantages

Some reasons why Lambda functions should be considered to deploy ML applications:

- **Scalability**: Lambda can automatically scale up or down to handle varying loads. This is important for ML models that may see bursty traffic or need to handle prediction requests at scale.

- **Event-driven**: Lambda functions can be easily triggered by events like incoming data. This makes it simple to run ML predictions every time new data comes in without managing servers.

- **Pay-per-use**: with Lambda, you only pay for the compute resources used to run your code. This saves costs for ML workloads that may be intermittent or only needed during model training cycles.

- **No servers to manage**: Lambda handles all the infrastructure maintenance, so you can focus on coding your ML logic without worrying about servers, scaling, availability etc.

- **Deployment flexibility**: you can host complex ML pipelines or prediction code on Lambda. Models can also be deployed as REST APIs using API Gateway for low-latency predictions.


## Disadvantages

**AWS Lambda** may not always be the best choice for ML applications due to:

- **Limited memory/compute**: Lambda functions have strict memory limits ranging from 128MB to 10240MB. ML models often require much more RAM.

- **Cold start**: when a Lambda function hasn't been invoked in awhile, the first invocation takes longer due to container initialization. This may not be suitable for real-time ML inferences.

- **Stateful dependencies**: Lambda functions are stateless by design. Supporting stateful dependencies like databases for ML model training is challenging.

- **Long-running workloads**: ML model training typically involves batch processing large datasets over long periods which exceeds Lambda's 15 minute timeout limit.

- **GPU/TPU support**: Lambda doesn't support hardware accelerators like GPUs which are essential for many deep learning workloads.
