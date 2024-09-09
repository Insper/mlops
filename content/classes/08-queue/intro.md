# Introduction

## Quotas

In the last classes, we saw how to use [**Lambda**](../07-lambda/aws_lambda.md) to deploy ML applications without worrying so much about the server infrastructure needed for execution.

Furthermore, we saw how to use [**Layers**](../07-lambda/lambda_layer.md) and [**Docker**](../07-lambda/lambda_and_docker.md)  images to maintain a good organization of the project and its dependencies, bypassing file size [**limits**](../07-lambda/lambda_quotas.md) established when creating functions in AWS Lambda.

!!! tip "Tip!"
    You can see AWS Lambda default quotas [**Here**](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html).

!!! info "Important!"
    Using Docker with AWS Lambda offers several benefits beyond overcoming ZIP size limitations.

    Docker allows you to package not only your code but also the entire runtime environment, including *dependencies* and *system configurations*, into a *consistent* and *portable* container.

## Concurrent Executions

!!! exercise text long "Question"
    In computer science, what is **concurrency**?

    !!! answer "Answer!"
        [Concurrency](https://en.wikipedia.org/wiki/Concurrency_(computer_science)) is the ability of different parts or units of a program, algorithm, or problem to be executed out-of-order or in partial order, **without affecting the outcome**. This allows for **parallel execution** of the concurrent units, which can significantly **improve overall speed **of the execution in multi-processor and multi-core systems.

!!! exercise text long "Question"
    In the context of an AWS Lambda function, what is **concurrency**?

    !!! answer "Answer!"
        In AWS Lambda, [**Concurrency**](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html) is the number of in-flight requests your AWS Lambda function is handling at the same time.


!!! exercise short long "Question"
    Is there a limit on simultaneous execution of lambda functions?

    !!! answer "Answer!"
        Yes, check it [**Here**](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html). It can be increased up.

!!! exercise short long "Question"
    What happens if there are too many calls to a lambda function, so that the concurrency limit is reached?

    !!! answer "Answer!"
        Let's test it and find out!

