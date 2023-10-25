# Model Monitoring

From an MLOps point of view, Machine learning models need to be monitored at two levels:

- **Resource level**: we need to guarantee that the model is running correctly in the production environment. Here we monitor the CPU, RAM, storage and verify that requests are being processed at the expected rate and with no errors.

- **Performance level**: here we monitor the model performance to verify if it keep its relevance over time.

!!! info "Important!"
    In this class, we are more interested in exploring the latter case!

## Why?

But why do we need to monitor performance?

!!! exercise text long "Question!"
    Why wouldn't a model maintain its performance over time?

    !!! answer "Answer!"
        Variations in user behavior, for example, can mean that the **patterns learned during the training phase** are not **completely valid** anymore, resulting in **performance degradation**.

        As the world is constantly changing, a **static model cannot catch up with new patterns** that are emerging and evolving without a constant source of new data.

!!! info "Important!"
    For effective model monitoring, resources from previous classes may be required, such as **tracking** and **logging**!

## What is performance?

Model performance is a crucial aspect of ML that determines the effectiveness of the model in making predictions. 

Evaluating model performance involves the use of various metrics and techniques to assess how well the model generalizes to unseen data.

!!! exercise text long "Question!"
    Do you know any model performance metrics?

    !!! answer "Answer"
        Answered in the next topic!

