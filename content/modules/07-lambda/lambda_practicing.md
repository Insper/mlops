# AWS Lambda - Practicing

Let's create our own function in AWS Lambda.

## Create Folder

!!! exercise "Question"
    Create a new folder and store all the source code in it!

## Create `.env`

!!! exercise "Question"
    Create an `.env` file containing the variables:
    ```
    AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXX"
    AWS_SECRET_ACCESS_KEY="aaaaaaaaaaaaaaaaaaaaaaaaaaa"
    AWS_REGION="xx-xxxx-2"
    AWS_LAMBDA_ROLE_ARN="arn:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

    !!! tip "Tip!"
        Ask the professor for the new credentials!

## Create function

!!! exercise "Question"
    Create a file called `my_lambda.py` containing the function that will run on AWS.

    For now, we'll make a simple function that responds with a fixed JSON!

    Source code:
    ```python
    def say_hello(event, context):
        return {
            "created_by": "your name",
            "message": "Hello World!"
        }
    ```

    !!! tip "Tip!"
        The function `say_hello` will be our **handler** function.

## Create ZIP

!!! exercise "Question"
    Create a file called `my_lambda.zip` that is the compression `my_lambda.py`.

## Show functions

Let's use this code to list the functions available in our account:

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


# Call the list_functions API to retrieve all Lambda functions
response = lambda_client.list_functions()

# Extract the list of Lambda functions from the response
functions = response["Functions"]

print(f"You have {len(functions)} Lambda functions")


# Print the name of each Lambda function
if len(functions) > 0:
    print("Here are their names:")

for function in functions:
    function_name = function["FunctionName"]
    print(function_name)
```

!!! exercise "Question"
    Run the Python code and check out the functions currently available in our account!

## Create Lambda Function

Let's create a lambda function with:

!!! danger "Atention!"
    Change the `function_name` variable.
    
    Provide a name in the pattern `sayHello_<YOUR_INSPER_USERNAME>`

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide function name: sayHello_<YOUR_INSPER_USERNAME>
function_name = ""

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Lambda basic execution role
lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

# Read the contents of the zip file that you want to deploy
# Inside the "my_lambda.zip" there is a "my_lambda.py" file with the
# "say_hello" function code
with open("my_lambda.zip", "rb") as f:
    zip_to_deploy = f.read()

lambda_response = lambda_client.create_function(
    FunctionName=function_name,
    Runtime="python3.9",
    Role=lambda_role_arn,
    Handler="my_lambda.say_hello", # Python file DOT handler function
    Code={"ZipFile": zip_to_deploy},
)

print("Function ARN:", lambda_response["FunctionArn"])
```

!!! exercise long "Question"
    Run the Python code to create the function. Then write down the returned ARN

!!! exercise "Question"
    Rerun the code to display the existing functions in the account.

    Check that your function was created correctly.

## Check if worked

Let's check if the function worked:

!!! danger "Atention!"
    Change the `function_name` variable.

```python
import boto3
import os
import io
from dotenv import load_dotenv

load_dotenv()

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Lambda function name
# Provide function name: sayHello_<YOUR_INSPER_USERNAME>
function_name = ""

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

!!! exercise "Question"
    Make sure the function returns the expected result

This code provides a way to check if the lambda function works. However, when integrating it with other applications, its execution would probably depend on an event such as the creation of a file on S3 or an API call.

Let's check out how to use API Gateway to create an API for our Lambda function.
