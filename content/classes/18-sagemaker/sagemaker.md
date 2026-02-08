# Sagemaker

## Notebook Instances

Notebook instances in AWS SageMaker are used when you need an interactive development environment based on Jupyter Notebooks in the cloud.

AWS Sagemaker notebook instances work similarly to a Jupyter Lab or Notebooks that we use daily, but running on AWS. They will be particularly useful because they do not require extensive local resources when analyzing data.

!!! info ""
    This way you won't have to worry about whether your computer has enough RAM or processing power!

Furthermore, integration with AWS S3 and other resources will be easier, due to being in the AWS environment.

## Create a Notebooks Instance

!!! tip "Tip!"
    Ensure that you have configured AWS credentials. Check this if you get any permission error.

    <p>
    <div class="termy">

    ```console
    $ aws configure
    ```

    </div>
    </p>

!!! exercise "Question!"
    To create a notebook instance, just run:

    !!! danger "Important!"
        Ask the professor which *role-arn* to use!

        Replace `ROLE_ARN` in the command with the provided *role-arn*.

    !!! danger "Important!"
        Replace `YOUR_INSPER_USERNAME` with your Insper user.

    <p>
    <div class="termy">

    ```console
    $ aws sagemaker create-notebook-instance \
        --notebook-instance-name "exp-note-YOUR_INSPER_USERNAME-01" \
        --role-arn "ROLE_ARN" \
        --instance-type "ml.t2.medium" \
        --volume-size-in-gb 10
    ```

    </div>
    </p>

    !!! Info "Important!"
        We define `ml.t2.medium` as the [VM type](https://aws.amazon.com/pt/sagemaker/pricing/) used by the instance. This is an important step as it will limit the amount of computing resources available to the notebook.

You will need to wait a few minutes for the instance to be available.

!!! exercise "Question!"
    To check the instance status, run:

    !!! danger "Important!"
        Replace `YOUR_INSPER_USERNAME` with your Insper user.

    !!! tip "Tip!"
        Repeat this process until the status changes from *Pending* to *InService*.

    <p>
    <div class="termy">

    ```console
    $ aws sagemaker describe-notebook-instance --notebook-instance-name "exp-note-YOUR_INSPER_USERNAME-01"
    ```

    </div>
    </p>

## Access the Instance

In the output returned by the `aws sagemaker describe-notebook-instance` command, look for the `Url`. 

!!! exercise "Question!"
    Access the `Url` in the browser.
    
    Choose the *IAM user* login option and use the login information provided by the professor.

    !!! danger "Attention!"
        Ensure that the URL accessed starts with `https`. Depending on the browser, access may not occur if it is not `https`!

!!! tip "Tip!"
    After accessing Jupyter Notebook, replace the end of the URL `/tree` with `/lab` if you want to access the Jupyter Lab version!

You are now accessing a Jupyter Notebook that is running on AWS! Let's bring some resources into this environment:

## Initial Exploration!


!!! exercise "Question!"
    Create a notebook **In your notebook instance in Sagemaker** with `conda_python3` kernel.

    We will use this notebook to download some other notebooks.

    Execute in any cell:

    ```console
    !wget https://mlops-material.s3.us-east-2.amazonaws.com/sagemaker/01-eda.ipynb
    !wget https://mlops-material.s3.us-east-2.amazonaws.com/sagemaker/02-train-model-on-instance.ipynb
    !wget https://mlops-material.s3.us-east-2.amazonaws.com/sagemaker/03-train-deploy.ipynb
    ```

!!! exercise "Question!"
    Open notebook `01-eda` **In your notebook instance in Sagemaker** and study its contents.

!!! exercise "Question!"
    Open notebook `02-train-model-on-instance.ipynb` **In your notebook instance in Sagemaker** and study its contents.

!!! exercise "Question!"
    Open notebook `03-train-deploy.ipynb` **In your notebook instance in Sagemaker** and study its contents.

# AWS Sagemaker Examples

!!! exercise "Question!"
    Access the **Sagemaker Examples** tab in the Jupyter Notebook root and check out the other example notebooks.

    ![](sagemaker_examples.png)

## Stop Instance

!!! danger "Important!"
    Delete resources at the end of class!

To prevent unnecessary resource expenditure, instances can be stopped and restarted as needed.

To **start**:

!!! danger "Important!"
    Replace `YOUR_INSPER_USERNAME` with your Insper user.

<p>
<div class="termy">

```console
$ aws sagemaker start-notebook-instance --notebook-instance-name "exp-note-YOUR_INSPER_USERNAME-01"
```

</div>
</p>

To **stop**:

!!! danger "Important!"
    Replace `YOUR_INSPER_USERNAME` with your Insper user.

<p>
<div class="termy">

```console
$ aws sagemaker stop-notebook-instance --notebook-instance-name "exp-note-YOUR_INSPER_USERNAME-01"
```

</div>
</p>

To **delete**:

!!! danger "Important!"
    Replace `YOUR_INSPER_USERNAME` with your Insper user.

<p>
<div class="termy">

```console
$ aws sagemaker delete-notebook-instance --notebook-instance-name "exp-note-YOUR_INSPER_USERNAME-01"
```

</div>
</p>


## References
- Beginning MLOps with MLFlow. Chapter 5.
- https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html
