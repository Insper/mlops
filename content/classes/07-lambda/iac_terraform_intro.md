# Infrastructure as Code (IaC)

## Introduction

**Infrastructure as Code** (**IaC**) is a key practice in modern cloud computing and DevOps that allows you to manage and **provision computing infrastructure** through machine-readable definition files, rather than through physical hardware configuration or **interactive configuration tools**.

!!! info "What is IaC?"
    Infrastructure as Code treats infrastructure the same way developers treat application code:
    
    - **Version controlled**: Infrastructure definitions are stored in version control systems
    - **Reproducible**: The same infrastructure can be created multiple times with identical results
    - **Automated**: Infrastructure deployment and management can be automated
    - **Testable**: Infrastructure changes can be tested before being applied to production

## Why IaC for MLOps?

In MLOps, IaC becomes crucial for several reasons:

- **Consistency**: Ensure that development, staging, and production environments are more consistent
- **Scalability**: Easily replicate infrastructure for different models or experiments
- **Collaboration**: Teams can collaborate on infrastructure changes through code reviews
- **Disaster Recovery**: Quickly rebuild infrastructure from code definitions
- **Cost Control**: Track and manage cloud resources more effectively

## IaC Tools

Several tools can be used for IaC:

- **AWS CloudFormation**: Native AWS service for infrastructure provisioning
- **AWS CDK**: Code-based approach using familiar programming languages
- **AWS SAM**: Simplified approach specifically for serverless applications
- **Pulumi**: Modern IaC using real programming languages
- **Terraform**: Popular multi-cloud IaC tool
- **OpenTofu**: Community-driven fork of Terraform

