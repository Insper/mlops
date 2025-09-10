# SQS Practicing

## Introduction

Let's practice using the SQS service. Initially we will create a queue and interact with it using Python **locally**, on our own machine.

## Create Queue

Let's create a **SQS** queue with:

!!! danger "Atention!"
    Change the `queue_name` variable.
    
    Provide a name in the pattern `message_queue_<YOUR_INSPER_USERNAME>`.

=== "With Python"
    ```python
    import os
    import boto3
    from dotenv import load_dotenv

    load_dotenv()

    # Queue name: message_queue_<YOUR_INSPER_USERNAME>
    queue_name = ""

    # Create a Boto3 client for AWS Lambda
    sqs_client = boto3.client(
        "sqs",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Create a new SQS queue
    response = sqs_client.create_queue(
        QueueName=queue_name,
        Attributes={
            "DelaySeconds": "0",
            "MessageRetentionPeriod": "3600",  # 1 hour in seconds (could be days in real applications)
        },
    )

    # Get the queue URL
    queue_url = response["QueueUrl"]

    print("SQS queue created with URL:", queue_url)
    ```

=== "With AWS CLI"
    !!! danger "Attention!"
        Export the required environment variables.

    <p>
    <div class="termy">

    ```console
    $ aws sqs create-queue \
        --queue-name message_queue_YOUR_INSPER_USERNAME \
        --attributes DelaySeconds=0,MessageRetentionPeriod=3600 \
        --region $AWS_REGION \
        --profile mlops
    ```

    </div>
    </p>

!!! exercise long "Question"
    Run the Python code to create the queue. Then write down the returned URL

## Checking Queue

Let's check basic information such as the number of messages available in the queue.

!!! danger "Atention!"
    Change the `queue_url` variable, returned before.


=== "With Python"
    ```python
    import os
    import boto3
    from dotenv import load_dotenv

    load_dotenv()

    # Replace with your queue URL or name
    queue_url = ""

    # Create a Boto3 client for AWS Lambda
    sqs_client = boto3.client(
        "sqs",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )


    # Get the attributes of the SQS queue
    response = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["All"])

    # Extract the desired attributes from the response
    attributes = response["Attributes"]
    approximate_message_count = attributes["ApproximateNumberOfMessages"]
    approximate_message_not_visible_count = attributes[
        "ApproximateNumberOfMessagesNotVisible"
    ]

    print("Approximate number of visible messages:", approximate_message_count)
    print(
        "Approximate number of messages not visible:", approximate_message_not_visible_count
    )
    ```

=== "With AWS CLI"
    <p>
    <div class="termy">

    ```console
    $ aws sqs get-queue-attributes \
        --queue-url QUEUE_URL \
        --attribute-names All \
        --region $AWS_REGION \
        --profile default
    ```

    </div>
    </p>

!!! exercise "Question"
    Run the Python code to verify the queue.
    
    Make sure it is empty!

## Send Messages to Queue

To send messages to the queue, we will use:

!!! danger "Atention!"
    Change the `queue_url` variable, returned before.

```python
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Replace with your queue URL or name
queue_url = ""

# Change the message!
message = "I love Python"

# Create a Boto3 client for AWS Lambda
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


# Send a message to the SQS queue
response = sqs_client.send_message(
    QueueUrl=queue_url,  # Replace with your queue URL or name
    MessageBody=message,
)

# Get the message ID from the response
message_id = response["MessageId"]

print("Message sent with ID:", message_id)
```

!!! exercise "Question"
    Run the Python code to send messages to queue (as seen before).
    
    Change the message text and, after each sending, check if the number of messages in the queue changes.

## Consuming Messages

To read messages from the queue, we will use:

!!! danger "Atention!"
    Change the `queue_url` variable, returned before.

```python
import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

# Replace with your queue URL or name
queue_url = ""

# Create a Boto3 client for AWS Lambda
sqs_client = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Receive messages from the SQS queue
response = sqs_client.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    VisibilityTimeout=60,  # Timeout in seconds before the message becomes visible again
    WaitTimeSeconds=20,  # Wait up to 20 seconds for a message to be available
)

# Process received messages
for message in response.get("Messages", []):
    message_text = message["Body"]

    # Print the message
    print(f"Received message: {message_text}")

    # Delete the processed message from the SQS queue
    sqs_client.delete_message(
        QueueUrl=queue_url,  # Replace with your queue URL or name
        ReceiptHandle=message["ReceiptHandle"],
    )
```

!!! exercise "Question"
    Run the Python code to read messages from queue.
    
    Check whether the number of messages in the queue changes.

    Send new messages if necessary!