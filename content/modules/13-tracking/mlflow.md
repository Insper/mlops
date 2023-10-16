# Practicing

## Installing MLflow

To install MLflow, run:

!!! tip "Tip!"
    Remember to activate the course environment (`conda` or `venv`) or create one for this class!

<p>
<div class="termy">

```console
$ pip install mlflow
```

</div>
</p>

## Base Code

Before including MLflow resources in our project, let's consider the following structure, containing the necessary files to work with:

```console
├── data
│   ├── Churn_Modelling.csv
└── src
    └── train.py
```

!!! exercise "Question"
    Create the folder and file structure.
    
    The *CSV* file can be found [HERE](https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction/data).

    The source code of the `train.py` file can be found below. 

??? "Click to see `train.py` source code!"

    ```python
    """
    This module contains functions to preprocess and train the model
    for bank consumer churn prediction.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.utils import resample
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.compose import make_column_transformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix,
        ConfusionMatrixDisplay,
    )


    def rebalance(data):
        """
        Resample data to keep balance between target classes.

        The function uses the resample function to downsample the majority class to match the minority class.

        Args:
            data (pd.DataFrame): DataFrame

        Returns:
            pd.DataFrame): balanced DataFrame
        """
        churn_0 = data[data["Exited"] == 0]
        churn_1 = data[data["Exited"] == 1]
        if len(churn_0) > len(churn_1):
            churn_maj = churn_0
            churn_min = churn_1
        else:
            churn_maj = churn_1
            churn_min = churn_0
        churn_maj_downsample = resample(
            churn_maj, n_samples=len(churn_min), replace=False, random_state=1234
        )

        return pd.concat([churn_maj_downsample, churn_min])


    def preprocess(df):
        """
        Preprocess and split data into training and test sets.

        Args:
            df (pd.DataFrame): DataFrame with features and target variables

        Returns:
            ColumnTransformer: ColumnTransformer with scalers and encoders
            pd.DataFrame: training set with transformed features
            pd.DataFrame: test set with transformed features
            pd.Series: training set target
            pd.Series: test set target
        """
        filter_feat = [
            "CreditScore",
            "Geography",
            "Gender",
            "Age",
            "Tenure",
            "Balance",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "EstimatedSalary",
            "Exited",
        ]
        cat_cols = ["Geography", "Gender"]
        num_cols = [
            "CreditScore",
            "Age",
            "Tenure",
            "Balance",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "EstimatedSalary",
        ]
        data = df.loc[:, filter_feat]
        data_bal = rebalance(data=data)
        X = data_bal.drop("Exited", axis=1)
        y = data_bal["Exited"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=1912
        )
        col_transf = make_column_transformer(
            (OneHotEncoder(handle_unknown="ignore", drop="first"), cat_cols),
            remainder="passthrough",
        )

        X_train = col_transf.fit_transform(X_train)
        X_train = pd.DataFrame(X_train, columns=col_transf.get_feature_names_out())

        X_test = col_transf.transform(X_test)
        X_test = pd.DataFrame(X_test, columns=col_transf.get_feature_names_out())

        return col_transf, X_train, X_test, y_train, y_test


    def train(X_train, y_train):
        """
        Train a logistic regression model.

        Args:
            X_train (pd.DataFrame): DataFrame with features
            y_train (pd.Series): Series with target

        Returns:
            LogisticRegression: trained logistic regression model
        """
        log_reg = LogisticRegression(max_iter=1000)
        log_reg.fit(X_train, y_train)
        return log_reg


    def main():
        df = pd.read_csv("data/Churn_Modelling.csv")
        col_transf, X_train, X_test, y_train, y_test = preprocess(df)
        model = train(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"Accuracy score: {accuracy_score(y_test, y_pred):.2f}")
        print(f"Precision score: {precision_score(y_test, y_pred):.2f}")
        print(f"Recall score: {recall_score(y_test, y_pred):.2f}")
        print(f"F1 score: {f1_score(y_test, y_pred):.2f}")

        conf_mat = confusion_matrix(y_test, y_pred, labels=model.classes_)
        conf_mat_disp = ConfusionMatrixDisplay(
            confusion_matrix=conf_mat, display_labels=model.classes_
        )
        conf_mat_disp.plot()
        plt.show()


    if __name__ == "__main__":
        main()
    ```

