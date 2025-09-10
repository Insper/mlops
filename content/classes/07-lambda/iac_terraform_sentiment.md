# Terraform Project: Sentiment Analysis

Now that you understand the basics of Terraform, let's create a more complex project for our sentiment analysis Lambda function used in the previous class.

## Initialize Terraform Project

<p>
<div class="termy">

```console
$ mkdir sentiment-analysis-iac-terraform
$ cd sentiment-analysis-iac-terraform
```

</div>
</p>

This creates a new directory for our Terraform project with the following structure we'll build:

!!! warning
    You don't have this structure yet. We will create it in the following steps.

```
sentiment-analysis-iac-terraform/
├── main.tf               # Main Terraform configuration
├── variables.tf          # Input variables
├── outputs.tf            # Output values
├── terraform.tfvars      # Variable values
├── versions.tf           # Provider requirements
├── lambda/               # Lambda function code
│   ├── app.py            # Lambda function
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Docker configuration
└── modules/              # Reusable modules (optional)
```

## Creating the Lambda Function Code

Let's create our sentiment analysis function that will be deployed using Docker.

### Create Lambda Directory

!!! exercise "Question"
    First, create the `lambda` directory:

    <div class="termy">

    ```console
    $ mkdir lambda
    $ cd lambda
    ```

    </div>

### Lambda Function Code

!!! exercise "Question"
    Create a file `lambda/app.py` with the following sentiment analysis function:

    ```python
    import json
    import logging
    from textblob import TextBlob

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def lambda_handler(event, context):
        """
        AWS Lambda handler for sentiment analysis using TextBlob
        """
        try:
            # Log the incoming event
            logger.info(f"Received event: {json.dumps(event)}")
            
            # Extract text from the event
            if 'body' in event:
                # API Gateway format
                body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
                text = body.get('text', '')
            else:
                # Direct invocation format
                text = event.get('text', '')
            
            if not text:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'No text provided'
                    })
                }
            
            # Perform sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment category
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            result = {
                'text': text,
                'sentiment': sentiment,
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3)
            }
            
            logger.info(f"Analysis result: {result}")
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Internal server error'
                })
            }
    ```

### Requirements File for Lambda

!!! exercise "Question"
    Create a file `lambda/requirements.txt` with the dependencies:

    ```
    textblob==0.19.0
    ```

### Dockerfile for Lambda

!!! exercise "Question"
    Create a file `lambda/Dockerfile`:

    ```dockerfile
    # Use the official AWS Lambda Python runtime
    FROM public.ecr.aws/lambda/python:3.9

    # Copy requirements and install dependencies
    COPY requirements.txt ${LAMBDA_TASK_ROOT}
    RUN pip install -r requirements.txt

    # Download NLTK data required by TextBlob
    RUN python -c "import nltk; nltk.download('punkt', download_dir='/opt/python')"
    RUN python -c "import nltk; nltk.download('brown', download_dir='/opt/python')"

    # Set NLTK data path
    ENV NLTK_DATA=/opt/python

    # Copy function code
    COPY app.py ${LAMBDA_TASK_ROOT}

    # Set the CMD to your handler
    CMD [ "app.lambda_handler" ]
    ```

## Defining Infrastructure with Terraform

Now let's define our infrastructure using Terraform configuration files.

### Get Lambda Execution Role

!!! exercise "Question"
    Before creating the infrastructure, you need to get the ARN of an existing Lambda execution role from the professor.
    
    Ask the professor for:

    - **Lambda Execution Role ARN** (e.g., `arn:aws:iam::123456789012:role/lambda-execution-role`)
    
    You will need this ARN for the Terraform configuration.

!!! tip "Finding Role ARN"
    If you need to find existing roles, you can list them with:
    
    <div class="termy">

    ```console
    $ aws iam list-roles --query "Roles[?contains(RoleName, 'lambda')].{RoleName:RoleName, Arn:Arn}" --output table --profile mlops
    ```

    </div>


### Create Provider Configuration

