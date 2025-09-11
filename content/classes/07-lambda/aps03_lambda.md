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

!!! warning
    In the upcoming exercises, you will write scripts to provision resources (repository creation, functions, API, etc.).
    
    If You prefer, you may use the Terraform setup right away (as will be required in Part 2).

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
    Redo all the steps from Part I using Terraform to provision infrastructure (where applicable).

!!! exercise "Question"
    Create a good `README.md` file.
    
    - Explain how to deploy your project.

    - Leave in the `README.md` an example of how to test your API Gateway (curl command, bash script or Python code).

## Delivering the assignment

!!! exercise "Question"
    Commit and push before the [deadline](../../deadlines.md): mission accomplished!

After pushing the code on GitHub, to achieve the highest grade, the student must inform the professor (in class or during office hours) that they wish to present the project. The presentation will involve showing that the project works and discussing its components, possibly demonstrating that they studied or learned beyond the project requirements (if that was the case).

Before starting this stage, it is advisable to have the repository open (both on GitHub’s website and in VSCode), have the deployment completed and functional on AWS, and have code or calls ready to demonstrate its operation.

Students who do not present their project to the professor will have their maximum grade restricted at a B.

## Deadlines

- **Github submission Deadline**: available [here](../../deadlines.md)
- **Presentation deadline (only for maximum concept)**: october 15th.



## Rubrics

| Concept | Criteria |
|---------|----------|
| I (Insufficient) | Did not complete the required steps, major components missing, or solution does not work. |
| D (Developing) | Attempted some steps, but with significant errors or missing parts; solution is incomplete or unreliable. |
| C (Essential) | Completed all required steps from Part 1; solution works but lacks polish or best practices, improvements possible. |
| B (Above Average) | Solution is robust (both Part 1 and 2), well-documented (wrote a good README), follows best practices. |
| A (Excellent) | Presented the project to the professor during class or office hours. Demonstrates deep understanding and extra effort. The Terraform infrastructure state is maintained centrally in S3. |