!!! exercise text long "Question"
    Take a few minutes to read the source code of the `train.py` file and understand what is being done.

    Identify the lines where:

    - Resampling is done to ensure balance between classes.
    - Separation is made between training and testing.
    - Transformations are created in the columns for categorical variables
    - The model is trained.
    - Metrics are calculated on the test suite.
    - The confusion matrix is generated.

!!! exercise "Question"
    From the root directory, test the code with:
    <p>
    <div class="termy">

    ```console
    $ python src/train.py
    ```

    </div>
    </p>

You will notice that nothing is **registered**, all results from model training code are just displayed on screen.

To be able to make changes to the data or code and compare the results, we will use **MLflow** to track experiments.

## MLflow Logging

To track our ML experiments, let's change the `train.py` file, as required in the next exercises.

!!! exercise "Question"

    Import MLflow:

    ```python
    import mlflow
    ```

!!! exercise "Question"
    Then, we will set up an experiment.

    Change the `main` function source code. In the first line add:

    ```python
    mlflow.set_experiment("churn-exp")
    ```

    Where `"churn-exp"` is the name chosen for our experiment.

!!! exercise "Question"
    Now let's initialize an experiment and leave all the `main` function code as part of the experiment. The `main` function code will look like this:

    ```python
    def main():
        mlflow.set_experiment("churn-exp")
        with mlflow.start_run():
            df = pd.read_csv("data/Churn_Modelling.csv")
            # ... rest of the source code
    ```

!!! exercise "Question"
    Log metrics after calculating them in the `main` function. For example:

    ```python
    mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
    mlflow.log_metric("precision", precision_score(y_test, y_pred))
    ```

## Tracking UI

The **Tracking UI** provides a user-friendly interface to visualize, search, and compare runs in **MLflow**. It also allows you to download run artifacts and metadata for further analysis in external tools.

A `mlruns` folder was probably created by MLflow to store the tracking data. The file structure should look like:

```console
├── data
│   └── Churn_Modelling.csv
├── mlruns
│   ├── 0
│   │   └── meta.yaml
│   ├── 981952663556035646
│   │   ├── 15b47ca85fd84bd396b49e640c54d379
│   │   │   ├── artifacts
│   │   │   ├── meta.yaml
│   │   │   ├── metrics
│   │   │   │   ├── accuracy
│   │   │   │   └── precision
│   │   │   ├── params
│   │   │   │   ├── feature_names
│   │   │   │   └── max_iter
│   │   │   └── tags
│   │   │       ├── mlflow.runName
│   │   │       ├── mlflow.source.name
│   │   │       ├── mlflow.source.type
│   │   │       └── mlflow.user
└── src
    └── train.py

```

Then, navigate to the parent directory of mlruns (project root directory) in your terminal and run the command:

<p>
<div class="termy">

```console
$ mlflow ui -p 5005
```

</div>
</p>

!!! tip "Tip!"
    The `-p 5005` defines a port for the application. Use another port if it is occupied!

### Access the UI

