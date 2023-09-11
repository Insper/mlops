# Lambda Layer

## Introduction

A [AWS Lambda layer](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html) is a ZIP file that contains supplementary code, such as library dependencies.

The main advantages of using Lambda layers [are](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html):

- **Reduce size of deployment packages**: Rather than packaging function dependencies directly with your function code, isolate dependencies into reusable layers. This keeps deployment packages small and organized.

- **Separete core function logic from dependencies**: Using layers allows function logic and dependencies to evolve separately. Layers facilitate independent management, where dependencies can be revised without touching function code. This allows deployment packages for your functions to focus solely on application logic without the bloat of bundled dependencies.

- **Share dependencies across multiple functions**: By building dependencies into layers, those components can then be associated with multiple functions simultaneously (layers are reusable). Once a layer is established, any function configuration can reference and inherit its dependencies, rather than requiring redundant inclusion in each deployment package definition.

Check the diagram for a comparison of the model without versus with the use of layers.

![](lambda-layers-diagram.png)

!!! tip "Tip!"
    Lambda layers provide a convenient and effective way to package code libraries for sharing with Lambda functions in your account.

!!! progress "Click to continue"

## Creating the ZIP with dependencies

Let's create a ZIP file with our project's dependencies and create a layer from it.

As you are probably in a Windows environment (and to standardize the class), we will use *Ubuntu* *Docker* and create dependencies from it.

To start a container in interactive mode, use:

<div class="termy">

    ```console
    $ docker run -it ubuntu
    ```

</div>

<br>

!!! danger "Atention!"
    The next commands will be executed inside the container!

Then, install the version of Python used by your Lambda functions and the ZIP:

<div class="termy">

    ```console
    $ apt update
    $ apt install python3.10 python3-pip zip
    ```

</div>

<br>

Create a folder to store the dependencies and install then:

<div class="termy">

    ```console
    $ mkdir -p layer/python/lib/python3.10/site-packages
    $ pip3 install textblob -t layer/python/lib/python3.10/site-packages

    ```

</div>

<br>

Create the ZIP with dependencies:

<div class="termy">

    ```console
    $ cd layer
    $ zip -r polarity_layer_package.zip *

    ```

</div>

<br>

Check the results:

<div class="termy">

    ```console
    $ ls -la
    total 5820
    drwxr-xr-x 3 root root    4096 Sep 08 15:02 ./
    drwxr-xr-x 1 root root    4096 Sep 08 15:00 ../
    -rw-r--r-- 1 root root 5945036 Sep 08 15:02 polarity_layer_package.zip
    drwxr-xr-x 3 root root    4096 Sep 08 15:00 python/

    ```

</div>

<br>

!!! danger "Atention!"
    The next commands will be executed outside the container!

Now, let's extract the ZIP out of the container! To do this, we need to find out the container ID: and call the  `docker cp` command.

<div class="termy">

    ```console
    $ docker ps -a
    CONTAINER ID   IMAGE                       COMMAND
    ba7a7aba2b95   ubuntu                      "/bin/bash"
    ```

</div>

<br>

With the container ID, we then call the `docker cp` command: `docker cp <Container-ID:path_of_zip_on_container>   <path_where_you_want_to_copy_the_zip>`

For example:

<div class="termy">

    ```console
    $ docker cp ba7a7aba2b95:/layer/polarity_layer_package.zip ./
    ```

</div>

<br>

## Create Layer

Now that we have the ZIP with the dependencies, let's create the layer with:

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide a name following the pattern `layer_polarity_<YOUR_INSPER_USERNAME>`
layer_name = ""

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Read the contents of the zip file that you want to deploy
with open("polarity_layer_package.zip", "rb") as f:
    zip_to_deploy = f.read()


lambda_response = lambda_client.publish_layer_version(
    LayerName=layer_name,
    Description="Layer with textblob for polarity",
    Content={"ZipFile": zip_to_deploy},
)

print("Layer ARN:\n", lambda_response["LayerArn"])
print("Layer LayerVersionArn:\n", lambda_response["LayerVersionArn"])
```

!!! info "Important!"
    Copy the `LayerVersionArn` as it will be used.

## Assign Layer

Let's link the Lambda function we created to the layer. To do this:


!!! danger "Important!"
    Provide the `layer_version_arn` and `function_name` copied previously.

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide ARN and function name
layer_version_arn = (
    "xxxxxxxxxxx"
)
function_name = "xxxxxxx"

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Get the current configuration of the Lambda function
response = lambda_client.get_function(FunctionName=function_name)

# Retrieve the existing layers
layers = (
    response["Configuration"]["Layers"] if "Layers" in response["Configuration"] else []
)

print("Existing layers:")
print(layers)

# Append the layer ARN to the existing layers
layers.append(layer_version_arn)

# Update the function configuration with the new layers
lambda_response = lambda_client.update_function_configuration(
    FunctionName=function_name, Layers=layers
)

# Print response
print("Lambda response:\n", lambda_response)
```

