# Structured Logging

## The Problem with Plain Text Logs

You already know how to use Python's `logging` module to write messages. Let's start by examining *why* unstructured text logs are painful in production ML systems.

Consider this log output from a model API:

```
2024-01-15 14:32:01 INFO Processing request
2024-01-15 14:32:01 INFO Prediction complete: 0.87
2024-01-15 14:32:02 INFO Processing request
2024-01-15 14:32:02 ERROR Model failed
2024-01-15 14:32:02 INFO Processing request
2024-01-15 14:32:02 INFO Prediction complete: 0.12
```

!!! exercise text long "Question"
    Your manager asks: *"How many requests failed in the last hour? What was the average prediction for successful requests? Which user submitted the request that failed?"*
    
    Can you answer these questions from the log above?

    !!! answer "Answer!"
        No. The logs are:
        
        - **Not queryable**: You'd need regex to extract anything
        - **Missing context**: No user ID, no request ID, no input features
        - **Hard to aggregate**: To compute averages you'd have to parse every line
        
        This is fine for a toy project. In production, with millions of requests per day and multiple services, this approach **does not scale**.

## Structured Logging: The Solution

**Structured logging** means emitting logs as **machine-parseable records** (typically JSON) instead of free-form strings. Each field becomes a named key, making logs queryable and aggregatable.

The same events as structured logs:

```json
{"timestamp": "2024-01-15T14:32:01Z", "level": "INFO", "request_id": "abc-123", "user_id": "u-42", "event": "prediction_complete", "prediction": 0.87, "latency_ms": 142, "model_version": "v2.1"}
{"timestamp": "2024-01-15T14:32:02Z", "level": "ERROR", "request_id": "def-456", "user_id": "u-17", "event": "model_failed", "error": "ValueError: input has NaN", "model_version": "v2.1"}
{"timestamp": "2024-01-15T14:32:02Z", "level": "INFO", "request_id": "ghi-789", "user_id": "u-42", "event": "prediction_complete", "prediction": 0.12, "latency_ms": 98, "model_version": "v2.1"}
```

!!! exercise text short "Question"
    With the structured logs above, can you now answer: *"What was the average prediction for successful requests?"*

    !!! answer "Answer!"
        Yes! Filter records where `event == "prediction_complete"` and compute the mean of the `prediction` field. In CloudWatch Logs Insights, this is a single query. In pandas, it's one line.

## Setting Up `structlog`

The standard `logging` module can produce JSON, but it requires boilerplate. The `structlog` library makes structured logging ergonomic.

!!! exercise "Question"
    Install `structlog`:

    <p>
    <div class="termy">

    ```console
    $ pip install structlog
    ```

    </div>
    </p>

## First Steps with `structlog`

Save and run this code:

```python
import structlog

log = structlog.get_logger()

log.info("prediction_complete", prediction=0.87, latency_ms=142)
log.warning("low_confidence", prediction=0.51, threshold=0.60)
log.error("model_failed", error="ValueError: input has NaN")
```

!!! exercise text short "Question"
    Run the code. What format does the output appear in?

    !!! answer "Answer!"
        By default, `structlog` uses a human-friendly colored format in development. Each key-value pair from your call appears as a separate field.

        Notice how **you never construct a string manually**. You pass context as keyword arguments.

## Configuring Output

For production, we want pure **JSON** output so log aggregation tools (CloudWatch, Datadog, etc.) can parse it automatically.

Save and run:

```python
import structlog
import sys

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(sys.stdout),
)

log = structlog.get_logger("ml_model")

log.info("prediction_complete", prediction=0.87, latency_ms=142, model_version="v2.1")
log.error("model_failed", error="ValueError: input has NaN", model_version="v2.1")
```

!!! exercise text short "Question"
    Run the code and inspect the output. Is it valid **JSON**? Try using `python -m json.tool` to confirm.

    !!! info "Info!"
        If you run `python -m json.tool` and paste the dicts, press `Ctrl+D` (EOF) to see the pretty-printed **JSON**.

## Correlation IDs

In a production system, a single user action may trigger multiple log events across multiple services. Without a way to correlate them, your logs are just independent islands of information.

A **correlation ID** (also called a **request ID** or **trace ID**) is a unique identifier attached to every log event belonging to the same request.

!!! exercise text long "Question"
    Picture someone sending a request to your ML API: the service cleans the input, runs the model, records the prediction, and then saves data to the database. If the database step fails, how can you identify exactly which request triggered the error when there is no correlation ID?

    !!! answer "Answer!"
        You can't, unless the request timestamp perfectly isolates the logs (fragile). With a correlation ID, you simply filter all logs by `request_id = "abc-123"` and get the full picture in one query.

Let's implement this pattern:

