from ..config import consumer
from .data_pipeline import handle_csv_billing_data


def poll_kafka_messages():
    """Function to continuously poll messages from Kafka."""
    while True:
        try:
            msg = consumer.poll(timeout=15.0)
            if msg is None:
                print("No message found.")
                continue 
            if msg.error():
                raise Exception(str(msg.error()))
            else:
                handle_csv_billing_data(msg.value().decode('utf-8'))
                print(f"Message consumed.: {msg.value().decode('utf-8')}")
        except Exception as e:
            print(f"Error consuming message: {str(e)}")