# Lambda Quotas

In the last classes we saw how to create functions that run serverless, that is, we don't need to worry about the infrastructure needed to execute the functions.

Ideally, we would like to run any function, with any time and memory requirement on AWS Lambda. But there are limits.

!!! exercise long "Question"
    Do you know of any quotas that limit the execution of AWS lambda functions?

    !!! answer "Answer"
        You can see the quotas [Here](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)

Considering ML applications, it is common for them to use packages such as `sklearn`, `XGBoost`, `lightgbm`, `pandas`, etc. Since dependencies need to be packaged in ZIP, it is common to use hundreds of MiB or a few GiB.

!!! exercise short "Question"
    Note the "Deployment package (.zip file archive) size" topic. What is the file size limit for a ZIP we want to deploy?

    !!! answer "Answer"
        50 MB (zipped, for direct upload), 250 MB (unzipped), 3 MB (console editor).

!!! exercise short "Question"
    Is there any alternative that we have already seen in class to solve the problem?

    !!! answer "Answer"
        We could split the code into several layers, but notice that there is also limits for number of function layers.

        Take a look at **Container image code package size** [quota](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html). Well, it turns out that we can also deploy functions to AWS lambda using containers! As the limit in this case is 10GB, we are able to deploy packages with dependencies larger than the ZIP limit.

Advance to the next topic to continue exploring this topic.