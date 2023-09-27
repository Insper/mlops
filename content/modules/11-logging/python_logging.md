# Python Logging

!!! exercise text long "Question"
    Do you think that `print` function could be used for logging?

    !!! answer "Answer!"
        `print` is not suitable for comprehensive logging in production or professional software development! We want something more powerful!

## Python Logging

The `logging` library in Python is a powerful and versatile tool for capturing and managing log information within your Python applications. It offers a wide range of features and capabilities that enhance the logging experience.

Save and run this source code:

```python
import logging

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
```

!!! exercise choice "Question"
    When running, were all messages displayed on standard output?

    - [ ] Yes
    - [X] No

!!! exercise text long "Question"
    Add in the line after `import logging`:
    ```python
    import logging

    logging.basicConfig(level=logging.CRITICAL)

    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    ```

!!! exercise text long "Question"
    Now try to run it and explain what happens:
    ```python
    import logging

    logging.basicConfig(level=logging.NOTSET)

    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    ```

    !!! answer "Answer!"
        **Logging levels** represent the severity or importance of log messages. They allow you to control which messages are logged based on their importance.

        The logging module defines the following logging levels in increasing **order of severity**:

        - **DEBUG**: Detailed information, typically useful for debugging purposes.
        - **INFO**: General information about the progress or state of the application.
        - **WARNING**: Indicates a potential issue or something that might cause problems later.
        - **ERROR**: Indicates an error that caused the application to fail to perform a specific function.
        - **CRITICAL**: Indicates a critical error that may result in the application terminating.

## Customize messages

It is possible to customize the messages displayed in the log, adding information about the date and time the event occurred, the level and message. For example:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
)

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
```

When running, the following messages are displayed:

<p>
<div class="termy">

    ```console
    $ python3 test_log.py 
    23-09-26 12:40     root     INFO     This is an info message
    23-09-26 12:40     root     WARNING  This is a warning message
    23-09-26 12:40     root     ERROR    This is an error message
    23-09-26 12:40     root     CRITICAL This is a critical message
    ```

</div>
</p>

## Save Logs to files

In machine learning, a baseline model refers to a simple and often rudimentary model that serves as a starting point for comparison with more complex and sophisticated models. It provides a benchmark or reference point against which the performance of other models can be evaluated.

Let's code a class called `BaselineModel` that can be trained with any `X` array:

```python
import numpy as np


class BaselineModel:
    """
    Baseline model. Return average value!
    """

    def __init__(self):
        self.model = None
        self.pred = None

    def fit(self, X, y):
        """
        Fit the model.
        """
        self.pred = np.average(y)

    def predict(self, X):
        """
        Predict the value (returns trained average).
        """
        return self.pred


def test_baseline_model():
    """
    Test if BaselineModel returns the correct value.
    """
    X = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([1, 2])
    model = BaselineModel()
    model.fit(X, y)

    # The average of [1,2] is 1.5!
    assert model.predict(X) == 1.5


if __name__ == "__main__":
    test_baseline_model()

```

Let's add logging to a file, with information and verification of the data used for training. Modify the file:

!!! warning "Changes!"
    Modifications were made to the `fit` function, main and the `config_logging` function!

```python
import logging
import numpy as np


class BaselineModel:
    """
    Baseline model. Return average value!
    """

    def __init__(self):
        self.model = None
        self.pred = None

    def fit(self, X, y):
        """
        Fit the model.
        """
        if len(y) < 30:
            logging.warning("y is small!")
        logging.info("Fitting model...")
        self.pred = np.average(y)

    def predict(self, X):
        """
        Predict the value.
        """
        return self.pred


def test_baseline_model():
    """
    Test if BaselineModel returns the correct value.
    """
    X = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([1, 2])
    model = BaselineModel()
    model.fit(X, y)

    # The average of [1,2] is 1.5!
    assert model.predict(X) == 1.5


def config_logging():
    """
    Configure Logging
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
        datefmt="%y-%m-%d %H:%M",
        filename="baseline.log",
        filemode="a",
    )

    logging.basicConfig(level=logging.NOTSET)


if __name__ == "__main__":
    config_logging()
    test_baseline_model()

```

Check the results:

<p>
<div class="termy">

    ```console
    $ cat baseline.log 
    23-09-26 14:03     root     WARNING  y is small!
    23-09-26 14:03     root     INFO     Fitting model...
    ```

</div>
</p>

Think carefully about your logging functions and avoid complex outputs like:
```python
"x=1, sp=3 0xA32341 192.168.20.100"
```

!!! tip "Work Hard!"
    Producing **meaningful output** that aids in **understanding** a program's state requires **dedicated effort**.

!!! danger "Danger!"
    The `logging` module provides built-in support for **thread-safe logging**.

    But the `logging` module is not **process-safe**. However, it provides an additional handler called `logging.handlers` to deal with that!

See more [**here**](https://docs.python.org/3.10/howto/logging.html#logging-advanced-tutorial) and [**here**](https://docs.python.org/3.10/howto/logging-cookbook.html#logging-cookbook)!