!!! exercise "Question"
    Navigate back to the project root and create `versions.tf`:

    ```hcl
    terraform {
      required_version = ">= 1.0"
      
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"
        }
        docker = {
          source  = "kreuzwerker/docker"
          version = "~> 3.0"
        }
      }
    }

    # Configure the AWS Provider
    provider "aws" {
      region  = var.aws_region
      profile = var.aws_profile
      
      default_tags {
        tags = {
          Project     = "SentimentAnalysis"
          Environment = var.environment
          StudentId   = var.student_id
          ManagedBy   = "Terraform"
        }
      }
    }

    # Configure Docker provider
    provider "docker" {
      registry_auth {
        address  = data.aws_ecr_authorization_token.token.proxy_endpoint
        username = data.aws_ecr_authorization_token.token.user_name
        password = data.aws_ecr_authorization_token.token.password
      }
    }
    ```

### Create Variables Configuration

!!! exercise "Question"
    Create `variables.tf`:

    ```hcl
    variable "aws_region" {
      description = "AWS region for resources"
      type        = string
      default     = "us-east-2"
    }

    variable "aws_profile" {
      description = "AWS profile to use"
      type        = string
      default     = "mlops"
    }

    variable "student_id" {
      description = "Unique student identifier"
      type        = string
      validation {
        condition     = can(regex("^[a-z0-9-]+$", var.student_id))
        error_message = "Student ID must contain only lowercase letters, numbers, and hyphens."
      }
    }

    variable "environment" {
      description = "Environment name"
      type        = string
      default     = "dev"
    }

    variable "lambda_execution_role_arn" {
      description = "ARN of existing Lambda execution role"
      type        = string
      validation {
        condition     = can(regex("^arn:aws:iam::", var.lambda_execution_role_arn))
        error_message = "Lambda execution role ARN must be a valid IAM role ARN."
      }
    }

    variable "lambda_timeout" {
      description = "Lambda function timeout in seconds"
      type        = number
      default     = 30
    }

    variable "lambda_memory_size" {
      description = "Lambda function memory size in MB"
      type        = number
      default     = 512
    }
    ```

### Create Variable Values File

!!! exercise "Question"
    Create `terraform.tfvars` with your specific configuration:

    !!! warning "Important!"
        - Replace `student_id` with your **insper username**
        - Replace `lambda_execution_role_arn` with the role ARN provided by the professor

    !!! danger "Security Notice!"
        Never commit `terraform.tfvars` files to version control as they contain sensitive configuration values.

    ```hcl
    # AWS Configuration
    aws_region  = "us-east-2"
    aws_profile = "mlops"

    # Student Configuration (REQUIRED - Make this unique!)
    student_id = "macielx"

    # Environment
    environment = "dev"

    # Lambda Execution Role (Ask the professor)
    lambda_execution_role_arn = "arn:aws:iam::123456789012:role/lambda-execution-role"

    # Lambda Configuration
    lambda_timeout     = 30
    lambda_memory_size = 512
    ```

### Create Main Terraform Configuration

