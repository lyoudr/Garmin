# Billing Service

## Project Overview

In my project flow, the producer service continuously sends billing file paths (raw data) to a Kafka topic, while the consumer service subscribes to this topic. Upon receiving a message, the consumer service continously executes an Apache Beam data pipeline that implements a map-reduce pattern, processing the data and writing the results to a Cassandra database. It is a streaming event processing system. Additionally, I utilize Prometheus to collect metrics from the containers, enabling me to monitor request volumes, CPU usage, and memory utilization effectively.

## Tools Used
- **Apache Kafka**: For message streaming.
- **Cassandra**: As the database for storing billing data.
- **Node Exporter**: To expose system-level metrics from each service for Prometheus to scrape.
- **Prometheus**: For monitoring and scraping metrics from the services.
- **FastAPI**: For Building Producer service and Consumer service backend.
- **Apache Beam**: Implement Map Reduce, and run data pipeline.

## Project Diagram
![link](https://github.com/lyoudr/Garmin/blob/main/structure.png)


## Data Pipeline principle
### Map Reduce

- Map Phase
    - `Map(k1,v1) → list(k2,v2)`
    ```
      beam.Map(lambda billing: (billing.company, billing.cost))  
    ```
- Shuffle and Sort Phase 
    - The intermediate key-value pairs generated by the mappers are shuffled and sorted based on the keys
- Reduce Phase
    - `Reduce(k2, list (v2)) → list((k3, v3))`
    ```
        beam.CombinePerKey(sum)
    ```

## Project Structure

```bash
├── docker-compose.yml        # Docker Compose configuration for the project
├── consumer/                 # Consumer service folder
│   └── app...                # Consumer application code
├── producer/                 # Producer service folder
│   └── app...                # Producer application code
├── kafka/                    # Kafka-related files
│   └── Dockerfile            # Dockerfile for Kafka setup
├── prometheus/               # Prometheus configuration folder
│   └── prometheus.yml        # Prometheus configuration file
└── README.md                 # Project README file         
```

## Start Project
#### 1. Clone the project
```
git clone https://github.com/lyoudr/Garmin.git
cd Garmin
```
#### 2. Start the service
```
docker-compose up --build
```
#### 3. Activate consumer service to subscribe to the topic
[swagger docs](http://localhost:8081/docs)

API endpoint: http://localhost:8081/consume


#### 4. Produce event to Kafka topic
[swagger docs](http://localhost:8000/docs)

API endpoint: http://localhost:8000/produce


Upon receiving the event, the producer triggers the data pipeline to process the billing_report.csv file and writes the results to the database.

payload
```
{
    "topic": "test-topic",
    "msg": "/workspace/app/statics/billing_report_1.csv" # or "/workspace/app/statics/billing_report_2.csv"
}
```

#### 5. To make sure data has been written to the database 
Enter to cassandra container
```
docker exec -it cassandra bash
```
Enter to cassandra terminal
```
cqlsh
```
Use `ann` keyspace
```
USE ann;
```
Select data from table `billing_report`
```
SELECT * FROM billing_report;
```

## Metrics

### To monitor the metrics of each service, please visit 
[http://localhost:9090](http://localhost:9090)

#### 1. monitor producer service
enter
`up{job="producer"}` to the search bar.
And the result series will be 1, which means the service is being detected.

#### 2. monitor producer service
enter
`up{job="consumer"}` to the search bar.
And the result series will be 1, which means the service is being detected.

#### 3. monitor producer service
enter
`up{job="kafka"}` to the search bar.
And the result series will be 1, which means the service is being detected.
