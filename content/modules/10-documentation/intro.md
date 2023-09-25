# Documentation

Today's topic is documentation! Before answering what documentation is and how to do it, let's think about some more basic ML questions.

## Why?!

!!! exercise text long "Question"
    In your opinion, what leads a company to invest in innovative technologies such as Machine Learning? What are companies’ expectations?

    !!! answer "Answer!"
        Some reasons, among others:

        - **Increase efficiency**: automate tasks using ML, freeing employees to focus on more strategic work.

        - **Gain competitive advantage**: early adopters tend to have advantages over competitor.

        - **Increase revenue**: be more precise in decision making, increasing revenue and profit.

        - **Improve public image**: the adoption of technologies can improve the market's view of the company, resulting in an improvement in share prices.

Each person in a company may have their own expectations. Let’s now think about the technical areas:

!!! exercise text long "Question"
    If you were a data scientist developing a model (think of any model). What would your expectations be?

Well, a data scientist could feel satisfaction in seeing a model giving financial results for the company. This could also result in a **bonus** or **job promotion**!

We know that many data science projects fail to bring results to companies. Although I agree that it is a valid thing to have a project that results in profit, this is not the only valid metric (money).

!!! exercise text long "Question"
    Think about your fictional colleagues who work with you on the data team. What would be their expectations regarding the projects you develop?

    !!! answer "Answer"
        If they need to act on the project, they hope to do so in the easiest way possible.

        As technical people, they can expect, for example, **well-written code** and some **support material** so they understand what the project does.

Besides everything, everyone expects you to be able to do ML **faster** and faster! Truly committed companies have already realized that it isn’t just about going fast right now but about going **sustainably fast in the long run**.

!!! info "Important!"
    It's not just about you, think about the team and in the long run!

## Documentation

For application of ML methods, a data scientist should be able to consult software documentation to comprehend how to utilize a product such as an API in **LightGBM** or **TensorFlow**.

!!! exercise text long "Question"
    How would you define Sofware Documentation in general?

    !!! answer "Answer"
        Documentation is meant to **guide users** about **software functionality**. It is any artifact which its purpose is to communicate information about the software system to which it belongs, to individuals involved in the production of that software.

So, at this point we are already familiar with **using** documentation! Isn't it cool when our knowledge about a library is close to zero and in a matter of minutes we can consult the documentation and obtain the necessary knowledge?

!!! exercise text long "Question"
    What about **writing** documentation? Have you ever had to document a project? Do you usually document everything you develop?

It is common for us to have an extremely technical orientation, focusing on developing code and avoiding tasks such as documentation.

Many **hate** and **postpone** documentation activities! Even the professor didn't like much preparing this lesson (just kidding!)

!!! danger "Danger!"
    Most software engineers and data scientists tend to **prefer writing code** and **leave behind** other tasks like **testing**, **documentation**.

!!! exercise text long "Question"
    Think and describe some problems arising from having no documentation.

    !!! answer "Answer"
        Someone will pay the price! It is common to have to maintain models or APIs developed months ago. Good documentation ensures efficiency in this process.
        
        Furthermore, it is common for turnover to occur in data teams. Good documentation also ensures that the software is more about the **company** and less about the **scientists** (an ongoing project, where many people can act).

## Audience Factor

Consider your audience when making documentation decisions. Identify if they are **internal** or **external** to your organization and their level of knowledge about the product and domain.

Tailor your documentation accordingly: for less knowledgeable customers, provide tutorial-focused content, diagrams, and glossary to introduce concepts. For experienced customers, focus on examples and scenarios to enhance their usage and value from the product.

## Documentation Storage

!!! tip "Tip!"
    The best place to store documentation is on the documented thing itself.

Both the Google datacenters and the Centre Pompidou in Paris share a distinctive feature: an abundance of color-coded pipes. These pipes are adorned with printed or riveted labels for easy identification. At the Pompidou Center, for example, blue pipes signify air circulation, while green pipes represent water systems.

![](where_documentation.png)

This is an example of documentation on the pipe itself. Another option would be to have a document that describes, using codes, the usefulness of each pipe.

!!! info "Persistent documentation"
    Persistent documentation can be categorized into two types: **external** and **internal**.

**External documentation** involves expressing knowledge in a format that is independent of the specific implementation technologies employed in a project. This encompasses traditional documentation methods, such as separate **Microsoft Office** documents.

One advantage of external documentation is its **flexibility**, as it allows for the use of various formats and tools that best suit the needs of both the audience and the writers.

!!! tip "Tip!"
    Remember, managers are not programmers!

However, a drawback of external documentation is the challenge, and sometimes impossibility, of **keeping it up-to-date** with the latest version of the product. Additionally, external documentation runs the risk of being lost or misplaced over time.

In the next sections, we will discuss how to document ML products efficiently.