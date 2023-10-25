# Performance metrics

## Classification

Some performance metris used for classification problems are:

- **Accuracy**: Accuracy measures the proportion of **correctly classified** instances out of the **total number** of instances.

$$
A = (TP + TN) / (TP + TN + FP + FN)
$$

- **Precision**: Precision measures the proportion of **true positive** predictions out of **all positive** predictions. It focuses on the correctness of positive predictions.

$$
P = TP / (TP + FP)
$$

- **Recall** (Sensitivity or True Positive Rate): Recall measures the proportion of **true positive** predictions out of **all actual positive** instances.

$$
R = TP / (TP + FN)
$$

- **Specificity**: Specificity measures the proportion of **true negative** predictions out of **all actual negative** instances.

$$
S = TN / (TN + FP)
$$

- **F1 Score**: The F1 score combines **precision** and **recall** into a single metric. It provides a **balanced measure** between precision and recall.

$$
F = 2 * (P * R) / (P + R)
$$

- **Area Under the ROC Curve**: AUC-ROC is a commonly used metric for binary classification models. It measures the model's ability to distinguish between positive and negative instances across different thresholds.

!!! tip "Tip!"
    A classification problem refers to the task of categorizing or classifying input data into discrete classes or categories.

!!! exercise text long "Question!"
    Give an example of a situation where we should look at **precision** and **recall** and not just **accuracy**.
    
    !!! answer "Answer!"
        Let's assume that we are developing a classification model to detect a rare disease in patients. In this case, the disease may only affect a small proportion of the population, for example, 1%. If we build a model that labels all patients as not having the disease, we will have a high accuracy of 99%, as the majority of patients do not have the disease.

        However, accuracy alone is not sufficient to evaluate the effectiveness of the model in this context. The goal is to maximize the correct identification of patients with the disease (recall) and minimize the cases where the model erroneously labels a healthy patient as having the disease (precision).


## Regression

Some performance metris used for regression problems are:

- **Mean Absolute Error** (MAE): MAE measures the average absolute difference between the predicted and actual values. It provides a straightforward measure of the model's overall performance.

$$
MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|
$$

- **Mean Squared Error** (MSE): MSE measures the average squared difference between the predicted and actual values. It amplifies the impact of larger errors compared to MAE.

$$
MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

- **Root Mean Squared Error** (RMSE): RMSE is the square root of MSE and provides a measure of the average magnitude of the residuals.

$$
RMSE = \sqrt{MSE}
$$

- **R-squared** (Coefficient of Determination): R-squared represents the proportion of the variance in the dependent variable that is predictable from the independent variables.

$$
R^2 = 1 - \frac{SSR}{SST}
$$

where $SSR$ is the sum of squared residuals and $SST$ is the total sum of squares:

$$
SSR = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

$$
SST = \sum_{i=1}^{n} (y_i - \bar{y})^2
$$

- **Mean Absolute Percentage Error** (MAPE): MAPE measures the average percentage difference between the predicted and actual values.

$$
MAPE = \frac{1}{n} \sum_{i=1}^{n} \left|\frac{y_i - \hat{y}_i}{y_i}\right| \times 100
$$

- **Adjusted R-squared**: Adjusted R-squared adjusts the R-squared value by the number of predictors in the model. It penalizes the addition of unnecessary predictors and provides a more accurate measure of the model's goodness of fit.

$$
\text{Adjusted }\ R^2 = 1 - \left[ \frac{(1 - R^2) \times (n - 1)}{n - p - 1} \right]
$$

where $n$ is the sample size and $p$ is the number of predictors.

!!! tip "Tip!"
    A regression problem refers to the task of predicting a continuous numerical value.

!!! exercise text short "Question!"
    Give a reason to use $RMSE$ instead of $MSE$.
    
    !!! answer "Answer!"
        $RMSE$ is commonly used as it is in the same unit as the target variable.

!!! exercise text short "Question!"
    Give a reason to use $MAPE$ instead of $RMSE$.
    
    !!! answer "Answer!"
        $MAPE$ is often used in situations where relative errors are more important than absolute errors.

!!! tip "Tip!"
    The main advantage of these performance metrics is that they are **domain agnostic**, so the data scientist likely feels comfortable setting thresholds for them!

!!! tip "Tip!"
    But it is also important to choose metrics that are aligned with the business goal. Talk to the business areas to check this!

