# Write Logs to S3

Some applications generate huge log loads, which makes local storage unfeasible. Furthermore, it is in the interest of companies that the logs are stored centrally, facilitating their use to generate improvements.

Therefore, it is interesting to store logs in AWS S3 storage. To do this, we will create a an in-memory stream for storing log data and write it to S3.

## Create Bucket

To create the bucket, use the code:

!!! danger "Provide function name"
    Change the `bucket_name` variable in the following source code: `log-bucket-YOUR_INSPER_USERNAME`

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide bucket name: log-bucket-YOUR_INSPER_USERNAME
bucket_name = ""

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION")},
)

```

## Generate Logs

Let's simulate log generation with the code:

!!! danger "Provide function name"
    Change the `bucket_name` variable in the following source code: `log-bucket-YOUR_INSPER_USERNAME`

```python
import io
import os
import logging
import boto3
from dotenv import load_dotenv

load_dotenv()

# Provide bucket name: log-bucket-YOUR_INSPER_USERNAME
bucket_name = ""
key = "log1"

# Function to write logs
def write_logs(body, bucket, key):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    s3.put_object(Body=body, Bucket=bucket, Key=key)


log = logging.getLogger("my_logger")
string_io = io.StringIO()
handler = logging.StreamHandler(string_io)
log.addHandler(handler)

try:
    # Simulate exception
    raise ValueError
except ValueError:
    log.error("Missing value")
    log.error("Some error occurred!")
finally:
    # Persists logs to s3
    write_logs(body=string_io.getvalue(), bucket=bucket_name, key=key)
```

## Check Logs

Let's read the logs generated to check if everything worked as it should:

```python
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Provide bucket name: log-bucket-YOUR_INSPER_USERNAME
bucket_name = ""
# Same key from previous source code
key = "log1"

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

obj = s3.get_object(Bucket=bucket_name, Key=key)

file_content = obj["Body"].read().decode("utf-8")

print("Stored log:")
print(file_content)

```

## Task

!!! exercise "Question"
    Configure logging in a local file in your batch processing activity.

    Think about appropriate log levels and use informative messages.

!!! exercise "Question"
    Configure logging to S3 in your batch processing activity.