```python
import structlog
import logging
import sys
import uuid

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(sys.stdout),
)

log = structlog.get_logger()


def handle_request(payload: dict):
    # Generate a unique ID for this request and bind it to the logging context
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    log.info("request_received", payload_keys=list(payload.keys()))

    try:
        # Simulate preprocessing
        if "feature_1" not in payload:
            raise ValueError("Missing required feature: feature_1")

        # Simulate prediction
        prediction = 0.73
        log.info("prediction_complete", prediction=prediction, model="churn-v3")

    except ValueError as e:
        log.error("request_failed", error=str(e))
    finally:
        # Clear context so the next request starts clean
        structlog.contextvars.clear_contextvars()


# Simulate two concurrent requests
handle_request({"feature_1": 42, "feature_2": "yes"})
handle_request({"feature_2": "no"})  # Missing feature_1 (will fail)
```

!!! exercise "Question"
    Run the code above.

!!! exercise text long "Question"
    You see that `bind_contextvars` was called at the start and `clear_contextvars` in the `finally` block. Why is `clear_contextvars` in a `finally` block instead of the `try` block?

    !!! answer "Answer!"
        Because `finally` runs whether or not an exception was raised.

        If we put `clear_contextvars()` only in the `try` block, a crash would prevent cleanup, and the next request processed by the same thread would **inherit the previous request's context** , potentially leaking a `request_id` from one user to another.

## Logging ML-Specific Context

Now let's build a more realistic logging helper that captures everything useful for an ML prediction event:

```python
import structlog
import sys
import uuid
import time

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(sys.stdout),
)

log = structlog.get_logger()

MODEL_VERSION = "churn-v3.2"
CONFIDENCE_THRESHOLD = 0.65


def predict(features: dict) -> float:
    """Simulate a model prediction."""
    time.sleep(0.05)  # Simulate inference latency
    # Toy model: just sum and normalize
    return min(sum(features.values()) / 100, 1.0)


def handle_prediction_request(user_id: str, features: dict):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        user_id=user_id,
        model_version=MODEL_VERSION,
    )

    log.info("request_received", feature_count=len(features))

    start = time.monotonic()
    try:
        prediction = predict(features)
        latency_ms = round((time.monotonic() - start) * 1000, 2)

        log_data = dict(
            prediction=prediction,
            latency_ms=latency_ms,
            low_confidence=prediction < CONFIDENCE_THRESHOLD,
        )

        if prediction < CONFIDENCE_THRESHOLD:
            log.warning("low_confidence_prediction", **log_data)
        else:
            log.info("prediction_complete", **log_data)

        return prediction

    except Exception as e:
        latency_ms = round((time.monotonic() - start) * 1000, 2)
        log.error("prediction_failed", error=str(e), latency_ms=latency_ms)
        raise
    finally:
        structlog.contextvars.clear_contextvars()


# Simulate requests
handle_prediction_request("user-001", {"age": 35, "balance": 20, "campaign": 1})
handle_prediction_request("user-002", {"age": 55, "balance": 5, "campaign": 8})
```

!!! exercise text long "Question"
    Run the code and inspect the JSON events. What fields are shared across all events from the same request? What fields are specific to each event?

    !!! answer "Answer!"
        **Shared across events in a request** (bound via `bind_contextvars`):
        - `request_id`
        - `user_id`
        - `model_version`

        **Specific to each event** (passed as keyword arguments to the log call):
        - `feature_count` (on `request_received`)
        - `prediction`, `latency_ms`, `low_confidence` (on `prediction_complete` / `low_confidence_prediction`)

!!! exercise "Question"
    Modify the `predict` function to raise a `ValueError` when `features` is empty (`{}`). Then call `handle_prediction_request("user-003", {})` and verify that the error log is emitted with the correct `request_id` and `user_id`.

!!! exercise text short "Question"
    The `low_confidence` field is a boolean flag. Why is it useful to log this as a field rather than just changing the log level to `WARNING`?

    !!! answer "Answer!"
        Both are useful and complementary. Logging `low_confidence=True` as a structured field lets you:

        - **Query** CloudWatch Insights for `filter low_confidence = true`
        - **Count** low-confidence predictions per model version
        - **Alert** when the percentage of low-confidence predictions exceeds a threshold

        Log level filtering (`WARNING`) is coarser, you can't easily distinguish between a low-confidence prediction warning and an infrastructure warning at the same level.

## Logging to a File

Up to now, we've been printing to `stdout`. In production, you often want logs in a file *and* on `stdout` simultaneously:

```python
import structlog
import logging
import sys

# Standard logging handler for file output
logging.basicConfig(
    format="%(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),           # Terminal
        logging.FileHandler("predictions.log"),      # File
    ],
    level=logging.DEBUG,
)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

log.info("service_started", port=8080, model_version="churn-v3")
log.warning("high_latency_detected", latency_ms=850, threshold_ms=500)
```

!!! exercise "Question"
    Run the code above and verify that `predictions.log` was created with valid JSON logs.

    Inspect the file:

    <p>
    <div class="termy">

    ```console
    $ cat predictions.log
    ```

    </div>
    </p>

!!! exercise "Question"
    Try parsing the log file with Python:

    ```python
    import json

    with open("predictions.log") as f:
        for line in f:
            event = json.loads(line.strip())
            print(f"[{event['level'].upper()}] {event['event']} at {event['timestamp']}")
    ```

    This is exactly what log aggregation services do at scale.
