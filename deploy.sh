#!/bin/bash

gcloud functions deploy process_pubsub \
  --gen2 \
  --runtime python310 \
  --trigger-topic sensor-data \
  --entry-point process_pubsub \
  --region us-central1 \
  --set-env-vars GOOGLE_PROJECT=$(gcloud config get-value project) \
  --memory=256MB \
  --timeout=60s \
  --source=.
