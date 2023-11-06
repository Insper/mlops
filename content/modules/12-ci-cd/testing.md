# Testing

Let's build an action on github that runs automatic tests whenever a push is made to the main branch.

First, we will need to build the testing infrastructure in a repository.

## Create Repository

!!! exercise "Question"
    Create a **private** repository for the class and clone it on your machine.

    !!! info ""
        This activity is just for practice! It isn't part of mandatory APSs!

!!! exercise "Question"
    Create an `.gitignore` file. Ignore, at least:

    - `.env`
    - `__pycache__`


## Create Folders

!!! exercise "Question"
    Create the files and folder tree at the root of the repository.

    ```console
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── src/
    └── tests/
    ```

Let's create a lambda function similar to those created in previous classes. It will be a simple word processing function.

!!! exercise "Question"
    Create the file `src/word_count.py` with the content:

    ```python
    def word_count_handler(event, context):
        msg = event["body"]

        n_words = len(msg.split())

        return {"len": len(msg), "words": n_words}
    ```

    Now the file tree will be:

    ```console
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── src
    │   └── word_count.py
    └── tests/
    ```

## Add Testing

Let's add **unit tests** to our project. Initially we will run the tests **locally**. Then, we will automate this task to be executed in a **github action**.

!!! exercise "Question"
    Add `pytest` to `requirements.txt`.

!!! exercise "Question"
    Create the file `pytest.ini` (at root) with the content:

    ```ini
    [pytest]
    pythonpath = src
    ```

    This will enable module importing during test running.

!!! exercise "Question"
    Create the file `tests/test_word_count.py` with the content:

    ```python
    import pytest
    import sys
    import word_count as wc


    def test_simple_text_count():
        event = {"body": "Hello World"}
        expected = {"len": 11, "words": 2}

        # Test if return is as expected
        assert wc.word_count_handler(event, None) == expected
    ```

    Now the file tree will be:

    ```console
    ├── .gitignore
    ├── pytest.ini
    ├── README.md
    ├── requirements.txt
    ├── src
    │   └── word_count.py
    └── tests
        └── test_word_count.py
    ```

!!! exercise "Question"
    To check if the tests are passing, run:

    <p>
    <div class="termy">

    ```console
    $ pytest
    == test session starts ===
    platform linux -- Python 3.10.12, pytest-7.4.0, pluggy-1.2.0
    rootdir: /path/to/directory
    configfile: pytest.ini
    plugins: anyio-3.7.1
    collected 1 item                                                                                                     

    tests/test_word_count.py .                                                                                     [100%]

    === 1 passed in 0.00s ====
    ```

    </div>
    </p>

!!! exercise "Question"
    To finalize the edits, add basic project information to `README.md`!

## Automating

In an environment where several Data Scientists work on the data team's various projects, it is desirable that there are **automatic** verification routines whenever modifications are sent to the repository.

Let's see how to automate the execution of tests using *github actions*.

!!! tip "Tip!"
    Failing tests is a good indication that the code should not have been submitted and should not be deployed!

### Create Github Action

Let's create a **directed acyclic graph (DAG)** or **pipeline** with the sequence of steps to verify the tests in our repository.

The actions to be performed are stored in the `.github/workflows` folder in the repository root and are represented in **YAML** format.

!!! info "Info!"
    **YAML** is a human-readable data serialization standard used for configuration files!

!!! exercise "Question"
    Create the file `.github/workflows/test_workflow.yaml` with the content:

    ```yaml
    name: An example of an automatic testing action
    on:
      push:
        branches:
          - main
    jobs:
      build-and-test:
        runs-on: ubuntu-latest
        steps:

          - name: Checkout code
            uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v3
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: pip install -r requirements.txt

          - name: Run tests
            run: pytest
    ```

    Now the file tree will be:

    ```console
    ├── .github
    │   └── workflows
    │       └── test_workflow.yaml
    ├── .gitignore
    ├── pytest.ini
    ├── README.md
    ├── requirements.txt
    ├── src
    │   └── word_count.py
    └── tests
        └── test_word_count.py
    ```

Explaining workflow **YAML**:

- First, we provide a description for the workflow with:
```yaml
name: An example of an automatic testing action
```
- We set the action to be run whenever there is a `push` on the `main` branch when doing:
```yaml
on:
push:
    branches:
    - main
```
- To define a job, which is a group of steps that are executed together as part of a workflow run, we do:
```yaml
jobs:
build-and-test:
    runs-on: ubuntu-latest
    steps:
```
Note that we defined that the task must be executed in an `ubuntu` container.
!!! warning ""
    Github will deal with container creation and management.

    You have a free quota, see more [Here](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- Then we define a sequence of steps for our job:
    - To bring code from the repository into the container:
    ```yaml
    - name: Checkout code
      uses: actions/checkout@v3
    ```
    - To set up Python:
    ```yaml
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.10'
    ```
    - To install dependencies
    ```yaml
    - name: Install dependencies
      run: pip install -r requirements.txt
    ```
    - To run tests:
    ```yaml
    - name: Run tests
      run: pytest
    ```

### Check if it worked

Let's push the code to github and check if the action is executed correctly.

!!! exercise "Question"
    Go to the repository site at `https://github.com` and access the **Actions** tab.
    
    You don't need to do anything there for now, just leave it open to facilitate our check!

!!! exercise "Question"
    Run `git status` and check if all folders (including workflow) are listed and ready to be sent to github!

!!! exercise "Question"
    Then **commit** and **push** and go to the repository site at `https://github.com`.

    <p>
    <div class="termy">

    ```console
    $ git add .
    $ git commit -m "Try testing with gh actions"
    $ git push
    ```

    </div>
    </p>

    Refresh the **Actions** tab. You should see the action being runned.

    ![](github_actions_running.png)

    After some seconds, refresh the page and see the action in finished status, with success!

    ![](github_actions_finished.png)

!!! exercise "Question"
    Click on the workflow name (which has the commit message).
    
    You will see all the **jobs** of this workflow. In this case, just one: `build-and-test`.

    ![](github_actions_click.png)

    Click on `build-and-test` to see more details on each **step** of this **job**:

    ![](github_actions_details.png)

!!! exercise text long "Question"
    Will the commits be ignored on action fail?

    !!! answer "Answer"
        No! Although it is possible to configure this functionality, we did not do this.

## Tasks

!!! exercise "Question"
    Add the following to the final of `tests/test_word_count.py`:

    ```python
    def test_no_body():
        event = {}
        expected = {"error": "no body"}
        assert wc.word_count_handler(event, None) == expected
    ```

!!! exercise "Question"
    Check locally if the tests pass.

    Since the *body* key is not being sent but is being read in the function, the test should fail (**KEYERROR**).

    <p>
    <div class="termy">

    ```console
    $ pytest
    ```

    </div>
    </p>

!!! exercise "Question"
    Commit the changes and check if the action also fails.   

    ![](github_actions_fail.png)

!!! exercise "Question"
    Make corrections to the source code until the tests passes locally.
    
    !!! info ""
        Commit and verify that the action was also executed successfully!
