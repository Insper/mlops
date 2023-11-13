# Centralization

In the last class we saw how to use *MLflow* to track experiments.

!!! exercise text short "Question"
    Where was the information about the runs (metrics, parameters, artifacts) stored?

    !!! answer "Answer!"
        In a `mlruns` folder created by *MLflow*.

!!! exercise text long "Question"
    How will local storage of experiments impact a project developed by multiple ML scientists and engineers?

    !!! answer "Answer!"
        We may have a problem, as one will not have vision of what was attempted by the other.

It would be appropriate to keep information about experiments centrally. Thus, whenever an experiment is carried out by a data scientist, the result will be available for analysis by others.

!!! exercise text short "Question"
    Can you think of any solution to store metrics and parameter data centrally?

    !!! answer "Answer!"
        In a relational database!

!!! exercise text short "Question"
    Can you think of any solution to store artifacts, such as images and files, centrally?

    !!! answer "Answer!"
        S3 bucket!

## New scenario!

Let's propose a reconfiguration of the scenario from last class. In it, all structured information about the experiments will be stored in a PostgreSQL database, while the artifacts will be stored in an S3 bucket.

![](mlflow_integration.png)


!!! info "Important!"
    Now the results of the experiments will be available to everyone on the team!

The MLFlow server could also run centrally (like on an EC2 instance). However, we will keep it running locally, but storing data centrally.

## Create Database

!!! exercise "Question"
    Using the database credentials provided by the professor, make a connection to the database using DBeaver and create a database with the name following the pattern `mlflow_INSPER_USERNAME`.

    !!! danger "Important"
        Replace `INSPER_USERNAME` with your Insper username!

        When creating the database, use the **tablespace** `Default` instead of `pg_default`.

    !!! tip "Tip!"
        When creating the connection in DBeaver, in the second tab `"PostgreSQL"`, check the `"Show all databases"` option.

        ![](dbeaver_all_databases.png)

## Create Bucket

!!! exercise "Question"
    Create a bucket in AWS S3 to store your experiment artifacts.

    As we already have the AWS CLI configured, we will use it for this task. If you want, you can also use Python codes for this task!

    !!! danger "Important"
        Replace `INSPER-USERNAME` with your Insper username to configure S3 Bucket name properly.

    <p>
    <div class="termy">

    ```console
    $ aws s3api create-bucket --bucket mlflow-exp-tracking-INSPER-USERNAME --region us-east-2 --create-bucket-configuration LocationConstraint=us-east-2
    ```

    </div>
    </p>


## Configure MLflow Server

Now let's start a local MLflow server that will connect to the database and the S3 bucket.

!!! exercise "Question"
    Start the server with:

    !!! danger "Important"
        Replace `INSPER-USERNAME` with your Insper username to configure S3 Bucket name properly.

    !!! danger "Important"
        Fill in the database credentials provided by the professor: `USERNAME`, `PASSWORD`, `HOST`, `PORT`.
        
        For the `DATABASE`, use the one created by you, following the pattern `mlflow_INSPER_USERNAME`.

    <p>
    <div class="termy">

    ```console
    $ mlflow server --backend-store-uri postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE --default-artifact-root s3://mlflow-exp-tracking-INSPER-USERNAME
    ```

    </div>
    </p>

## Use MLflow Server

!!! exercise "Question"
    We will continue working on the same project as last class.

    Make a copy of the past class folder.

Let's configure the copy of the previous class project to connect to the server using the URL. Thus, MLflow will make requests to the REST API of the MLflow server that is running locally and, in turn, the server will store the experiment logs in PostgreSQL and AWS S3.

!!! exercise "Question"
    Change the code in the `train.py` file, in the `main` function, so that it uses the MLFlow server URL:

    !!! danger "Attention!"
        Add the line with `mlflow.set_tracking_uri` and keep the others!

    ```python
    def main():
        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("churn-exp")
    ```

    !!! tip "Tip!"
        Check if your server was actually started on port 5000.

    !!! tip "Tip!"
        Instead of leaving the URL hardcoded, try setting an **environment variable**.

!!! exercise "Question"
    From the root directory, test the code with:
    <p>
    <div class="termy">

    ```console
    $ python src/train.py
    ```

    </div>
    </p>

!!! exercise "Question"
    Go to http://localhost:5000 in your browser and check if the experiment results are available.

    Make sure your artifact URLs point to S3.

!!! exercise "Question"
    In DBeaver, explore the created tables and their contents.

!!! exercise "Question"
    List the contents of the bucket and check the created objects.

    !!! danger "Important"
        Replace `INSPER-USERNAME` with your Insper username to configure S3 Bucket name properly.

    <p>
    <div class="termy">

    ```console
    $ aws s3api list-objects-v2 --bucket  mlflow-exp-tracking-INSPER-USERNAME
    ```

    </div>
    </p>

    
## Interact with friends!

!!! exercise "Question"
    Talk to your colleagues to use the same database and bucket.
    
    This way you will be able to see in practice that you can integrate the experiments and visualize each other's results.

    !!! tip "Tip!"
        You can agree to run experiments with different names if you don't want to work on the same one!