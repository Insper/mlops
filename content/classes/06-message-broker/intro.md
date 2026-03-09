# Message Broker

## Introduction

An ML application will usually be made up of several interconnected parts. We have already seen in previous classes how to create an API, so applications that need prediction by an ML model can access a specific route.

We have also seen that a model can read data and write prediction results to a DBMS (database management system).

## Message Broker

Today we will see how to work with **message brokers**. A message broker is a middleware software component that allows applications to exchange messages asynchronously. It acts as an intermediary to route messages between publishers and subscribers.

Think, for example, of an ML model that analyzes a store's delivery data for complaint prevention.

![](example_delivery.png)

Suppose that, for some deliveries, he recommends sending a message explaining the situation (reason for the delay). This sending (Telegram, Email, WhatsApp) will not be done by the ML model and will require calling an extra application.

An alternative is to add the model's predict result to a queue, so that the sending application (Telegram, Email, WhatsApp) handles the messages according to their availability. The application responsible for managing this queue is the **message broker**.

!!! exercise short "Question"
    Could the message broker be used to create a queue of JSON from customers for a model to process? For example:
    ```JSON
    {
        "age": 42,
        "job": "entrepreneur",
        "marital": "married",
        "education": "primary",
        "balance": 558,
        "housing": "yes",
        "duration": 186,
        "campaign": 2
    }
    ```
    !!! answer "Answer"
        Yes! In general, the message broker does not care about the actual message content or format. Messages can contain serialized objects, JSON strings, binary files - essentially any type of content that can be serialized into a byte stream.

## Advantages

The main advantages of using message brokers are:

- **<span style="color: green;">Asynchronous communication</span>**: messages can be sent and received asynchronously. This allows work to be queued when systems are **overloaded** and prevents failures from stopping the flow of work.

- **<span style="color: green;">Decoupling of services/applications</span>**: a message broker allows different parts of a distributed system to communicate **without the need of direct knowledge** of each other.

- **<span style="color: green;">Scalability</span>**: more **consumers/producers can be added easily** without modifying code as load increases.

- **<span style="color: green;">Reliability</span>**: message brokers guarantee at-least-once delivery of messages, so **messages aren't lost if a receiver fails**.

- **<span style="color: green;">Durability</span>**: messages can **survive recipient or broker failures** through persistent storage and retries.

- **<span style="color: green;">Location transparency</span>**: services remain **agnostic to location or availability** of other services using the broker.

- **<span style="color: green;">Manageability</span>**: brokers provide **centralized tools for administration**, monitoring and management of messaging infrastructure.

## Alternatives

There are several message broker that we could use, such as:

- RabbitMQ
- Apache Kafka
- Azure Service Bus
- AWS SQS/SNS

In this class, we will work with RabbitMQ.
