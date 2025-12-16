#!/bin/bash
set -e

# Configurar proyecto y crear bucket

gcloud config set project us-accidents-481401

gsutil mb -p us-accidents-481401 -l us-central1 gs://us-accidents-bd
