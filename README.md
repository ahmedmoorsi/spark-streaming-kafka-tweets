# spark-streaming-kafka-tweets


### video [here](https://vimeo.com/754404997)


1 -- Zookeeper

starting a Zookeeper instance.

```bash
~$ cd kafka/
~/kafka$ bin/zookeeper-server-start.sh config/zookeeper.properties
```


2 -- Kafka Broker

Now we need to start the Kafka broker.

```bash
~$ cd kafka/
~/kafka$ bin/kafka-server-start.sh config/server.properties
```

3 -- Kafka Config

Creating topics that hold all the tweets 


```bash
~/kafka$ bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Create a new topic named `tweets`

```bash
~/kafka$ bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets
```

Starting the Hadoop cluster.

~$ hdfs namenode -format
~$ start-dfs.sh 

4 -- Hive Metastore
~$ hive --service metastore

* ### Terminal 5 -- Hive


```bash
~$ hive

 ...

hive> use default;
hive> select count(*) from tweets;
```

* ### Terminal 6 -- Stream Producer

```bash
~$ ./tweet_stream.py
```

* ### Terminal 7 -- Stream Consumer + Spark Transformer

```bash
~$ spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar transformer.py
```


