# Sentiment Analysis

## Remembering

[In AWS lamda class page](aws_lambda.md) we saw how to build [**Lambda functions**](aws_lambda.md#aws-lambda_1) in AWS.

We chose the [**API Gateway**](api_gateway.md) service to expose our Lambda functions. Thus, the function is triggered whenever the user makes a request to an endpoint.

![](api_gateway_lambda.png)

!!! info "Info!"
    AWS Lambda allows machine learning models to be deployed and hosted serverlessly.

Looking back at the examples we did, they involved a [*function that returned a fixed JSON*](lambda_practicing.md#create-function) and a lambda function that [*counted the number of words in a sentence*](api_gateway.md#practicing). No ML for now!

Let's use this class to build more complex examples using AWS Lambda!

<!-- !!! progress "Click to continue" -->

## Sentiment Analysis

Sentiment analysis (**SA**) is the process of determining whether a given phrase is positive, negative or neutral.

It can be applied to analyze feedback, reviews, survey responses, social media posts and more to gauge public opinion on certain topics.

!!! exercise long "Question"
    How can we represent the **sentiment** of a text as a **variable** in a database?

    !!! answer "Answer!"
        We can represent it as a **continuous score**, for example, in the range `[-1,1]``, where `-1.0` represents a very negative text and `1.0` represents a very positive text.

        Another option is to use **categorical variables**, such as:

        - Very negative
        - Negative
        - Neutral
        - Positive
        - Very positive

!!! exercise long "Question"
    Is it possible to predict the sentiment of a sentence without using ML algorithms? Can you think of any way?

    !!! answer "Answer!"

        One of the simplest ways is to create fixed rules. For example, count how many times a word like `disappointed` occurs in text. A high occurrence may indicate negativity!

        Another way is to create two lists of words: one of *negative* words and another of *positive* words. We count how many words we have from each list in the sentence we are analyzing, and if we have more positive words, we say the text has positive sentiment, otherwise we say it has negative sentiment.

        Furthermore, we can ask an expert to provide weights for words, for example, `hate` could have a weight of `-0.9` while `cool` could have a weight of `0.4`. Thus, we can compute whether in total we have a predominant positive or negative weight.

        [See more Here](https://neptune.ai/blog/sentiment-analysis-python-textblob-vs-vader-vs-flair#:~:text=methods%20and%20packages.-,Rule%2Dbased%20sentiment%20analysis,-Rule%2Dbased%20sentiment)

!!! exercise long "Question"
    Have you trained or have any idea how to train an ML model for sentiment analysis? Explain how.

    !!! answer "Answer!"

        Considering a manually classified database, we can pre-process the text, removing punctuations and stop-words. Then we can tokenize the text and train a Naive Bayes classifier. You probably did this in Ciência dos dados (you created the Python code to calculate probabilities yourself) and Megadados (using Spark) courses.
        
        See more [Here](https://scikit-learn.org/stable/modules/naive_bayes.html) and [Here](https://en.wikipedia.org/wiki/Naive_Bayes_classifier).

Instead of training our own sentiment analysis model, we will use a ready-made library that already provides this functionality.

## Textblob library

We chose to use the `textblob` library for sentiment analysis. It provides a series of features such as:

- Calculation of n-grams.
- Tokenization
- Spelling Correction
- Sentiment Analysis
- etc.

See the documentation [here](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis) and [here](https://textblob.readthedocs.io/en/dev/api_reference.html#textblob.blob.TextBlob.sentiment).

Let's see an example of how to use the library. But first, do the installation:

<div class="termy">

    ```console
    $ pip install textblob
    ```

</div>

<br>
Let's use `textblob` to obtain the *polarity* of three different texts:

```python
from textblob import TextBlob

text1 = "What a damn company. You guys are the worst, you can't meet the deadline."
text2 = "Hello everybody"
text3 = "I am so happy to be here"

blob1 = TextBlob(text1)
blob2 = TextBlob(text2)
blob3 = TextBlob(text3)

print(f"Polarity of text1: {blob1.polarity}")
print(f"Polarity of text2: {blob2.polarity}")
print(f"Polarity of text3: {blob3.polarity}")

```

!!! tip "Tip!"
    Here it is the repository of textblob: https://github.com/sloria/textblob

!!! exercise "Question"
    Run this code locally and test it with other sentences. Then proceed to the next topic.