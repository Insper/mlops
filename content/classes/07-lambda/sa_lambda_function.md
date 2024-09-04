# Lambda Function for Sentment Analysis (SA)

Let's create a lambda function that uses the `textblob` library to return the polarity of a text.

But first, let's configure the AWS CLI so we have another way to interact with our resources created in AWS.

## AWS CLI - Command Line Interface

### Install

[**Click Here**](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install AWS CLI.

### Configure

Configure the region and credentials provided by the professor.

<div class="termy">

    ```console
    $ aws configure --profile mlops
    AWS Access Key ID [None]: ????????????
    AWS Secret Access Key [None]: ????????????????????????????????
    Default region name [None]: us-east-2
    Default output format [None]: 
    ```

</div>
<br>

### Set profile

To set a default profile, use:

=== "Linux"

    <div class="termy">

    ```console
    $ export AWS_PROFILE=mlops
    ```

    </div>
    <br>

=== "Windows CMD (Command Prompt)"

    <div class="termy">

    ```console
    $ set AWS_PROFILE=mlops
    ```

    </div>
    <br>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ env:AWS_PROFILE="mlops"
    ```

    </div>
    <br>

### Example: list Lambda functions

You can now use the AWS CLI to create, list, or remove resources. For example, to list the names of lambda functions:

<div class="termy">

    ```console
    $ aws lambda list-functions --query "Functions[*].FunctionName" --output text
    ```

</div>
<br>

From here on, you can research how to do with the AWS CLI what we did with `boto3` library.

## Create source code

!!! exercise "Question"
    Create a file `polarity.py` containing a Lambda function `get_polarity` that receives a JSON in the request body and returns a JSON containing:

    - The received sentence itself
    - The polarity returned by `TextBlob`
    - The feeling of the sentence.
        - If the polarity is below `-0.8`, consider it as negative sentiment.
        - If the polarity is between `-0.8` and `0.2`, consider it neutral sentiment.
        - If the polarity is above `0.2`, consider it as positive sentiment.

    Once finished, check your code with the official answer provided below.

??? "Official answer for `polarity.py`"
    ```python
    from textblob import TextBlob
    import json


    def get_polarity(event, context):
        # Provide a body for the request!
        if "body" not in event:
            return {"error": "No body provided"}

        # Get the raw posted JSON
        raw_json = event["body"]

        # Load it into a Python dict
        body = json.loads(raw_json)

        if "phrase" not in body:
            return {"error": "No phrase provided"}

        phrase = body["phrase"]

        # Create a TextBlob object of the phrase
        blob = TextBlob(phrase)

        # Get the polarity score
        polarity = blob.polarity

        # Create a response object with the phrase and polarity
        res = {"phrase": phrase, "polarity": str(polarity)}

        # Determine the sentiment
        if polarity > 0.2:
            res["sentiment"] = "Positive sentiment"
        elif polarity >= -0.8:
            res["sentiment"] = "Neutral sentiment"
        else:
            res["sentiment"] = "Negative sentiment"

        return res
    ```

!!! Exercise "Question"
    Do as in the last class, create a ZIP of your Python file to deploy to AWS Lambda.

## Create Lambda function

!!! danger "Atention!"
    Change the `function_name` variable.
    
    Provide a name in the pattern `get_polarity_<YOUR_INSPER_USERNAME>`

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Lambda function name
# Provide a name in the pattern `get_polarity_<YOUR_INSPER_USERNAME>`
function_name = ""

# Lambda basic execution role
lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Read the contents of the zip file that you want to deploy
with open("polarity.zip", "rb") as f:
    zip_to_deploy = f.read()

lambda_response = lambda_client.create_function(
    FunctionName=function_name,
    Runtime="python3.10", # Change the runtime if you want!
    Role=lambda_role_arn,
    Handler="polarity.get_polarity",  # function get_polarity inside polarity.py
    Code={"ZipFile": zip_to_deploy},
)

print("Function ARN:", lambda_response["FunctionArn"])
```

## Check if worked

Before creating the API, let's check if the Lambda function works correctly!

To do this, let's make a direct call to the function with:

!!! danger "Atention!"
    Change the `function_name` variable with the same name as before.

```python
import boto3
import os
import io
from dotenv import load_dotenv

load_dotenv()

# Lambda function name
function_name = ""

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


try:
    # Invoke the function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
    )

    payload = response["Payload"]

    txt = io.BytesIO(payload.read()).read().decode("utf-8")
    print(f"Response:\n{txt}")
except Exception as e:
    print(e)
```

!!! Exercise short "Question"
    The call must not have worked. What error is returned?
    
    !!! answer "Answer!"
        Among others:
        ```python
        {
            "errorMessage": "Unable to import module 'polarity': No module named 'textblob'"
        }
        ```

This occurred because our function depends on a library `textblob` that is not available in the environment where it is being executed.

## Runtime dependencies

In AWS Lambda, when our Python code depends on another package or module, two options are:

1. Include the dependencies in the ZIP
1. Use Lambda layer

Let's work with the second option! Proceed to the next topic.