!!! exercise "Question"
    Create `main.tf`:

    ```hcl
    # Data sources
    data "aws_caller_identity" "current" {}

    data "aws_ecr_authorization_token" "token" {}

    # Data source for lambda source hash
    data "archive_file" "lambda_source" {
      type        = "zip"
      source_dir  = "./lambda"
      output_path = "/tmp/lambda-${var.student_id}.zip"
    }

    # Create ECR repository for Lambda container image
    resource "aws_ecr_repository" "sentiment_analysis" {
      name                 = "sentiment-analysis-iac-${var.student_id}"
      image_tag_mutability = "MUTABLE"

      image_scanning_configuration {
        scan_on_push = true
      }

      lifecycle {
        prevent_destroy = false
      }
    }

    # ECR repository policy
    resource "aws_ecr_repository_policy" "sentiment_analysis_policy" {
      repository = aws_ecr_repository.sentiment_analysis.name

      policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "LambdaECRImageRetrievalPolicy"
            Effect = "Allow"
            Principal = {
              Service = "lambda.amazonaws.com"
            }
            Action = [
              "ecr:BatchGetImage",
              "ecr:GetDownloadUrlForLayer"
            ]
          }
        ]
      })
    }

    # Build and push Docker image
    resource "docker_image" "sentiment_analysis" {
      name = "${aws_ecr_repository.sentiment_analysis.repository_url}:${substr(data.archive_file.lambda_source.output_sha, 0, 8)}"
      
      build {
        context    = "./lambda"
        dockerfile = "Dockerfile"
        platform   = "linux/amd64"
      }

      depends_on = [aws_ecr_repository.sentiment_analysis]
    }

    resource "docker_registry_image" "sentiment_analysis" {
      name = docker_image.sentiment_analysis.name

      depends_on = [docker_image.sentiment_analysis]
    }

    # Import existing IAM role
    data "aws_iam_role" "lambda_execution_role" {
      name = split("/", var.lambda_execution_role_arn)[1]
    }

    # Lambda function
    resource "aws_lambda_function" "sentiment_analysis" {
      function_name = "sentiment-analysis-iac-${var.student_id}"
      role          = var.lambda_execution_role_arn

      package_type = "Image"
      image_uri    = docker_image.sentiment_analysis.name

      timeout     = var.lambda_timeout
      memory_size = var.lambda_memory_size

      environment {
        variables = {
          LOG_LEVEL  = "INFO"
          STUDENT_ID = var.student_id
        }
      }

      depends_on = [
        docker_registry_image.sentiment_analysis,
        aws_ecr_repository.sentiment_analysis
      ]

      description = "Sentiment analysis using TextBlob for ${var.student_id}"
    }

    # CloudWatch Log Group
    resource "aws_cloudwatch_log_group" "sentiment_analysis" {
      name              = "/aws/lambda/${aws_lambda_function.sentiment_analysis.function_name}"
      retention_in_days = 7

      depends_on = [aws_lambda_function.sentiment_analysis]
    }

    # API Gateway
    resource "aws_api_gateway_rest_api" "sentiment_analysis" {
      name        = "sentiment-analysis-api-iac-${var.student_id}"
      description = "API for sentiment analysis - ${var.student_id}"

      endpoint_configuration {
        types = ["REGIONAL"]
      }
    }

    # API Gateway CORS configuration
    resource "aws_api_gateway_method" "options" {
      rest_api_id   = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id   = aws_api_gateway_rest_api.sentiment_analysis.root_resource_id
      http_method   = "OPTIONS"
      authorization = "NONE"
    }

    resource "aws_api_gateway_method_response" "options" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_rest_api.sentiment_analysis.root_resource_id
      http_method = aws_api_gateway_method.options.http_method
      status_code = "200"

      response_parameters = {
        "method.response.header.Access-Control-Allow-Headers" = true
        "method.response.header.Access-Control-Allow-Methods" = true
        "method.response.header.Access-Control-Allow-Origin"  = true
      }
    }

    resource "aws_api_gateway_integration" "options" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_rest_api.sentiment_analysis.root_resource_id
      http_method = aws_api_gateway_method.options.http_method
      type        = "MOCK"

      request_templates = {
        "application/json" = jsonencode({
          statusCode = 200
        })
      }
    }

    resource "aws_api_gateway_integration_response" "options" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_rest_api.sentiment_analysis.root_resource_id
      http_method = aws_api_gateway_method.options.http_method
      status_code = aws_api_gateway_method_response.options.status_code

      response_parameters = {
        "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
        "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'"
        "method.response.header.Access-Control-Allow-Origin"  = "'*'"
      }
    }

    # API Gateway resources and methods for /analyze endpoint
    resource "aws_api_gateway_resource" "analyze" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      parent_id   = aws_api_gateway_rest_api.sentiment_analysis.root_resource_id
      path_part   = "analyze"
    }

    resource "aws_api_gateway_method" "analyze_post" {
      rest_api_id   = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id   = aws_api_gateway_resource.analyze.id
      http_method   = "POST"
      authorization = "NONE"
    }

    resource "aws_api_gateway_integration" "analyze_lambda" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_resource.analyze.id
      http_method = aws_api_gateway_method.analyze_post.http_method

      integration_http_method = "POST"
      type                    = "AWS_PROXY"
      uri                     = aws_lambda_function.sentiment_analysis.invoke_arn
    }

    # API Gateway resources and methods for /health endpoint
    resource "aws_api_gateway_resource" "health" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      parent_id   = aws_api_gateway_rest_api.sentiment_analysis.root_resource_id
      path_part   = "health"
    }

    resource "aws_api_gateway_method" "health_get" {
      rest_api_id   = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id   = aws_api_gateway_resource.health.id
      http_method   = "GET"
      authorization = "NONE"
    }

    resource "aws_api_gateway_integration" "health_mock" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_resource.health.id
      http_method = aws_api_gateway_method.health_get.http_method
      type        = "MOCK"

      request_templates = {
        "application/json" = jsonencode({
          statusCode = 200
        })
      }
    }

    resource "aws_api_gateway_method_response" "health_get" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_resource.health.id
      http_method = aws_api_gateway_method.health_get.http_method
      status_code = "200"

      response_parameters = {
        "method.response.header.Access-Control-Allow-Origin" = true
      }
    }

    resource "aws_api_gateway_integration_response" "health_mock" {
      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id
      resource_id = aws_api_gateway_resource.health.id
      http_method = aws_api_gateway_method.health_get.http_method
      status_code = aws_api_gateway_method_response.health_get.status_code

      response_templates = {
        "application/json" = jsonencode({
          status     = "healthy"
          service    = "sentiment-analysis"
          student_id = var.student_id
        })
      }

      response_parameters = {
        "method.response.header.Access-Control-Allow-Origin" = "'*'"
      }
    }

    # Lambda permissions for API Gateway
    resource "aws_lambda_permission" "api_gateway" {
      statement_id  = "AllowAPIGatewayInvoke"
      action        = "lambda:InvokeFunction"
      function_name = aws_lambda_function.sentiment_analysis.function_name
      principal     = "apigateway.amazonaws.com"
      source_arn    = "${aws_api_gateway_rest_api.sentiment_analysis.execution_arn}/*/*"
    }

    # API Gateway deployment
    resource "aws_api_gateway_deployment" "sentiment_analysis" {
      depends_on = [
        aws_api_gateway_method.analyze_post,
        aws_api_gateway_integration.analyze_lambda,
        aws_api_gateway_method.health_get,
        aws_api_gateway_integration.health_mock,
        aws_api_gateway_method.options,
        aws_api_gateway_integration.options,
      ]

      rest_api_id = aws_api_gateway_rest_api.sentiment_analysis.id

      triggers = {
        redeployment = sha1(jsonencode([
          aws_api_gateway_resource.analyze.id,
          aws_api_gateway_method.analyze_post.id,
          aws_api_gateway_integration.analyze_lambda.id,
          aws_api_gateway_resource.health.id,
          aws_api_gateway_method.health_get.id,
          aws_api_gateway_integration.health_mock.id,
        ]))
      }

      lifecycle {
        create_before_destroy = true
      }
    }

    resource "aws_api_gateway_stage" "sentiment_analysis" {
      deployment_id = aws_api_gateway_deployment.sentiment_analysis.id
      rest_api_id   = aws_api_gateway_rest_api.sentiment_analysis.id
      stage_name    = var.environment
    }
    ```

