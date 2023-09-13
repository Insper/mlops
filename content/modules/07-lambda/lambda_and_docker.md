# Lambda and Docker

## Introduction

We saw in [previous classes](../05-docker/intro.md) why Docker is important for ML. In this class, we will see how to create Docker images and deploy Lambda functions from them.

## Create Function

Consider the following lambda function code:

```python
import sys

def hello_from_docker(event, context):
    return {
        "created_by": "your name",
        "message": "Hello World!",
        "version": sys.version
    }
```

Our goal is to deploy this function with Docker + Lambda.

!!! danger "Important!"
    Create a folder for today's class and store the suggested files in the root of this folder

!!! exercise "Question"
    Save the source code above in `lambda_function.py` file.

!!! exercise "Question"
    Create a `requirements.txt` with some dummy dependencies like `textblob` or `pandas`.

    !!! danger ""
        For now, we will not use these dependencies, they will only serve as an example for the tasks at the end of the class.

## Create Image

!!! exercise "Question"
    Create a file `Dockerfile` with the content:

    !!! danger ""
        Notice:

        - The image used
        - The dependencies
        - The file with the handler

        See more images [Here](https://gallery.ecr.aws/lambda/python)

    ```docker
    FROM public.ecr.aws/lambda/python:3.10

    # Copy requirements.txt
    COPY requirements.txt ${LAMBDA_TASK_ROOT}

    # Copy function code
    COPY lambda_function.py ${LAMBDA_TASK_ROOT}

    # Install the specified packages
    RUN pip install -r requirements.txt

    # Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
    CMD [ "lambda_function.hello_from_docker" ]
    ```

Let's name the image `lambda-ex-image` and give it the `test` tag:

<div class="termy">

```console
$ docker build --platform linux/amd64 -t lambda-ex-image:test .
```

</div>

## Test locally

Before deploying, let's test the function locally Start the Docker image with the `docker run`` command.

<div class="termy">

```console
$ docker run -p 9500:8080 lambda-ex-image:test
```

</div>

Let's make a request with:

<div class="termy">

```console
$ curl "http://localhost:9500/2015-03-31/functions/function/invocations" -d '{}'
```

</div>

<br>
!!! tip "Tip!"
    If you prefer, make the request from Python with the `requests` library!

## Container Registry

The Amazon Elastic Container Registry (ECR) is a fully managed service that allows you to store, manage, and deploy container images. With ECR, you can securely store and manage your Docker container images.

Let's upload our image to ECR. But first, we need to create a container repository:

!!! danger "Atention!"
    Change the `repository_name` variable.
    
    Provide a name in the pattern `test1-mlops-<INSPER_USERNAME>`

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide a name like test1-mlops-<INSPER_USERNAME>
repository_name = "test1-mlops-xxxxx"

# Create a Boto3 client for ECR
ecr_client = boto3.client(
    "ecr",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

response = ecr_client.create_repository(
    repositoryName=repository_name,
    imageScanningConfiguration={"scanOnPush": True},
    imageTagMutability="MUTABLE",
)

print(response)

print(f"\nrepositoryArn: {response['repository']['repositoryArn']}")
print(f"repositoryUri: {response['repository']['repositoryUri']}")
```

!!! info "Important!"
    Write down the `repositoryUri`

## Upload Image to ECR

Before uploading our Docker image to ECR, we need to configure the AWS Command Line Interface (AWS CLI).

!!! info "Install!"
    See how to install [Here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

The AWS CLI can be used to interact with AWS via the command line, similar to what we are doing with `boto3` in Python.

For now, we will use the AWS CLI to enable authentication to `docker`.

After installing, run and provide the authentication keys for our account.

<div class="termy">

```console
$ aws configure
```

</div>
<br>

Let's authenticate and login to ECR using the Docker CLI:

!!! danger "Atention!"
    Change the `<AWS_ACCOUNT_ID>`, for example `123456789012`

<div class="termy">

```console
$ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-2.amazonaws.com
```

</div>

Then, we will run the `docker tag` command to tag our local Docker image into your Amazon ECR repository as the **latest** version by doing:

!!! danger "Atention!"
    Provide the `<REPOSITORY_URI>` from before

<div class="termy">

```console
$ docker tag lambda-ex-image:test <REPOSITORY_URI>:latest
```

</div>

<br>
And push image to ECR with:

!!! danger "Atention!"
    Provide the `<REPOSITORY_URI>` from before


<div class="termy">

```console
$ docker push 789828965675.dkr.ecr.us-east-2.amazonaws.com/test1-mlops-macielcv:latest
```

</div>


## Create Function

Now we can create the lambda function from the image already stored in the ECR.

To do this, run:

!!! danger "Atention!"
    Change the `function_name` and `image_uri`

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide function name: 
function_name = "ex_docker_<INSPER_USERNAME>"

# Provide Image URI from before
image_uri = ""

lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

response = lambda_client.create_function(
    FunctionName=function_name,
    PackageType="Image",
    Code={"ImageUri": image_uri},
    Role=lambda_role_arn,
    Timeout=30,  # Optional: function timeout in seconds
    MemorySize=128,  # Optional: function memory size in megabytes
)

print("Lambda function created successfully:")
print(f"Function Name: {response['FunctionName']}")
print(f"Function ARN: {response['FunctionArn']}")
```

!!! exercise "Question"
    Use the codes from the previous class as a reference and test the function.
    
    Call the lambda function directly, without creating an API in API Gateway.

!!! exercise "Question"
    Use the codes from the previous class as a reference and test the function.

Proceed to the APS!

## References

- https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions
- https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html