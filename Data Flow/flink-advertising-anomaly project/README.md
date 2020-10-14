# Flink-advertising-anomaly

This project was written by Olivier Randavel and Louis Fontaine

The goal of this school project is to detect anomalies from advertising events (clicks & displays) from Criteo data, using a streaming flow from Kafka and creating a real-time alerting job with Flink.

This repository gathers our flink implementation under the `orlf` directory. 
We advise the reader to start with the python notebook named `Exploration&Results.ipynb`. This python notebook describes our method to identify the uids and ip to remove. Also, it shows that the Flink implementation is successful.

It is possible to clone this projet, then follow these steps to reproduce all experiments : 

1. To start the Kafka streaming flow, follow indications from this [git](https://github.com/Sabmit/paris-dauphine)
2. Import `docker-compose.yml` file from this [link](https://github.com/Sabmit/paris-dauphine/tree/master/docker/kafka-zk)
3. From your terminal, execute `docker-compose rm -f; docker-compose up` to start the streaming data of advertising events
4. Finally run `orlf/src/main/java/eu/dauphine/StreamingJob.java` 
5. Our results are availaible throught this directory `orlf/outputs/`. It shows all events and the fraudulent uids and ip.

This project was graded 17.5/20