!!! info "OpenTofu: Fun Fact!"
    A few years ago, HashiCorp decided to change Terraform's license to a more restrictive model, which raised concerns about the project's freedom and sustainability.
    
    In response, the community created an open fork to maintain collaboration and ensure transparency in development.

    Initially called OpenTF and later renamed to [**OpenTofu**](https://opentofu.org/), the project became maintained by the *Linux Foundation*, ensuring open governance and compatibility with Terraform.
    
    Thus, it became a free and reliable alternative for users and companies that depend on **IaC**.

For this class, we'll focus on **Terraform** as it's widely adopted across the industry and provides excellent multi-cloud support.

## Terraform Overview

[**Terraform**](https://developer.hashicorp.com/terraform) is an open-source infrastructure as code software tool created by HashiCorp. It enables users to define and provision infrastructure using a declarative configuration language.

Key benefits of Terraform:

- **Multi-cloud**: Works with AWS, Azure, GCP, and many other providers
- **Declarative**: Describe what you want, not how to get there
- **State Management**: Tracks infrastructure state and manages changes
- **Plan and Apply**: Preview changes before applying them
- **Modular**: Create reusable modules for common patterns

## Setting Up the Environment

### Install Terraform

Install the latest version of Terraform following the instructions for your operating system:

!!! note "Extra"
    If needed, access more information directly on the [Terraform](https://developer.hashicorp.com/terraform/install) website.

=== "Linux (Ubuntu/Debian)"
    <div class="termy">

    ```bash
    $ sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
    $ wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
    $ gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
    $ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    $ sudo apt update
    $ sudo apt-get install terraform

    ```

    </div>

=== "macOS"
    <div class="termy">

    ```bash
    $ brew tap hashicorp/tap
    $ brew install hashicorp/tap/terraform
    ```

    </div>

=== "Windows"
    1. Download the Terraform binary from [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)
    2. Extract the ZIP file to a directory (e.g., `C:\terraform`)
    3. Add the directory to the system PATH [Tutorial 1](https://www.wikihow.com/Change-the-PATH-Environment-Variable-on-Windows) [Tutorial 2](https://www.eukhost.com/kb/how-to-add-to-the-path-on-windows-10-and-windows-11/)

Verify the installation:

<p>
<div class="termy">

```console
$ terraform version
```

</div>
</p>

### Configure AWS Profile

Make sure you have AWS credentials configured. Set the AWS profile for the session:


=== "Linux/Mac"
    <p>
    <div class="termy">

    ```console
    $ export AWS_PROFILE=mlops
    ```

    </div>
    </p>

=== "Windows PowerShell"
    <p>
    <div class="termy">

    ```console
    $ $env:AWS_PROFILE="mlops"
    ```

    </div>
    </p>

=== "Windows CMD"
    <p>
    <div class="termy">

    ```console
    $ set AWS_PROFILE=mlops
    ```

    </div>
    </p>

Verify your AWS configuration:

<p>
<div class="termy">

```console
$ aws sts get-caller-identity --profile mlops
```

</div>
</p>

!!! exercise "Question"
    Before we start, make sure you have:

    1. **AWS CLI** configured with appropriate credentials
    1. **Docker** installed and running
    1. **Terraform** installed

## Getting Started with Terraform: S3 Bucket Experiment

Before diving into a more complex project, let's start with a simple Terraform experiment to understand the basics.

### Create S3 Bucket Experiment

Let's create a simple S3 bucket using Terraform to understand the workflow.

<p>
<div class="termy">

```console
$ mkdir terraform-s3-experiment
$ cd terraform-s3-experiment
```

</div>
</p>

### Basic Terraform Configuration for S3

In Terraform, the `main.tf` file is where we define our infrastructure resources.

!!! exercise "Question"
    Create a file `main.tf` with the following content:

    ```hcl
    # Configure the AWS Provider
    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"
        }
      }
    }

    provider "aws" {
      region  = var.aws_region
      profile = var.aws_profile
    }

    # Random ID for unique bucket naming
    resource "random_id" "bucket_suffix" {
      byte_length = 8
    }

    # S3 Bucket
    resource "aws_s3_bucket" "experiment_bucket" {
      bucket = "${var.bucket_prefix}-${var.student_id}-${random_id.bucket_suffix.hex}"

      tags = {
        Name        = "Terraform Experiment Bucket"
        Environment = "learning"
        StudentId   = var.student_id
        CreatedBy   = "Terraform"
      }
    }

    # S3 Bucket versioning
    resource "aws_s3_bucket_versioning" "experiment_bucket" {
      bucket = aws_s3_bucket.experiment_bucket.id
      versioning_configuration {
        status = "Enabled"
      }
    }

    # S3 Bucket encryption
    resource "aws_s3_bucket_server_side_encryption_configuration" "experiment_bucket" {
      bucket = aws_s3_bucket.experiment_bucket.id

      rule {
        apply_server_side_encryption_by_default {
          sse_algorithm = "AES256"
        }
      }
    }

    # S3 Bucket public access block
    resource "aws_s3_bucket_public_access_block" "experiment_bucket" {
      bucket = aws_s3_bucket.experiment_bucket.id

      block_public_acls       = true
      block_public_policy     = true
      ignore_public_acls      = true
      restrict_public_buckets = true
    }
    ```

### Variables Configuration for S3 Experiment

The `variables.tf` file is where we define the input variables for our Terraform configuration.

!!! exercise "Question"
    Create a file `variables.tf`:

    !!! info "Info!"
        You don't need to modify the `variables.tf` file for this experiment!

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

    variable "bucket_prefix" {
      description = "Prefix for the S3 bucket name"
      type        = string
      default     = "terraform-experiment"
    }
    ```

### Variable Values for S3 Experiment

We can define the variable values in a separate file called `terraform.tfvars`.

!!! exercise "Question"
    Create a file `terraform.tfvars`:

    !!! warning "Important"
        Replace `student_id` with your unique identifier (e.g., your username)

    ```hcl
    # AWS Configuration
    aws_region  = "us-east-2"
    aws_profile = "mlops"

    # Student Configuration (REQUIRED - Make this unique!)
    student_id = "your-username-here"

    # Bucket Configuration
    bucket_prefix = "terraform-experiment"
    ```
    

### Outputs Configuration for S3 Experiment

The `outputs.tf` file is where we define the output values for our Terraform configuration.

The output values are used to extract information from the resources created by Terraform.

!!! exercise "Question"
    Create a file `outputs.tf`:

    !!! info "Info!"
        You don't need to modify the `outputs.tf` file for this experiment!

    ```hcl
    output "bucket_name" {
      description = "Name of the created S3 bucket"
      value       = aws_s3_bucket.experiment_bucket.bucket
    }

    output "bucket_arn" {
      description = "ARN of the created S3 bucket"
      value       = aws_s3_bucket.experiment_bucket.arn
    }

    output "bucket_region" {
      description = "Region of the created S3 bucket"
      value       = aws_s3_bucket.experiment_bucket.region
    }

    output "student_id" {
      description = "Student identifier for this deployment"
      value       = var.student_id
    }
    ```

### Deploy the S3 Bucket

!!! exercise "Question"
    Now let's deploy our first Terraform infrastructure:
    
    <p>
    **Step 1: Initialize Terraform**
    The `terraform init` command is used to initialize a Terraform working directory.


    <div class="termy">

    ```console
    $ terraform init
    ```

    </div>
    </p>

    <p>
    **Step 2: Validate the configuration**
    The `terraform validate` command is used to validate the Terraform configuration files in a directory.

    <div class="termy">

    ```console
    $ terraform validate
    ```

    </div>
    </p>

    <p>
    **Step 3: Format the configuration**
    The `terraform fmt` command is used to format Terraform configuration files to a canonical format and style.

    <div class="termy">

    ```console
    $ terraform fmt
    ```

    </div>
    </p>

    <p>
    **Step 4: Plan the deployment**
    The `terraform plan` command is used to create an **execution plan**, showing what actions Terraform will take to change the infrastructure.

    !!! info "Info!"
        It won't make any changes to your infrastructure, just show you what will happen.

    <div class="termy">

    ```console
    $ terraform plan
    ```

    </div>
    </p>

    <p>
    **Step 5: Apply the configuration**

    When we run the `terraform apply` command, Terraform will create the resources defined in the configuration files.

    This means that the S3 bucket will be created in your AWS account.

    !!! warning "Warning!"
        Type `yes` when prompted to confirm the deployment.

    <div class="termy">

    ```console
    $ terraform apply
    ```

    </div>
    </p>

    

### Verify S3 Bucket Creation

!!! exercise "Question"
    After the deployment completes, verify your bucket was created using AWS CLI:

    <p>
    **Step 1: View Terraform outputs**

    Let's check the outputs from our Terraform deployment.

    <div class="termy">

    ```console
    $ terraform output
    ```

    </div>
    </p>

    <p>
    **Step 2: List all S3 buckets and filter for yours**

    To show your S3 buckets, use the following command:

    !!! info "Info!"
        Not all buckets were created by Terraform.

        Some may exist from previous classes!

    <div class="termy">

    ```console
    $ aws s3 ls --profile mlops
    ```

    </div>
    </p>

    <p>
    **Step 3: Filter buckets by your student ID**

    To filter the S3 buckets by your student ID, use the following command:

    <div class="termy">

    ```console
    $ aws s3api list-buckets --query "Buckets[?contains(Name, '$(terraform output -raw student_id)')].{Name:Name,CreationDate:CreationDate}" --output table --profile mlops
    ```

    </div>
    </p>

    <p>
    **Step 4: Get detailed information about your bucket**
    <div class="termy">

    ```console
    $ BUCKET_NAME=$(terraform output -raw bucket_name)
    $ aws s3api head-bucket --bucket $BUCKET_NAME --profile mlops
    $ aws s3api get-bucket-location --bucket $BUCKET_NAME --profile mlops
    $ aws s3api get-bucket-versioning --bucket $BUCKET_NAME --profile mlops
    $ aws s3api get-bucket-encryption --bucket $BUCKET_NAME --profile mlops
    ```

    </div>
    </p>

### Test S3 Bucket Functionality

Let's test our bucket by uploading and downloading a file:

!!! exercise "Question"
    Create a simple text file to upload to our **S3 bucket**.

    <div class="termy">

    ```console
    $ echo "Hello from Terraform experiment!" > test-file.txt
    $ echo "Student ID: $(terraform output -raw student_id)" >> test-file.txt
    $ echo "Bucket Name: $(terraform output -raw bucket_name)" >> test-file.txt
    $ echo "Created on: $(date)" >> test-file.txt
    $ cat test-file.txt
    ```

    </div>


!!! exercise "Question"
    Upload the file to **S3**

    <div class="termy">

    ```console
    $ BUCKET_NAME=$(terraform output -raw bucket_name)
    $ aws s3 cp test-file.txt s3://$BUCKET_NAME/test-file.txt --profile mlops
    ```

    </div>

!!! exercise "Question"
    List bucket contents

    <div class="termy">

    ```console
    $ aws s3 ls s3://$BUCKET_NAME/ --profile mlops
    ```

    </div>

!!! exercise "Question"
    Download the file with a new name

    <div class="termy">

    ```console
    $ aws s3 cp s3://$BUCKET_NAME/test-file.txt downloaded-file.txt --profile mlops
    $ cat downloaded-file.txt
    ```

    </div>


### Understanding Terraform State

Now, we are going to explore Terraform state management.

!!! exercise "Question"
    View the state file:

    <div class="termy">

    ```console
    $ terraform show
    ```

    </div>

!!! exercise "Question"
    List resources in state:

    <div class="termy">

    ```console
    $ terraform state list
    ```

    </div>

!!! exercise "Question"
    View specific resource details:

    <div class="termy">

    ```console
    $ terraform state show aws_s3_bucket.experiment_bucket
    ```

    </div>


### Make Changes and Update

Let's modify our infrastructure to understand how Terraform handles changes.

!!! exercise "Question"
    Add a lifecycle rule to the bucket
    
    Update your `main.tf` file by adding this resource after the existing S3 bucket resources:

    ```hcl
    # S3 Bucket lifecycle configuration
    resource "aws_s3_bucket_lifecycle_configuration" "experiment_bucket" {
      bucket = aws_s3_bucket.experiment_bucket.id

      rule {
        id     = "delete_old_versions"
        status = "Enabled"

        filter {
          prefix = ""
        }

        noncurrent_version_expiration {
          noncurrent_days = 30
        }
      }

      rule {
        id     = "delete_incomplete_multipart_uploads"
        status = "Enabled"

        filter {
          prefix = ""
        }

        abort_incomplete_multipart_upload {
          days_after_initiation = 7
        }
      }
    }
    ```

!!! exercise text short "Question"
    Plan the changes. Which resources are being created or modified?

    <div class="termy">

    ```console
    $ terraform plan
    ```

    </div>


!!! exercise "Question"
    Apply the changes.

    <div class="termy">

    ```console
    $ terraform apply
    ```

    </div>


!!! exercise "Question"
    Verify the lifecycle configuration.

    <div class="termy">

    ```console
    $ BUCKET_NAME=$(terraform output -raw bucket_name)
    $ aws s3api get-bucket-lifecycle-configuration --bucket $BUCKET_NAME --profile mlops
    ```

    </div>


### Clean Up S3 Experiment

When you're ready to move to the next experiment, clean up these resources!

!!! exercise "Question"
    Remove test files from bucket.

    <div class="termy">

    ```console
    $ BUCKET_NAME=$(terraform output -raw bucket_name)
    $ aws s3 rm s3://$BUCKET_NAME/test-file.txt --profile mlops
    ```

    </div>

!!! exercise "Question"
    Remove all objects and versions from bucket (required for versioned buckets).

    <div class="termy">
    ```console
    $ BUCKET_NAME=$(terraform output -raw bucket_name)
    $ aws s3api delete-objects --bucket $BUCKET_NAME --delete "$(aws s3api list-object-versions --bucket $BUCKET_NAME --query='{Objects: Versions[].{Key:Key,VersionId:VersionId}}' --profile mlops)" --profile mlops
    $ aws s3api delete-objects --bucket $BUCKET_NAME --delete "$(aws s3api list-object-versions --bucket $BUCKET_NAME --query='{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' --profile mlops)" --profile mlops
    ```
    </div>
    
    !!! warning "Alternative: Manual Bucket Cleanup"
        If `terraform output` is not available or if you need to clean up manually, you can use these commands instead:

        !!! warning "Attention"
            Replace `BUCKET_NAME` with your actual bucket name

        <div class="termy">
        ```console
        $ aws s3 ls --profile mlops | grep terraform-experiment
        $ BUCKET_NAME="terraform-experiment-your-student-id-xxxxxxxx"
        $ aws s3api delete-objects --bucket $BUCKET_NAME --delete "$(aws s3api list-object-versions --bucket $BUCKET_NAME --query='{Objects: Versions[].{Key:Key,VersionId:VersionId}}' --profile mlops)" --profile mlops
        $ aws s3api delete-objects --bucket $BUCKET_NAME --delete "$(aws s3api list-object-versions --bucket $BUCKET_NAME --query='{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' --profile mlops)" --profile mlops
        $ aws s3 rb s3://$BUCKET_NAME --force --profile mlops
        ```
        </div>

!!! exercise "Question"
    Destroy the infrastructure.

    !!! warning "Bucket Not Empty Error"
        If you get a *"BucketNotEmpty"* error during `terraform destroy`, it means there are still objects or versions in the bucket.
        
        Use the commands above to remove all objects and versions before running `terraform destroy` again.

    !!! info "Info!"
        Type `yes` when prompted to confirm the destruction.

    <div class="termy">

    ```console
    $ terraform destroy
    ```

    </div>


!!! exercise "Question"
    Verify bucket deletion.

    <div class="termy">

    ```console
    $ aws s3api list-buckets --query "Buckets[?contains(Name, '$(terraform output -raw student_id)')]" --profile mlops
    ```

    </div>


Now, you can go to the next activity!