### Create Outputs Configuration

!!! exercise "Question"
    Create `outputs.tf`:

    ```hcl
    output "api_url" {
      description = "Sentiment Analysis API URL"
      value       = "${aws_api_gateway_stage.sentiment_analysis.invoke_url}"
    }

    output "lambda_function_name" {
      description = "Lambda function name"
      value       = aws_lambda_function.sentiment_analysis.function_name
    }

    output "student_id" {
      description = "Student identifier for this deployment"
      value       = var.student_id
    }

    output "ecr_repository_url" {
      description = "ECR repository URL"
      value       = aws_ecr_repository.sentiment_analysis.repository_url
    }

    output "api_gateway_id" {
      description = "API Gateway REST API ID"
      value       = aws_api_gateway_rest_api.sentiment_analysis.id
    }

    output "health_check_url" {
      description = "Health check endpoint URL"
      value       = "${aws_api_gateway_stage.sentiment_analysis.invoke_url}/health"
    }

    output "analyze_endpoint_url" {
      description = "Sentiment analysis endpoint URL"
      value       = "${aws_api_gateway_stage.sentiment_analysis.invoke_url}/analyze"
    }
    ```

### Secure Your Configuration

!!! exercise "Question"
    Create `.gitignore` file to avoid committing sensitive information:

    ```gitignore
    # Terraform
    *.tfstate
    *.tfstate.*
    .terraform/
    .terraform.lock.hcl
    terraform.tfvars
    
    # Environment variables
    .env
    
    # Python
    __pycache__/
    *.pyc
    .venv/
    
    # IDE
    .vscode/
    .idea/
    
    # Docker
    .docker/
    
    # AWS
    .aws/
    
    # Logs
    *.log
    ```

