# DVC Pipelines

As discussed in the CI-CD class, a **pipeline** represents a series of sequential steps. A pipeline is essentially a **Directed Acyclic Graph (DAG)**, ensuring that there are no cycles in its structure.

![](dag.png)

In *DVC*, each step (node of the DAG) in the pipeline is called **stage**. **Stages** are responsible for *processing data* and *executing code* to generate *outputs*, which can include machine learning models or other artifacts.

These *stages* are interconnected by defining *dependencies*, where the output of one stage becomes the input for another stage. By establishing this interdependence, a coherent pipeline is formed, allowing the flow of data and transformations from one stage to the next in a sequential manner.