Access the link [http://localhost:5005](http://localhost:5005) in the browser. You should see the MLflow graphical interface.

The default interface is:

![](mlflow_ui.png)

But since we already ran an experiment, you should see it in the left menu with the name `"churn-exp"`.

When you click on *churn-exp*, you should see a *run* of the experiment on the right, with some random name!

![](mlflow_ui_churn.png)

!!! exercise "Question"
    Click on the *run name* (in red in the image) to see the details of this run of the experiment.

    You should be able, for example, to see the model's metrics log.

    ![](mlflow_ui_metrics.png)

## Practicing

!!! exercise "Question"
    If you haven't already done so, log all metrics present in the source code.

!!! exercise "Question"
    It is also possible to define a name for each *run*, in order to avoid those random names!

    To do this, we use:

    ```python
    def main():
        mlflow.set_experiment("churn-exp")
        with mlflow.start_run():
            # Set a custom run name
            run_name = "Some custom run name"
            mlflow.set_tag("mlflow.runName", run_name)

            df = pd.read_csv("data/Churn_Modelling.csv")
            # ... rest of the source code
    ```

    Run the code and check the result in the *MLflow UI*. There must be a *run* with the chosen name.

!!! exercise "Question"
    Use the `mlflow.log_param` function to log the `max_iter` parameter during logistic regression model training:

    ```python
    mlflow.log_param("max_iter", 1000)
    ```

!!! exercise "Question"
    Use the `mlflow.log_param` to log feature names.

!!! exercise "Question"
    Use the `mlflow.log_image` to log the confusion matrix.

    When clicking on *run name*, the image should be available in *Artifacts*:

    ![](mlflow_ui_log_image.png)

!!! exercise "Question"
    Change the creation of *ColumnTransformer*, adding a `StandardScaler` to the numeric features:

    ```python
    col_transf = make_column_transformer(
        (StandardScaler(), num_cols), #  <--- change HERE
        (OneHotEncoder(handle_unknown="ignore", drop="first"), cat_cols),
        remainder="passthrough",
    )
    ```

    You will need to import:

    ```python
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    ```

    Name the *run* appropriately and check the result in the MLflow graphical interface.

    ![](mlflow_ui_scaler.png)

    When you click on *run name*, check if you can see a graph comparing the metrics of the version with and without the scaler.

!!! exercise "Question"
    Above where you see all the *run name* of the experiment, change the view from *Table* to *Chart*.
    
    Check if you can see a comparison of the **metrics** between the different *runs* of the experiment.

    ![](mlflow_ui_charts.png)


!!! exercise "Question"
    In *MLflow UI*, it is also possible to filter *runs*, for example, selecting those with some metric above a threshold.

    Use the filter to find *runs* with accuracy above `70%`.

    ![](mlflow_ui_filter.png)

!!! exercise "Question"
    Change the classification method to [`KNeighborsClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html).

    Perform a **Grid Search** for the best number of neighbors (ask Google or ChatGPT) and log the parameters and the results. Don't forget to choose a suitable name for your *run*!


!!! exercise "Question"
    Let's log the model.

    To do this, change the source code in the `train` function:

    ```python
    log_reg.fit(X_train, y_train)

    # Infer signature (input and output schema)
    signature = mlflow.models.signature.infer_signature(
        X_train, log_reg.predict(X_train)
    )

    # Log model
    mlflow.sklearn.log_model(
        log_reg,
        "model",
        signature=signature,
        registered_model_name="churn-model",
        input_example=X_train.iloc[:3],
    )
    ```

    Open *MLflow UI* and check the result. You should see information about the model under *Artifacts*.

    ![](mlflow_ui_model_artifacts.png)

    !!! tip "Tip!"
        The signature contains information about:

        - Input schema (features expected by the model at prediction time)
        - Output schema (what the model will return as predictions)

        See more [Here](https://mlflow.org/docs/latest/models.html#model-signature) and [Here](https://mlflow.org/docs/latest/models.html#model-signature-and-input-example).

Done! This way, with MLflow, we have a way to track our ML experiments!

## References

- Data: https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction/data
- Beginning MLOps with MLflow. Chapter 3 and 4.
- Introducing MLOps. Chapter 6.
- Git flow image: https://blog.kinto-technologies.com/assets/blog/authors/r.wen/git-flow-diagram.png