## Deploying with Terraform

### Initialize Terraform

<p>
<div class="termy">

```console
$ terraform init
```

</div>
</p>

### Validate Configuration

<p>
<div class="termy">

```console
$ terraform validate
```

</div>
</p>

### Format Configuration

<p>
<div class="termy">

```console
$ terraform fmt
```

</div>
</p>

### Plan the Deployment

<p>
<div class="termy">

```console
$ terraform plan
```

</div>
</p>

!!! warning
    If you see any errors related to Docker, ensure that Docker is running, with proper authorizations:

    <p>
    <div class="termy">

    ```console
    $ id -nG
    $ sudo usermod -aG docker $USER
    $ newgrp docker
    $ id -nG
    ```

    </div>
    </p>

    Also, ensure that you are authenticated with **ECR**.

    !!! danger "ECR Authentication"
        Replace `YOUR_ECR_URL` with your actual **ECR URL**.

    <p>
    <div class="termy">

    ```console
    $ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin YOUR_ECR_URL
    ```

    </div>
    </p>

This shows you what Terraform will create, modify, or destroy.

### Apply the Configuration

<p>
<div class="termy">

```console
$ terraform apply
```

</div>
</p>

!!! warning "Important!"
    The deployment process will:
    
    1. Create an ECR repository
    2. Build the Docker image locally
    3. Push it to Amazon ECR
    4. Create the Lambda function
    5. Set up the API Gateway
    6. Configure all necessary permissions

!!! info "Info!"
    Type `yes` when prompted to confirm the deployment.

### Troubleshooting Deployment Issues

!!! warning "Common Error: Docker Build Failures"
    If Docker image building fails:
    
    **Step 1: Check Docker is running**
    <p>
    <div class="termy">

    ```console
    $ docker info
    ```

    </div>
    </p>

    **Step 2: Authenticate with ECR manually**
    <p>
    <div class="termy">

    ```console
    $ aws ecr get-login-password --region us-east-2 --profile mlops | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text --profile mlops).dkr.ecr.us-east-2.amazonaws.com
    ```

    </div>
    </p>

### If Deployment Fails

!!! exercise "Question"
    If your deployment fails:

    <p>
    **Step 1: Check the specific error**
    <div class="termy">

    ```console
    $ terraform apply
    ```

    </div>
    </p>


    <p>
    **Step 2: Destroy and retry if needed**
    <div class="termy">

    ```console
    $ terraform destroy
    $ terraform apply
    ```

    </div>
    </p>

    <p>
    **Step 3: Check for existing resources**
    <div class="termy">

    ```console
    $ aws lambda list-functions --query "Functions[?contains(FunctionName, '${STUDENT_ID}')]" --profile mlops
    $ aws ecr describe-repositories --query "repositories[?contains(repositoryName, '${STUDENT_ID}')]" --profile mlops
    ```

    </div>
    </p>

