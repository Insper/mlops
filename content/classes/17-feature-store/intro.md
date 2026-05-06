# Introduction

Suppose you were hired as a data scientist by a company that doesn't do ML at all. In order for a model to be built, one of the first activities would involve carrying out **data engineering** to have data available for the models to consume.

As the iterations of adding new data and building new features took place, we hope that the model's performance will increase to an acceptable value and a new ML product will be born in the company!

After starting the development of a new project in the company, a likely feeling is that part of the features developed could be reused.

For example, the average purchase ticket, total sales, place of residence of a customer, profession, etc. These are examples of useful features for different models (credit, complaints, churn, etc.).

In software development, we talk a lot about **reuse**.

!!! exercise text long "Question!"
    Explain, in your own words, what **code reuse** is.

    !!! answer "Answer!"
        It is the use of **existing software**, or software knowledge, to **build new software**. It involves creating software components in a modular and reusable manner so that they can be easily incorporated into different projects without the need to reinvent or rebuild the same functionality. Reuse can lead to **faster development** cycles and **reduced costs**.

With the use version control and code Organization, among other, code reuse is facilitated and can also occur in ML projects. After all, ML projects also involve a lot of programming.

However, data is an important part in the development of ML projects. The efficient management and governance of data play a crucial role in ensuring project success.

!!! exercise text long "Question!"
    How can we guarantee the reuse and availability of features in ML projects?

Today we will explore **feature stores**. A **feature store** acts as a centralized repository for storing, managing, and serving ML **data features**, providing a unified and reliable source of data for model development and deployment.

!!! info "Info!"
    Features refer to data attributes or variables that are used as inputs to train and make predictions

The solution we will explore will be **Feast**: a standalone, open-source feature store that organizations use to store and serve features consistently for offline training and online inference.

Go to the next topic!