## Check if worked!

!!! Exercise short "Question!"
    Call the Lambda function, as [we did here](sa_lambda_function.md#check-if-worked) and check if it works. What was the result obtained?

    !!! answer "Answer!"
        Response:
        ```python
        {
            "error": "No body provided yet"
        }
        ```
        
        So the textblob seems to be being imported and the error is not sending the JSON with the data in the request.

## Create API Gateway

Let's create an API with:

```python
import boto3
import os
from dotenv import load_dotenv
import random
import string


load_dotenv()

# Provide function name and ARN copied previously
lambda_function_name = ""
lambda_arn = ""

# Provide a name following the pattern `demo_polarity_<YOUR_INSPER_USERNAME>`
api_gateway_name = "demo-polarity-xxxxxxxx"

id_num = "".join(random.choices(string.digits, k=7))

api_gateway = boto3.client(
    "apigatewayv2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

lambda_function = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

lambda_function_get = lambda_function.get_function(FunctionName=lambda_function_name)

print(lambda_function_get)

api_gateway_create = api_gateway.create_api(
    Name=api_gateway_name,
    ProtocolType="HTTP",
    Version="1.0",
    RouteKey="POST /polarity", # Create a /polarity POST route
    Target=lambda_function_get["Configuration"]["FunctionArn"],
)

api_gateway_permissions = lambda_function.add_permission(
    FunctionName=lambda_function_name,
    StatementId="api-gateway-permission-statement-" + id_num,
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
)

print("API Endpoint:", api_gateway_create["ApiEndpoint"])
```

!!! info "Important!"
    Copy the endpoint and edit in the following code.

And test by sending any text to obtain its polarity:

```python
import requests

# Change the endpoint
url_endpoing = "https://xxxxxxxxxx.execute-api.us-east-2.amazonaws.com"

url = f"{url_endpoing}/polarity"

# Change the phrase
body = {"phrase": "This was the worst movie I watched this year, horrible!"}

resp = requests.post(url, json=body)

print(f"status code: {resp.status_code}")
print(f"text: {resp.text}")
```

!!! Exercise "Question!"
    Check if the result was as expected:

    ```python
    {
        "phrase": "This was the worst movie I watched this year, horrible!",
        "polarity": "-1.0",
        "sentiment": "Negative sentiment"
    }
    ```

## Cleaning

If you have finished the class, delete the resources created in API Gateway and Lambda.

!!! tip "Tip!"
    After deleting, use the listing commands (from the previous class) to check that there is in fact no other resource created by you!

Deleting API Gateway:

!!! Danger
    Provide the `api_gateway_name` copied previously.

```python
import boto3
import os
from dotenv import load_dotenv
import random
import string


load_dotenv()

# Provide API Gateway name used previously
api_gateway_name = "demo-polarity-xxxxxxx"

api_gateway = boto3.client(
    "apigatewayv2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


response = api_gateway.get_apis(MaxResults="2000")
api_gateway_id = None
for item in response["Items"]:
    if item["Name"] == api_gateway_name:
        api_gateway_id = item["ApiId"]
        break

# Delete the API Gateway
if api_gateway_id:
    api_gateway.delete_api(ApiId=api_gateway_id)
    print(f"API Gateway '{api_gateway_name}' deleted successfully.")
else:
    print(f"API Gateway '{api_gateway_name}' not found.")
```

Deleting Lambda function:

!!! Danger
    Provide the `function_name` copied previously.

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide function name
function_name = "get_polarity_xxxxxxxx"

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Delete the Lambda function
lambda_client.delete_function(FunctionName=function_name)

print(f"Lambda function {function_name} deleted successfully")
```


Deleting the layer:

!!! Danger
    Provide the `layer_name` copied previously.

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Provide layer name
layer_name = "layer_polarity_xxxxx"

# Create a Boto3 client for AWS Lambda
lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

# Fetch the layer version ARN based on the layer name
response = lambda_client.list_layer_versions(
    CompatibleRuntime="python3.10",  # Provide the compatible runtime of the layer
    LayerName=layer_name,
)

if "LayerVersions" in response:
    layer_versions = response["LayerVersions"]

    # Delete each layer version
    for version in layer_versions:
        lambda_client.delete_layer_version(
            LayerName=layer_name, VersionNumber=version["Version"]
        )

    print(f"Deleted all versions of layer '{layer_name}'.")
else:
    print(f"No layer with the name '{layer_name}' found.")
```

## References
- Practical MLOps. Chapter 7.
- https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-dependencies
- https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html
- Image Lambda Layers diagram https://docs.aws.amazon.com/images/lambda/latest/dg/images/lambda-layers-diagram.png
- POE
