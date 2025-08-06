from google.cloud import pubsub_v1
import json
import time

project_id = "real-time-pipeline-467013"
topic_id = "sensor-data" 

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_sample_data():
    message = {
        "temperature": 23,
        "humidity": 55,
        "soil_moisture": 48
    }
    data_str = json.dumps(message)
    data = data_str.encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(f"Published message: {data_str}")
    future.result()

if __name__ == "__main__":
    publish_sample_data()
