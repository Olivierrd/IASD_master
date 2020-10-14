/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package eu.dauphine;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import static org.apache.flink.core.fs.FileSystem.WriteMode.OVERWRITE;


/**
 * The goal of the project is to create a Flink application which will read from Kafka clicks and displays, detect some suspicious/fraudulent activities and output the suspicious IP or UID into a file.
 */
public class StreamingJob {

	public static void main(String[] args) throws Exception {

		// set up the streaming execution environment
		final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment().setParallelism(1);

		Properties properties = new Properties();
		properties.setProperty("bootstrap.servers", "localhost:9092");
		properties.setProperty("zookeeper.connect", "localhost:2181");
		properties.setProperty("group.id", "test");

		List<String> topics = new ArrayList<>();
		topics.add("clicks");
		topics.add("displays");

		//Transform a Kafka source of clicks and displays to a DataStream of Event (java object)
		DataStream<Event> events = env.addSource(new FlinkKafkaConsumer<>(topics, new DeserializationToEventSchema(), properties)).setParallelism(1);

		//Fraud detector of UID which clicks too often
		FraudDetectorUid detectorUid = new FraudDetectorUid();
		//Fraud detector of IP which clicks too often
		FraudDetectorIp detectorIp = new FraudDetectorIp();

		//Take as input the Event Stream (click or display) and return an Alert Stream of fraudulent UIDs
		DataStream<AlertUid> alertsUid = events
				.keyBy(Event::getUid)
				.process(detectorUid)
				.name("fraud-detector-uid")
				.setParallelism(1);

		//Take as input the Event Stream (click or display) and return an Alert Stream of fraudulent IPs
		DataStream<AlertIp> alertsIp = events
				.keyBy(Event::getIp)
				.process(detectorIp)
				.name("fraud-detector-ip")
				.setParallelism(1);

		alertsUid.print();
		alertsIp.print();

		alertsUid.writeAsText("./outputs/uid_alert.txt",OVERWRITE);
		alertsIp.writeAsText("./outputs/ip_alert.txt",OVERWRITE);
		events.writeAsText("./outputs/events.txt",OVERWRITE);
		// execute program
		env.execute("Flink Streaming Java API to detect fraudulent clicks in ads.");
	}
}
