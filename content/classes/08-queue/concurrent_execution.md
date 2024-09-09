# Concurrent Executions

## Testing Concurrent Executions

In this activity, we will find out what happens when the concurrent execution limit is reached during the execution of lambda functions.

## Create Lambda Function

Consider the following source code. In it, we use `time.sleep` to simulate a time-consuming function.

```python
"""
Simulating a slow processing function
"""
import time


def do_something(event, context):
    """This is the main function (handler)
    that will be called by AWS Lambda."""
    # Simulate slow processing
    time.sleep(5)
    return {
        "created_by": "your name",
        "message": "data was processed",
    }


```

!!! exercise "Question"
    Save this code in `lambda_proc.py` and create a **ZIP** `lambda_proc.zip` file.

Let's create a lambda function with:

!!! danger "Atention!"
    Change the `function_name` variable.
    
    Provide a name in the pattern `do_something_concurrent_<YOUR_INSPER_USERNAME>`.

=== "With Python"
    ```python
    import os
    import boto3
    from dotenv import load_dotenv

    load_dotenv()

    # Lambda function name: do_something_concurrent_<YOUR_INSPER_USERNAME>
    function_name = ""
    # Timeout in seconds. Default is 3.
    timeout = 15
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
    with open("lambda_proc.zip", "rb") as f:
        zip_to_deploy = f.read()

    lambda_response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime="python3.10",
        Role=lambda_role_arn,
        Handler="lambda_proc.do_something",
        Code={"ZipFile": zip_to_deploy},
        Timeout=timeout,
    )

    print("Function ARN:", lambda_response["FunctionArn"])
    ```

=== "With CLI"

    !!! danger "Attention!"
        Before using the command, make sure you have exported (according to the terminal you are using) the variables `AWS_LAMBDA_ROLE_ARN` and `AWS_REGION`.

        An alternative is to check the values ​​used in the previous classes and leave them fixed in the command!

    <p>
    <div class="termy">

    ```console
    $ aws lambda create-function \
        --function-name do_something_concurrent_<YOUR_INSPER_USERNAME> \
        --runtime python3.10 \
        --role $AWS_LAMBDA_ROLE_ARN \
        --handler lambda_proc.do_something \
        --zip-file fileb://lambda_proc.zip \
        --timeout 15 \
        --region $AWS_REGION \
        --profile mlops
    ```

    </div>
    </p>

!!! info "Important!"
    Note that we defined a new argument: `Timeout`. See more information in the documentation [Here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/client/create_function.html)

!!! exercise short "Question"
    Run the Python code to create the function. Then write down the returned ARN

!!! exercise "Question"
    Run the code from previous classes to display the existing functions in the account.

    Make sure that your function is on the list.

## Configure Limits

As your functions receive more requests, Lambda [**automatically handles scaling**](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html) the number of execution environments until you reach your account's concurrency limit.

To test what happens when the limit is reached, let's set up a limit at the function level. We will use a small value for learning purposes only!

In order todo that, use:

!!! danger "Atention!"
    Change the `function_name` variable to the same as used before: `do_something_concurrent_<YOUR_INSPER_USERNAME>`.

=== "With Python"
    ```python
    import os
    import json
    import boto3
    from dotenv import load_dotenv

    load_dotenv()

    # Lambda function name: do_something_concurrent_<YOUR_INSPER_USERNAME>
    function_name = ""

    # Number of concurrent executions: 2
    concurrent_executions_limit = 2

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Set limits
    lambda_response = lambda_client.put_function_concurrency(
        FunctionName=function_name, ReservedConcurrentExecutions=concurrent_executions_limit
    )

    # JSON pretty print!
    json_formatted_str = json.dumps(lambda_response, indent=2)

    print(f"Response:\n{json_formatted_str}")
    ```

=== "With AWS CLI"
    !!! danger "Attention!"
        Before using the command, make sure you have exported (according to the terminal you are using) the variables `AWS_LAMBDA_ROLE_ARN` and `AWS_REGION`.

        An alternative is to check the values ​​used in the previous classes and leave them fixed in the command!

    !!! danger "Attention!"
        Remember to change the **function name** in `do_something_concurrent_<YOUR_INSPER_USERNAME>`

    <p>
    <div class="termy">

    ```console
    $ aws lambda put-function-concurrency \
        --function-name do_something_concurrent_YOUR_INSPER_USERNAME \
        --reserved-concurrent-executions 2 \
        --region $AWS_REGION \
        --profile default
    ```

    </div>
    </p>

!!! exercise "Question"
    Use the provided code to set a concurrent execution limit for your lambda function.

## Testing the function

Let's make multiple simultaneous calls and check if the function responds correctly. Use the code:

!!! danger "Atention!"
    Change the `function_name` variable to the same as used before: `do_something_concurrent_<YOUR_INSPER_USERNAME>`.

```python
import concurrent.futures
import boto3
import os
import io
from dotenv import load_dotenv

load_dotenv()

# Lambda function name: do_something_concurrent_<YOUR_INSPER_USERNAME>
function_name = ""

# Define the number of concurrent executions/calls
num_executions = 10

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


try:
    # Create a thread pool executor with the desired number of threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_executions) as executor:
        # List to store the future objects
        futures = []

        # Submit the Lambda invocations to the executor
        for _ in range(num_executions):
            future = executor.submit(
                lambda_client.invoke,
                FunctionName=function_name,
                InvocationType="RequestResponse",
            )
            futures.append(future)

        # Process the results as they become available
        for future in concurrent.futures.as_completed(futures):
            print("-" * 40)
            response = future.result()
            payload = response["Payload"]
            txt = io.BytesIO(payload.read()).read().decode("utf-8")
            print(f"Response:\n{txt}")

except Exception as e:
    print(e)

```

!!! exercise long "Question"
    What happens if there are too many calls to a lambda function, so that the concurrency limit is reached?

    !!! answer "Answer!"
        Calls that exceed the limit are not executed. The client or the invoker receives a response that the rate limit has been reached.

!!! exercise short "Question"
    Who is responsible for handling functions that failed due to rate limit?

    !!! answer "Answer!"
        It is the responsibility of the client or the invoker of the Lambda function to handle rate limiting and retries.

!!! exercise "Question"
    Change the variable `num_executions` to `2` and run again.
    
    Let's ensure that the function responds, as long as it is below the rate limit!

## Handle Rate Limiting

To handle rate limiting and retries effectively, you can implement error handling and retry mechanisms in your application code.

Another option is to use **queues**. In previous classes, we have already implemented **RabbitMQ** as a queuing/messaging service between ML applications. In this class, we look at solutions on AWS, such as **Amazon Simple Queue Service (SQS)**.

## Decoupling

Decoupling refers to designing components or services in a system so that they are loosely coupled, meaning they have **minimal dependencies** on each other. In a decoupled architecture, components can operate independently, allowing for better scalability, flexibility, and resilience.

AWS Lambda and SQS play a significant role in achieving decoupling within a system. Advance to the next topic!