# Logging

## Warming up

Analyze the following code:

```python
a = int(input())
b = int(input())

print(a / b)
```

!!! exercise text long "Question"
    Run the code and enter the values `3` and `2`. What happens?

    !!! answer "Answer!"
        `1.5` is printed in `stdout` (terminal).

!!! exercise text long "Question"
    Run the code and enter the values `6` and `0`. What happens?

    !!! answer "Answer!"
        An exception occurs, which is displayed in the terminal.


!!! exercise choice "Question"
    So the exception is also printed to stdout?

    - [ ] True
    - [X] False

    !!! answer "Answer"
        It is printed to `stderr`. In this case, `stdout` and `stderr` are both pointing to the terminal, but it could be different.

        Run the code and check:
        ```python
        import sys

        # Open a file in write mode to redirect stderr
        file = open("error_output.txt", "w")
        sys.stderr = file

        a = 5
        b = 0

        print(a / b)

        file.close()
        ```

        Now check the content of `error_output.txt` file.

## Logging Importance

Logging refers to the practice of **recording events** or **messages** from a software application, system, or device into a file or a centralized logging system.

Logging and monitoring are fundamental pillars of **DevOps** principles, playing a vital role in ensuring robust ML practices. It allows developers and data scientists to **track** the execution flow of an ML system, identify errors, and diagnose issues.

By logging relevant information, such as intermediate results, input data, and model predictions, it becomes easier to understand the **behavior of the ML system** and pinpoint the source of any problems.

In today's complex production infrastructures, which often involve multiple models deployed across multiple servers, effectively monitoring a live system, with or without machine learning components, entails **collecting** and **aggregating** data about its states. This highlights the increasing importance of having a robust logging system in place.

!!! info "Important!"
    Every **successful machine learning project** incorporates a **data feedback** loop, where **valuable information** from the **production** environment is fed back to the model prototyping environment to **enhance its performance**.

Advance to the next topic. Let's explore some logging options!

## References
- Practical MLOps. Chapter 6.
- Introducing MLOps. Chapter 7.
- https://docs.python.org/3/howto/logging-cookbook.html
- https://docs.python.org/3.10/library/logging.html