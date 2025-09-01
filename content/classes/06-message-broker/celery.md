# Celery

**Celery** is an open-source **distributed task queue system** written in Python, designed to manage the execution of tasks asynchronously across multiple workers.

!!! info "Info!"
    Celery is written in Python, but the protocol can be implemented in any language.
    
It operates on a **producer-consumer model**, where tasks are defined as units of work and are placed into a **queue**. These tasks are then picked up and processed by worker processes, which constantly monitor the task queue for new jobs.

Celery uses a **messaging broker**, such as **RabbitMQ** or Redis, to facilitate communication between the client that initiates the task and the worker that executes it. This system allows for **high availability** and **horizontal scaling**, making it possible to distribute work efficiently across different threads or machines.

Celery’s protocol can be implemented in various programming languages, enabling language interoperability and integration with diverse systems. For instance, Node.js and PHP have their own implementations, and HTTP endpoints can be used to connect Celery tasks with external services, further extending its versatility.

To practice, let's redo our first exercise and understand what we get new with the use of Celery.

## Install

Install Celery with:

<div class="termy">

    ```console
    $ python -m pip install celery
    ```

</div>
<br>

## Create App

Let's create a simple application to consume the messages. It will simply display the message on standard output.

!!! exercise "Question!"
    But first, let's configure Celery. To do this, create a `celeryconfig.py` file containing the broker information (RabbitMQ):

    ```python
    broker_url = "amqp://myuser:mypassword@localhost:5672//"
    task_serializer = "json"
    accept_content = ["json"]
    timezone = "UTC"
    enable_utc = True
    ```

    !!! danger "Update credentials!"
        Update `myuser` and `mypassword` to your RabbitMQ credentials!

!!! exercise "Question!"
    Then create a `my_ml_app.py` file containing:

    ```python
    from celery import Celery

    app = Celery("my_ml_app")

    # Load the Celery configuration from celeryconfig.py
    app.config_from_object("celeryconfig")


    @app.task
    def predict(payload):
        """Simulate a Prediction function"""
        print("Received:")
        print(payload)
        return
    ```

!!! info "Celery Task!"
    Notice that the `predict` function is annotated as a Celery **task**.
    
    This task should be called every time a prediction is needed.

## Run App

To initialize the application, use:

<div class="termy">

    ```console
    $ celery -A my_ml_app worker
    ```

</div>
<br>

!!! exercise "Question!"
    Initialize the application and check the queues created on the RabbitMQ dashboard.

## Send Message

To send messages for prediction (simulation), let's create a file and call the Celery prediction task.

!!! exercise "Question!"
    Then create a `use_ml_app.py` file containing:

    ```python
    from my_ml_app import predict

    while True:
        msg = input("Enter a message: ")
        if msg == "exit":
            break

        # Call Celery task
        payload = {"message": msg}
        result = predict.delay(payload)
    ```

    Notice that, for each message, a payload is sent to the prediction task.

!!! exercise "Question!"
    Run the `use_ml_app.py` and send several messages.
    
    Check if these messages are consumed by the worker that makes the prediction. For each message you should get an output on the terminal (standard output)!

    !!! danger "Important!"
        Make sure your Cellery application (that makes the prediction) is running!

## Celery Dashboard - Flower

Celery provides a Dashboard through which we can monitor the status of workers and the work queue. This functionality can be added by installing `Flower`:

<div class="termy">

    ```console
    $ python -m pip install flower
    ```

</div>
<br>

Install it, then initialize Flower with:

<div class="termy">

    ```console
    $ celery -A my_ml_app flower
    ```

</div>
<br>

Access **http://0.0.0.0:5555** and browse the available options in the menu.

![](flower_init.png)

## Horizontal Scaling

Let's check out the horizontal scaling functionality. To do this, we will change the prediction code to simulate a long task.

!!! exercise "Question!"
    Update the `my_ml_app.py` file to add a `sleep`:

    ```python
    from celery import Celery
    import time

    app = Celery("my_ml_app")

    # Load the Celery configuration from celeryconfig.py
    app.config_from_object("celeryconfig")


    @app.task
    def predict(payload):
        """Simulate a Slow Prediction function"""

        print("Received:")
        print(payload)

        # Simulate long task
        time.sleep(10)

        print("Ended processing:")
        print(payload)

        return
    ```

Let's initialize the application with a limit of up to 10 workers. If Celery identifies the need for more workers, they will be created automatically.

<div class="termy">

    ```console
    $ celery -A my_ml_app worker --autoscale=10,2
    ```

</div>
<br>

!!! exercise "Question!"
    Initialize the application with horizontal scaling.

!!! exercise "Question!"
    Send several messages to the prediction queue.
    
    Check the number of workers and messages waiting for prediction on the Flower Dashboard.

## Extra

!!! exercise "Question!"
    Try to create a `docker-compose.yml` file to run the entire application (RabbitMQ, Celery worker, Flower).

!!! exercise "Question!"
    The [**Celery Backend**](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html) is used to store the results of tasks.

    Configure a backend ([**redis**](https://redis.io/docs/latest/) or [**RabbitMQ**](https://www.rabbitmq.com/)) to save them for later retrieval.

    !!! info "Info!"
        In case of using **Redis** as a backend, you need to start a Redis **server** in Docker compose.

## References

- https://docs.celeryq.dev/en/stable/getting-started/index.html