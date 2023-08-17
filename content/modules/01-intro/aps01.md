# Standards - Aps01

What is the size of a Data Science team? Considering data analysts, data engineers, data scientists, machine learning engineers, it is not uncommon for the professional count to reach hundreds. Across industries, companies are building [larger data science teams](https://www.statista.com/statistics/1136560/data-scientists-company-employment/) more and more.

So let's assume that the odds are high that you won't work alone on a data team. Imagine if each professional developed their models in a completely different way, without any:

- Language standards
- Libraries standards
- Code organization standards
- Concerns about the resources needed to deploy the models.

It is certain that this team will have difficulties in generating business value from ML!

In this activity, we will work on producing a **repository template**, defining standars that should be used on future projects. Let's assume that git is used for code versioning.

## Accept assignment

All assignments delivery will be made using Git repositories. Access the link below to accept the invitation and start working on the first assignment.

[Invitation link](https://classroom.github.com/a/UlzIvQ43){ .ah-button }

!!! important
    You should have received a new private repository. Copy your repo address below. It will be used in the rest of the guide.

    ![](repo_ex.png)

## Configure assignment repository

The supporting code for this activity is public in the repository [APS 01 MLOps](https://github.com/insper-classroom/mlops-aps01-marketing). In this guide we will configure your private repository to go along with this public repo.

To get started, create a new folder for your delivery repository and initialize an empty repo:

<div class="termy">

    ```console
    $ mkdir aps01
    $ cd aps01
    $ git init
    ```

</div>

First let's add the remote repository of support files and download the `main` branch (which contains this semester's files)

<div class="termy">

    ```console
    $ git remote add insper https://github.com/insper-classroom/mlops-aps01-marketing
    $ git fetch insper
    $ git checkout main
    ```

</div>

Now let's add the repository of your assignment and send the support code:

<div class="termy">

    ```console
    $ git remote add aps your_private_repo_addresss
    $ git push --set-upstream aps main
    ```

</div>

With that you should already have your local repository configured and pointing to two remote repositories:

- **insper**: this repo contains all support code for **aps01**. It is shared across the room and no one is allowed to push it.
- **aps**: this repo is yours alone and contains your work only. It will have only the modifications made by you.

You can check that everything worked by running `git branch -avv`.

Let's start by downloading the news from the support repository:

<div class="termy">

    ```console
    $ git fetch insper
    ```

</div>

Let's then embed the news in your local repository and push the new files to your private repo.

<div class="termy">

    ```console
    $ git switch main
    $ git merge insper/main
    $ git push
    ```

</div>

## Configure dev environment

Use a tool of your preference to create an isolated Python environment.

### With `conda`

<div class="termy">

    ```console
    $ conda create -n mlops python=3.10
    $ conda activate mlops
    ```

</div>


### With `venv`

- On Windows:
<div class="termy">

    ```console
    $ python3 -m venv mlops
    $ mlops\Scripts\activate
    ```

</div>

- On Linux/macOS:

<div class="termy">

    ```console
    $ python3 -m venv mlops
    $ source mlops/bin/activate
    ```

</div>

<br>

!!! Danger "Important!"
    Remember to add your **env** folder (`mlops` in the example) to `.gitignore`

## Task 01: Opening

Check the content of the `aps01` repository. Install the notebook package of your preference and open the notebook.

<div class="termy">

    ```console
    $ pip install jupyter
    ```

</div>

You you notice that everything was done in a single notebook. Data proccessing, analysis, model construction, etc.

There are those who defend the software production inside notebooks. There is even the area of **NDD** ([Notebook-Driven Development](https://github.com/fastai/nbdev)). It works when done right, but let's stay away from these people and take a more classical approach!

## Task 02: Organizing

Now you must configure the repository according to some standards. Let's create specific folders for each type of resource used in the project.

Think that all the repositories of the company should follow this organization pattern.

!!! exercise
    Let's organize the **data** resources. You must:

    1. Create a folder called `data`
    1. Move data files to this folder

!!! exercise
    For **notebooks**:

    1. Create a folder called `notebooks`
    1. Move notebook files to this folder

## Task 03: Split notebook code

Every code on this project is on a single notebook. We are going to split it considering the different functionalities provided.

!!! exercise
    Now you must:

    1. Create a folder called `src`
    1. Create a file `src/proccess.py` with all necessary code for data preprocessing. This code can generate a separeted file inside `data`.
    1. Create a folder called `models`
    1. Create a file `src/train.py` with all necessary code for model training. This code should export models to folder `models`.

Leave in the notebook only code for data exploration.

## Task 04: Prediction

Once the training algorithm, features and hyperparameters have been chosen, the final model to be deployed can be trained with a more complete set of data (and not just `X_train`). We will ignore this fact for now!

Also, when the model is in use (making predictions), the target variable is not needed or does not exist. That is, we need specific data and scripts for prediction.

In this activity, consider that whenever training needs to be redone, there will be a `bank.csv` file with updated data in the `data` folder.

!!! exercise
    Let's simulate the prediction data. Now you must:

    1. Copy the `data/bank.csv` file to a new `data/bank_predict.csv` file. This new file must not have the **target** column
    1. Create a file `src/predict.py` with all necessary code for making predictions on file `data/bank_predict.csv`. You should use the **pickle** files of the models.
    1. Create a new column `y_pred` on file `data/bank_predict.csv` with the prediction of your model mapped to `"yes"` or `"no"`.

At this point, you have a repository:
- With well-organized folders
- With specific code files to train a model
- With specific code files to use a model to make predictions

## Task 05: Readme

!!! exercise
    Create a `README.md` with some basic informations of the project

## Task 06: Dependencies

!!! exercise
    Create a `requirements.txt` with all the libs used on the project.


!!! exercise choice "Question"
    Should you set lib versions?

    - [X] Yes
    - [ ] No

    !!! answer "Answer"
        In production deployment, it's a good idea to track dependencies to maintain stability and reliability. Besides that, in some companies your will run in a cluster (spark) where all data scientists and machine learning engineers must to use the same library versions.

## Task 07: Create a template

Now that we've defined a repository standard, it would be nice to reuse it in new projects.

For that we will use `cookiecutter` to define a **template repository**. Then, when a new ML project is started, we will just use our template to start it.

In order to do this, you will need to **create a new public repository**. Create a public repository on your own Github called, for example, `23-2-mlops-template`.

!!! danger "Atention"
    To deliver this part of the assignment, paste the link to the template repository in the `README.md` of your private repository of `APS01`. Remember to push this change!

Then, create a folder structure similar to:

![](template_folder.png)

!!! info "Info!"
    The `.gitkeep` are empty files created to allow empty folders to be in the template

!!! exercise
    Create a `README.md` (root directory) with some basic informations of the template repository

!!! exercise
    Create the `cookiecutter.json` with the content:

    ```json
    {
        "directory_name": "project-name",
        "author_name": "Your Name",
        "compatible_python_versions": "^3.8"
    }
    ```

!!! exercise
    Create the `.gitignore` inside `{ {cookiecutter.directory_name} }` with the files to be ignored by default in future projects.

!!! exercise
    Create the `README.md` inside `{ {cookiecutter.directory_name} }` with the default **README** for future projects. Be creative!

    ![](readme_ex.png)

!!! exercise
    Create basic python files in `src` folder.

!!! exercise
    You can also leave some notebooks with basic code for exploratory data analysis.

!!! exercise
    Commit and push your changes to Github!


### Testing your template

Install `cookiecutter`:

<div class="termy">

    ```console
    $ pip install cookiecutter
    ```

</div>

Then use the command:

<div class="termy">

    ```console
    $ cookiecutter https://github.com/your_user/your_template_repository --checkout main
    ```

</div>

Done! It should create the folders and files structure defined in the template.

!!! danger "Remember!"
    Delivering the assignment is the same as pushing to the `main` branch of your private repository of `aps01`!