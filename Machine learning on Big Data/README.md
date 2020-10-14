# Machine learning on Big Data

## Course

![Alt text](criteo_lab.PNG?raw=true "Title")

This course taught by Criteo, focuses on the typical, fundamental aspects that need to be dealt with in the design of machine learning 
algorithms that can be executed in a distributed fashion, typically on Hadoop clusters, in order to deal with big data 
sets, by taking into account scalability and robustness. Nowadays there is an ever increasing demand of machine learning
algorithms that scales over massives data sets.
In this context, this course focuses on the typical, fundamental aspects that need to be dealt with in the design of 
machine learning algorithms that can be executed in a distributed fashion, typically on Hadoop clusters, in order to 
deal with big data sets, by taking into account scalability and robustness. So the course will first focus on a bunch of
main-stream, sequential machine learning algorithms, by taking then into account the following crucial and complex 
aspects. The first one is the re-design of algorithms by relying on programming paradigms for distribution and 
parallelism based on map-reduce (e.g., Spark, Flink, ….). The second aspect is experimental analysis of the map-reduce 
based implementation of designed algorithms in order to test their scalability and precision. The third aspect concerns
the study and application of optimisation techniques in order to overcome lack of scalability and to improve execution 
time of designed algorithm.

The attention will be on machine learning technique for dimension reduction, clustering and classification, whose 
underlying implementation techniques are transversal and find application in a wide range of several other machine 
learning algorithms. For some of the studied algorithms, the course will present techniques for a from-scratch 
map-reduce implementation, while for other algorithms packages like Spark ML will be used and end-to-end pipelines will 
be designed. In both cases algorithms will be analysed and optimised on real life data sets, by relaying on a local 
Hadoop cluster, as well as on a cluster on the Amazon WS cloud.

## Project

The evaluation of the course focused on the presentation of a research article : 
[Network–Efficient Distributed Word2vec Training System for Large Vocabularies](https://arxiv.org/abs/1606.08495)

This project has been done with the collaboration of [Maxime Talarmain](https://www.linkedin.com/in/maxime-talarmain-58aa99165).
In this folder you will find the studied paper and the presentation made to present our understanding. This work was 
graded 17/20.