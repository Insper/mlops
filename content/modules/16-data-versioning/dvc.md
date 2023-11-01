# DVC: Data Versioning Control

Let's learn how to use tools for **data versioning**.

We already know the most famous versioning tool: `git`!

!!! exercise text long "Question!"
    Do you think we can we use `git` to version our **parquets** and **CSVs**? Explain whether or not this is a good idea.

    !!! answer "Answer!"
        It is possible, but it is not the best approach. Git is primarily designed for versioning **source code** and text-based files, it doesn't provide efficient storage and diffing capabilities for large and frequently changing binary files used in ML.

## An Alternative

In this class we will explore [DVC](https://dvc.org/), an open-source version control system for Data Science and ML projects. DVC provides a **git-like experience** to organize your data, models, and experiments.

!!! info "From the DVC creators"
    *DVC* is a tool for data science that takes advantage of existing software engineering toolset.
    
    It helps ML teams manage **large datasets**, **make projects reproducible**, and **collaborate better**.

## Create repository

!!! exercise "Question!"
    Create a private repository to be used in the experiment and clone it on your machine.

    !!! info ""
        If you create a public repository the `dvc` will also work! It's just a recommendation that it be a private repository.

!!! danger "Important!"
    Access the repository folder and work from there!

## Install `dvc`

!!! exercise "Question!"
    Create (or activate) a virtual environment to be used in class.

!!! exercise "Question!"
    After activating the environment, we install `dvc` with:

    <p>
    <div class="termy">

    ```console
    $ pip install -U pip
    $ pip install "dvc[s3]"
    ```

    </div>
    </p>

## Use `dvc`

Let's initialize `dvc` in our repository.

!!! exercise "Question!"
    Make sure you are at the root of the repository and run:

    <p>
    <div class="termy">

    ```console
    $ dvc init
    ```

    </div>
    </p>

Then, we can use `dvc` to download a dataset.

!!! exercise "Question!"
    To download a dataset, run:

    <p>
    <div class="termy">

    ```console
    $ dvc get-url https://mlops-material.s3.us-east-2.amazonaws.com/data_v0.csv  data/data.csv
    ```

    </div>
    </p>

!!! tip "Tip!"
    You could have used any tool (curl, wget) to download this file.

    If this file was in a **git repository**, you could use `dvg get` instead of `dvc get-url`.

!!! exercise "Question!"
    Then we configure `dvc` to track the `data/data.csv` file with:

    <p>
    <div class="termy">

    ```console
    $ dvc add data/data.csv
    ```

    </div>
    </p>

!!! exercise "Question!"
    And commit changes with:

    <p>
    <div class="termy">

    ```console
    $ git add data/data.csv.dvc data/.gitignore
    $ git commit -m "Add data to project"
    $ git push
    ```

    </div>
    </p>

!!! exercise choice "Question"
    Go to github.com and check out their repository. Browse the file structure and check which dvc files we don't commonly have in our repositories. Can you find the `data.csv` file?

    - [ ] Yes
    - [X] No

## Remotes

In *DVC*, **remotes** refer to the storage locations where you can store and retrieve your data, models, and other artifacts.

For this we can use, among other alternatives, a local folder or an S3 bucket.

First we will use a local folder.

!!! exercise "Question!"
    Create a folder `dvcstore` anywhere **outside the repository folder** and save its path:

    <p>
    <div class="termy">

    ```console
    $ mkdir /home/user/dvcstore
    ```

    </div>
    </p>

!!! exercise "Question!"
    Let's configure *DVC* to use this folder as remote storage:

    !!! danger "Attention!"
        Change `/home/user/dvcstore` to the path of the previously created folder!

    <p>
    <div class="termy">

    ```console
    $ dvc remote add -d myremote /home/user/dvcstore
    ```

    </div>
    </p>

!!! exercise "Question!"
    To upload data to the storage, run:

    !!! warning "Attention!"
        Out of curiosity, check that your storage folder is empty before running!

    <p>
    <div class="termy">

    ```console
    $ dvc push
    ```

    </div>
    </p>

    !!! warning "Attention!"
        Check that your storage folder is not empty after running!

### Testing the remote

To check if *DVC* is actually tracking the file, let's simulate a deletion and restoration of the `data/data.csv` base.

!!! exercise "Question!"
    To do this, run:

    <p>
    <div class="termy">

    ```console
    $ rm -rf .dvc/cache
    $ rm -f data/data.csv
    ```

    </div>
    </p>

!!! exercise "Question!"
    Check that the file has indeed been **deleted**

    <p>
    <div class="termy">

    ```console
    $ ls -la data/
    ```

    </div>
    </p>

!!! exercise "Question!"
    To restore the file we can do:

    <p>
    <div class="termy">

    ```console
    $ dvc pull
    ```

    </div>
    </p>

!!! exercise "Question!"
    Check that the file has indeed been **restaured**

    <p>
    <div class="termy">

    ```console
    $ ls -la data/
    ```

    </div>
    </p>

## Checkout to version

When developing with `git`, it is common to do *checkout* to explore a specific version of the software to be developed.

With *DVC*, we added the ability to maintain **data versioning**, without necessarily using the repository as storage.

!!! exercise "Question!"
    Let's ensure that all changes so far have been committed.

    <p>
    <div class="termy">

    ```console
    $ git add .
    $ git commit -m "version 0"
    $ git push
    ```

    </div>
    </p>

To make it easier to understand, let's create a *tag*:

!!! tip "Tip!"
    A git tag is a named reference to a specific commit in a Git repository.

!!! exercise "Question!"
    To create the tag `v0.0.0`, run:

    <p>
    <div class="termy">

    ```console
    $ git tag -a v0.0.0 -m "Release version 0.0.0"
    ```

    </div>
    </p>

Let's simulate that the data scientist identified the need to add new features to improve the model's performance.

!!! exercise "Question!"
    A new file has been prepared by the professor and can be downloaded with:

    <p>
    <div class="termy">

    ```console
    $ dvc get-url --force https://mlops-material.s3.us-east-2.amazonaws.com/data_v1.csv  data/data.csv
    ```

    </div>
    </p>

!!! warning "Attention!"
    After downloading, open the file `data/data.csv` and see that it has more columns than the previous version!

!!! warning "Attention!"
    create a new `src/train.py` file to simulate some source code addition:

    ```python
    # simulate trainning. No need to add source code!
    ```

!!! exercise "Question!"
    Commit the changes, both in `git` and `dvc`:

    <p>
    <div class="termy">

    ```console
    $ dvc commit data/data.csv
    $ dvc push

    $ git add .
    $ git commit -m "version 1"
    $ git push
    ```

    </div>
    </p>

!!! exercise "Question!"
    Create a new `v0.0.1` tag with:

    <p>
    <div class="termy">

    ```console
    $ git tag -a v0.0.1 -m "Release version 0.0.1"
    ```

    </div>
    </p>

Now we can switch between versions, checking out both `git` and `dvc`. This way, both the source code and the data are versioned!

![](project-versions.webp)

!!! warning "Attention!"
    Keep the file  `data/data.csv` open in VSCode and split your screen. This way you will be able to observe the modifications in the file as soon as the `checkout` occurs in *DVC*!

!!! exercise "Question!"
    To switch to version `v0.0.0` do:

    <p>
    <div class="termy">

    ```console
    $ git checkout v0.0.0
    $ dvc checkout
    ```

    </div>
    </p>

!!! warning "Attention!"
    Check if the `data/data.csv` file has been restored to the previous version.

!!! exercise "Question!"
    To switch to version `v0.0.1` do:

    <p>
    <div class="termy">

    ```console
    $ git checkout v0.0.1
    $ dvc checkout
    ```

    </div>
    </p>

!!! warning "Attention!"
    Repeat these last two steps a few times and check both the repository and the data being changed!

!!! info "Important"
    It is not mandatory to use `git tag`. You could checkout directly to a commit.

    We use the tag just to standardize and have a named commit!