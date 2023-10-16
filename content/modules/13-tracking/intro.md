# Introduction

As computer engineers, we understand the significance of **code versioning** and **Git flow** in software development. It provides a systematic approach to managing code changes, enabling collaboration, version control, and seamless integration of new features.

![](git-flow-diagram.png)

!!! info "Important!"
    Git flow ensures a streamlined development process, allowing teams to work efficiently while maintaining code quality. 

!!! exercise text long "Question"
    Is using git important for MLOps? Explain.

!!! exercise text long "Question"
    Is using git **enough** to version ML products?

## Traditional Software Development

To be able to answer the last question, it is important to understand the differences between traditional software development and Machine Learning product development.

In general, software development focuses on meeting pre-established functional requirements. The final quality of the product is intrinsically related to the quality of the code.

On the other hand, in ML the objective usually involves a cycle of optimization of some metric (accuracy, MSE), quality also depends on the data in addition to the code and the development environment is more diverse than in traditional software development.

## ML Lifecycle

!!! exercise text long "Question"
    Think you developed an ML product, you can imagine that the deployment has already been carried out. Could you list any scenario where it is necessary to modify the project? What changes could be made?!

    !!! answer "Answer!"
        Some possibilities, among others:

        - Retraining the same model on new data.
        - Adding new features to the model.
        - Developing new algorithms.

        !!! info "Important!"
            During these modifications, it will be desirable to compare metrics to validate whether the modifications actually improve the model performance.

!!! danger ""
    Imagine you updating a model and trying to make these changes. After testing two or three algorithms, new features, new parameters, you will probably be lost, not knowing which result came from which version of the model.

    A representation of this data scientist, according to DALL·E 3 😄:

    ![](lost_data_scientist.jpeg)


We can see that ML projects involve not only code but also data, models, and experiments. The ML Lifecycle will include a lot of trial and error, hypothesis testing and monitoring to ensure quality of the delivered product.

Managing the versioning and reproducibility of ML models and datasets is crucial for ensuring the reliability and consistency of results.

## MLflow

MLflow is an API that allows you to integrate MLOps principles into your projects with minimal
changes made to existing code, providing a comprehensive framework for managing and organizing ML workflows.

With MLflow tracking, developers can easily log and monitor parameters, metrics, and artifacts generated during ML runs and analyze relevant details of ML projects.

Some key concepts of MLflow are:

- **Experiment**: An experiment represents a specific machine learning task or project. It acts as a container for runs and helps organize and group related runs together.
- **Run**: A run represents a specific execution of an MLflow script or code. It captures the parameters, metrics, and artifacts generated during the run.
- **Parameters**: Parameters are inputs or configurations that define an MLflow run. They can be hyperparameters, model configurations, or any other variables that affect the experiment's outcome.
- **Metrics**: Metrics are measurements or evaluation criteria used to assess the performance of a model during training or evaluation. MLflow allows logging various metrics such as accuracy, loss, F1-score, or any other custom metric.
- **Artifacts**: Artifacts are the output files generated during an MLflow run, such as trained models, visualizations, or data files.
- **Tags**: Tags are user-defined key-value pairs that provide additional metadata for experiments and runs. They can be used to add descriptive labels, track specific attributes, or categorize experiments based on certain criteria.

Advance to the next topic, where we will see in practice how to use MLflow to track the development of an ML product.