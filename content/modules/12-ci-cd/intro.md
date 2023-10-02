# Continuous Integration and Continuous Delivery

## Introduction

**CI/CD** is a short for **Continuous Integration** and **Continuous Delivery** (or **Deployment**) and represents a modern approach to agile software development. It encompasses a set of practices and tools aimed at releasing applications **more frequently** and **efficiently**, while maintaining high quality and **minimizing risks**.

![](ci-cd-flow-desktop.png)

!!! info "CI/CD"
    By embracing **CI/CD**, organizations can streamline their development processes, enabling **faster** and **more frequent** releases while ensuring stringent **quality control** measures.

## Continuous Integration

In modern software development, it is common to have multiple developers or data scientists working simultaneously on different features within the same ML application.

!!! exercise text long "Question"
    How do you think it would be if an organization has to consolidate all the branch's source code, with project modifications made by data scientists, in a single day?

    !!! answer "Answer"
        This, known as **merge day** or **consolidation day**, is a process that can be tedious, manual, and time-consuming, with a high chance of **conflicts** with changes made by colleagues at the same time.

With **Continuous Integration** (CI), the team regularly consolidates code changes back into a shared branch, often on a daily basis. The changes are consolidated and then **validated** through **automated** application builds. Multiple **automated tests**, typically including unit and integration tests, are performed to ensure that the changes do not introduce any issues or break the application.

## Continuous Delivery

Continuous Delivery builds on Continuous Integration by **automating the release process** for builds that pass validation. With Continuous Delivery, code changes can be released to production with the click of a button after passing automated tests.

Some key aspects of Continuous Delivery:

- **Automated** release process that can deploy code to production environments
- **Shortens** the release cycle and provides **faster feedback**
- Allows for more **incremental updates** rather than big bang releases
- Releases still **require manual approval** before going live


## Continuous Deployment

Continuous Deployment takes automation one step further than Continuous Delivery. With Continuous Deployment, validated code changes are **automatically released** to production without any manual intervention.

Key aspects of Continuous Deployment:

- **Fully automated** process from commit to production with no manual steps
- New changes are immediately tested and **deployed** if they pass
- Enables much **faster release** cycles
- Requires comprehensive **test automation** and **continuous monitoring**
- Well suited for **web services** and **cloud infrastructure**
- Not suitable for every application - depends on comfort level

!!! exercise text long "Question"
    Could you give an example of an ML project where continuous deployment is not suitable?

    !!! answer "Answer"
        Some projects in medical diagnosis and financial transactions, where safety and sensitive data risks, besides regulations, are a concern.

        Also, early research projects and unstable models with poor performance may need further intervention and experimentation before being ready for automation.

!!! tip "Tip!"
    We need less manual steps and more **automation**!

## Some tools

Some tools that could be used for CI/CD of Machine Learning (ML) projects:

- **Jenkins**: Jenkins is a widely used open-source automation server that can be configured to support ML workflows.

- **GitLab CI/CD**: GitLab provides built-in CI/CD capabilities that support ML workflows.

- **Github Actions**: Github Actions provides a flexible and customizable platform to automate your ML pipelines directly from your GitHub repositories.

We will work with Github Actions. Advance to the next section!