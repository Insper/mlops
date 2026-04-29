# Evaluate Model Degradation

## Ground Truth Evaluation

We have already discussed the idea of monitoring model performance in production using metrics that could, for example, compare performance on the test set (separate during training) and the current data set in production.

This concept is known as **Ground Truth Evaluation**. It demands waiting for the occurrence of a labeled event. For example, in the case of a recommendation engine, it would determine whether a customer clicked on or purchased one of the recommended products.

Once the new ground truth data is gathered, the next step is to evaluate the models performance using this information and compare it against the predefined metrics established during the training phase.

!!! info "Decision making!"
    If the disparity between the model performance and the registered metrics exceeds a certain threshold, it signifies that the model has become outdated.

!!! exercise text short "Question!"
    What to do if the model's performance is below the threshold and we identify that the model has become outdated?

    !!! answer "Answer"
        Retrain the model on current data!  

!!! exercise text short "Question!"
    Once the need to retrain a model has been identified, why is it important to check if the distributions of features are **broadly similar** to those in the previous training set?

    !!! answer "Answer"
        The goal is to **refine** the model, not **radically change** it.

!!! exercise choice "Question"
    We can use **Ground Truth Evaluation** in all scenarios where we use ML models for regression or classification.

    This statement is:

    - [ ] True
    - [X] False

!!! exercise text long "Question!"
    Can you name any scenarios where using **Ground Truth Evaluation** is not practical or appropriate?

    !!! answer "Answer!"
        In scenarios where the events or outcomes of interest are **in the future** or have not occurred yet, so it becomes impractical to obtain ground truth data for evaluation.

        Think, for example, of **fraud detection** models. Sometimes it can take months for a credit card payment claim to be created.

        Another example: a model that predicts the occurrence of a disease in the next ten years requires a wait of up to ten years!

!!! tip "Tip!"
    When the **maturation time** of the target variable is high, the use of **Ground Truth Evaluation** may become not very practical!

!!! exercise text long "Question!"
    Think of some solution to still use Ground Truth Evaluation in this situation.

    !!! answer "Answer!"
        To address this challenge, one possible solution is to implement random labeling, which involves establishing a ground truth for a subset of the dataset chosen at random. This approach allows for a broader representation of the data, providing a more comprehensive evaluation of the model performance.

## Data Drift

Considering the challenges and limitations associated with Ground Truth Evaluation, a more practical alternative could be the use of **data drift** or **input drift detection**.

Rather than relying solely on ground truth labels, input drift detection focuses on **identifying changes in the input data** itself, without requiring explicit knowledge of the true outcomes. 

This approach offers a more feasible and efficient means of monitoring and maintaining machine learning models.

!!! tip "Tip!"
    We will compare the distribution of features in the data being predicted versus the distribution of features in the data used in training.

    Our goal is to check if **distribution** of the input data **changes over time**.

