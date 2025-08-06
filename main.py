import base64
import json
from google.cloud import bigquery

# Define expected sensor ranges (adjust based on your use case)
EXPECTED_RANGES = {
    "temperature": (-20, 50),
    "humidity": (0, 100),
    "soil_moisture": (0, 100)
}

def is_anomalous(data):
    anomalies = {}
    for key, (low, high) in EXPECTED_RANGES.items():
        if key in data:
            value = data[key]
            if not (low <= value <= high):
                anomalies[key] = value
    return anomalies

def process_pubsub(event, context):
    if 'data' not in event:
        print("No data found in event.")
        return

    try:
        data_str = base64.b64decode(event['data']).decode('utf-8')
        print(f"Raw message: {data_str}")
        data = json.loads(data_str)
        print(f"Parsed JSON: {data}")

        anomalies = is_anomalous(data)
        if anomalies:
            print(f" Anomalies detected: {anomalies}")
            # Optional: trigger alert (e.g., send email/webhook/log)
        else:
            print("Data passed validation.")

        client = bigquery.Client()
        table_id = "real-time-pipeline-467013.iot_data.sensor_readings"
        rows_to_insert = [data]
        errors = client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print("Insert errors:", errors)
        else:
            print("Row inserted:", data)

    except json.JSONDecodeError:
        print("❌ Message is not valid JSON. Skipping.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
