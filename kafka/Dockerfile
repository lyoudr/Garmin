# Base image
FROM ubuntu:22.04

# Install required packages (including wget, tar, and Java)
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Dynamically set JAVA_HOME using update-alternatives
RUN export JAVA_HOME=$(update-alternatives --list java | grep 'java-11' | sed 's|/bin/java||') && \
    echo "JAVA_HOME is set to $JAVA_HOME" && \
    export PATH="$JAVA_HOME/bin:$PATH"

# Set the working directory
WORKDIR /kafka

# Download Kafka
RUN wget https://dlcdn.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz

# Extract the Kafka tarball
RUN tar -xzf kafka_2.13-3.8.0.tgz

# Set working directory to Kafka extracted folder
WORKDIR /kafka/kafka_2.13-3.8.0

# Generate Kafka Cluster ID and format log directories
RUN bash -c "export KAFKA_CLUSTER_ID=\$(bin/kafka-storage.sh random-uuid) && \
    bin/kafka-storage.sh format -t \$KAFKA_CLUSTER_ID -c config/kraft/server.properties"

# Install Node Exporter
RUN wget https://github.com/prometheus/node_exporter/releases/latest/download/node_exporter-1.6.0.linux-amd64.tar.gz && \
    tar -xzf node_exporter-1.6.0.linux-amd64.tar.gz && \
    mv node_exporter-1.6.0.linux-amd64/node_exporter /usr/local/bin/ && \
    rm -rf node_exporter-1.6.0.linux-amd64*

# Expose Kafka port (default is 9092)
EXPOSE 9092 9100

# Start Kafka and Node Exporter
CMD ["bash", "-c", "node_exporter & bin/kafka-server-start.sh config/kraft/server.properties"]