## Testing the Deployment

!!! exercise "Question"
    View Terraform Outputs

    <div class="termy">

    ```console
    $ terraform output
    ```

    </div>

!!! exercise "Question"
    Perform Health Check

    <div class="termy">

    ```console
    $ curl $(terraform output -raw health_check_url)
    ```

    </div>

!!! exercise "Question"
    Test your sentiment analysis API:

    === "Using bash"
        Create a `test_api.sh` script:

        ??? "`test_api.sh`"

            ```bash
            #!/bin/bash
            
            # Get the API URL from Terraform output
            API_URL=$(terraform output -raw analyze_endpoint_url)
            
            # Test texts
            declare -a texts=(
                "I love this MLOps class!"
                "This assignment is terrible."
                "The weather is okay today."
                "AWS Lambda with Docker is amazing!"
            )
            
            # Test each text
            for text in "${texts[@]}"; do
                echo "Testing: $text"
                curl -X POST "$API_URL" \
                    -H "Content-Type: application/json" \
                    -d "{\"text\": \"$text\"}" \
                    | jq '.'
                echo "---"
            done
            ```
        
        Then, run it with:

        <p>
        <div class="termy">

        ```console
        $ chmod +x test_api.sh
        $ ./test_api.sh
        ```

        </div>
        </p>

    === "Using Python"

        !!! warning "Important"
            Provide `API_URL` with your actual API Gateway URL from Terraform outputs.

        ???  "`test_api.py`"

            ```python
            import requests
            import json

            # Replace with your actual API Gateway URL from Terraform outputs
            # You can get this by running: terraform output analyze_endpoint_url
            API_URL = "https://xxx.execute-api.xxx.amazonaws.com/dev/analyze"

            def get_polarity(text):
                """
                Get the polarity of the given text using the sentiment analysis API.
                
                Args:
                    text (str): The text to analyze
                    
                Returns:
                    float or str or None: The polarity/sentiment value, or None if failed
                """
                payload = {"text": text}
                
                try:
                    response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        return result
                    else:
                        print(f"API Error: HTTP {response.status_code} - {response.text}")
                        return None
                        
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
                    return None

            # Test the health endpoint
            HEALTH_URL = API_URL.replace("/analyze", "/health")
            try:
                health_response = requests.get(HEALTH_URL)
                if health_response.status_code == 200:
                    print("\nHealth Check:")
                    print(json.dumps(health_response.json(), indent=2))
                else:
                    print(f"Health check failed: HTTP {health_response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Health check request failed: {e}")


            print("\nType your messages to analyze polarity. Type 'exit' to quit.")

            while True:
                user_input = input("\nEnter text to analyze: ").strip()
                
                if user_input.lower() == 'exit':
                    break
                
                if not user_input:
                    print("Please enter some text.")
                    continue
                
                polarity = get_polarity(user_input)
                if polarity is not None:
                    print(f"Polarity: {polarity}")
                else:
                    print("Failed to analyze the text. Please try again.")
            ```

!!! exercise text long "Question"
    Change the `lambda/app.py`. You can add one more key to the response **JSON** (e.g., "library": "textblob").

    Then, perform `terraform plan`. Which resources will be affected?

    !!! warning
        Do not perform `terraform apply` yet!

!!! exercise text long "Question"
    Change the `terraform.tfvars`:
    
    ```
    lambda_timeout     = 10
    lambda_memory_size = 128
    
    Then, perform `terraform plan`. Which resources will be affected?

    !!! warning
        Do not perform `terraform apply` yet!

!!! exercise "Question"
    Run `terraform apply` to apply all changes.

!!! exercise "Question"
    Test the API endpoint using the provided test scripts.

    Ensure that the API is working and the changes are reflected in the API responses.

That's all for today! Let's just clean up the workspace.

!!! exercise "Question"
    Run `terraform destroy` to clean up all resources.

    !!! warning
        This action will permanently delete all resources created by Terraform.

        Type `yes` to confirm.
