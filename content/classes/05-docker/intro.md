# Containerization

## Why?

Managing the versions of a model is much more than just saving its code into a version control system like Github. It is necessary to provide an exact description of the environment, such as:
    
- Python libraries used as well as their versions
- System dependencies that need to be installed


!!! info "Important!"
    Deploying ML models to production should automatically and reliably rebuild this environment on the target machine.

In addition, the target machine will typically run **multiple models** simultaneously, and two models
may have incompatible dependency versions. Finally, several models running on the same machine could **compete for resources**.

One model exhibiting anomalous behavior has the potential to negatively impact the function of various other models deployed in the same machine.

## Containers

Containerization technology is increasingly used to address these challenges. These tools bundle an application with all its configuration files, libraries, and related dependencies that are needed for it to run in different operating environments.

Unlike virtual machines which each run their own operating system, containers share a single operating system kernel. This allows multiple containers to efficiently utilize system resources on a common operating system, without duplicating operating system environments for each workload.

!!! tip "Important!"
    Containers provide a more optimized use of computational capacity in comparison to virtual machines.

Before delving into Containers, let's talk about [Amazon S3](s3.md), a resource that will be important to us for storage!

## References

- Introducing MLOps, Chapter 6.
- https://aws.amazon.com/pt/s3/
- S3 Image: https://d1.awsstatic.com/s3-pdp-redesign/product-page-diagram_Amazon-S3_HIW.cf4c2bd7aa02f1fe77be8aa120393993e08ac86d.png