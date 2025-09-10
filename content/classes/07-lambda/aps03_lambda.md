# APS 03

In this assignment, we are going to create a new version of the work from the [API class](../02-api/api_deploy.md#an-api-that-makes-predictions).

## Accept assignment

All assignments delivery will be made using Git repositories. Access the link below to accept the invitation and start working on the third assignment.

[**Invitation link**](https://classroom.github.com/a/qeGDHA0J){ .ah-button }

## Clone repository

Clone your private repository:

!!! exercise "Question"
    Create a `.gitignore` and make sure the `.env` is in it!

Now, it's time to start working!

Our goal is to transform the `predict` route from class 02 into a lambda function. In other words, assume the model is already trained and that the model pickle can be embedded in the **Docker image**.

!!! info "Important!"
    Notice that we will no longer be using FastAPI.
    
    We will create a **lambda function** that has a handler for **predict**, then we will create an API Gateway that exposes the lambda function.

## Part I

This part is about creating a Lambda function for the sentiment analysis model **manually**. It's a more hands-on approach compared to using the **Terraform** setup.

!!! warning
    The **Part I** is **totally optional**.

    If You prefer to use the Terraform setup right away, feel free to skip this part.

!!! exercise "Question"
    Create a proper project structure (folders and files).

!!! exercise "Question"
    Create the `.py` file with the function handler.

!!! exercise "Question"
    Create the `requirements.txt` file with the dependencies.

!!! exercise "Question"
    Create the `Dockerfile`

    !!! tip "Tip!"
        In order to install `lightgbm`, you will need to install some dependencies on the system. So, before `RUN pip install -r requirements.txt` you can add:

        ```docker
        # Install system dependencies
        RUN yum install -y libstdc++ cmake gcc-c++ && \
            yum clean all && \
            rm -rf /var/cache/yum

        # Install the specified packages
        RUN pip install -r requirements.txt
        ```

!!! exercise "Question"
    Create the Docker image

!!! exercise "Question"
    Test the Docker image locally

!!! exercise "Question"
    Create a new repository `aps03_<INSPER_USERNAME>` in ECR

!!! exercise "Question"
    Tag and push your image to the ECR repository

!!! exercise "Question"
    Create a lambda function associated with your image

!!! exercise "Question"
    Test the lambda function

!!! exercise "Question"
    Create an API Gateway and test it.

    Leave in the README an example of how to test your API Gateway (curl command or Python code).

## Part 2

This APS requires that you use the **Terraform** setup to create the Lambda function and API Gateway.

Use the past pages as a reference.

It's advisable to study about and implement:

- How to use Terraform Modular Configuration (project structure)?
- How to perform Variable Validation (e.g Lambda memory size)?
- How to use Remote State (S3) to store Terraform state remotely for team collaboration?

!!! exercise "Question"
    Create a good `README.md` file.
    
    - Explain how to deploy your project.

    - Leave in the `README.md` an example of how to test your API Gateway (curl command, bash script or Python code).

!!! exercise "Question"
    Commit and push: mission accomplished!

## Rubrics

- To be released