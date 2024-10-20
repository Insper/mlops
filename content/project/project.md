# MLOps Project

## Main Goal

The MLOps project will involve taking an existing Machine Learning model and **operationalizing** it to be deployed and monitored in a **production environment**. This process will require several key steps to prepare the model for production.

## Major Tasks

The first major task will be to search for and acquire the necessary **data** and **code** to build and train a ML model. You have a few options for sourcing this initial model code and data. One approach would be to search for and utilize a model you previously developed and trained during another ML or Data Science course offered through Insper. This has the benefit of leveraging work you have already completed and are familiar with.

Alternatively, you could search online repositories like Kaggle to find **pre-existing Jupyter notebooks** containing example code to train models. **Kaggle** is a rich source for finding well documented sample notebooks covering common ML tasks and algorithms. When selecting a notebook, aim to choose one focused on a standard classification or regression problem with clearly documented code to load data, preprocess features, train a model, and evaluate results.

Once you have located suitable code and data to train a baseline ML model, the next step will be to run the notebook code locally and train a model on your own machine. This will validate that you understand the code and can successfully replicate the model training process. Make sure to document any issues or modifications required along the way.

!!! info "Important!"
    While the initial model building may seem like the mostinteresting part, this course is focused on MLOps practices.
    
    So having a simple, functional model upfront allows us to dive deeply into **operationalizing** ML in a production setting.

With a trained model in hand, the real work of the MLOps project will begin! Your concern will be **turning this model into an ML product** and later tasks will involve:

- Documenting the model
- Organizing the repository
- Code refactoring
- Model deployment
- Model monitoring
- Automation
- Etc.

Until the **operationalization** of this model is **optimal**!

## Groups

The project can be developed individually or in pairs.

###  Accept Assignment

All deliveries will be made via github classroom.

Click [**Here**](https://classroom.github.com/a/nz9gwfgo) to accept assignment.

!!! danger "Attention"
    The first member creates the group, while the second just joins the group.

## Rubrics

- **I**:
    - Did not deliver or project was far below expectations.

- **D**:
    - Delivered the project but it has errors (faulty codes or scripts) OR
    - Highly disproportionate contribution among team members.

- **C**:
    - Delivered a video explaining the details of the project (problem, data, main MLOps details) AND
    - The project runs without errors AND
    - The project repository and other resources are well organized AND
    - The project is reproducible, i.e. there is good documentation of the project, source code and data.

- **B** (two items), **A** (four items or more):
    - Uses logging.
    - There is a clear process for collecting (if applicable), storing, and preprocessing data.
    - Performs data versioning or uses feature store.
    - There is an automated pipeline to deploy the models to production.
    - Monitors model performance in production.
    - Deals with degradation in model performance over time.

## Deadlines

- **Oct 28**: Create group and repository.
- **Nov 10**: Partial delivery. The model to be operated must have been chosen. The data and code that generate the model (a first dirty version) must be presented. Commit to github.com with evidences that the task was accomplished (don't commit large files).
- **Nov 29**: Final delivery. In this delivery, it will be necessary to add a report and a short video describing the implemented project and its functionalities. 