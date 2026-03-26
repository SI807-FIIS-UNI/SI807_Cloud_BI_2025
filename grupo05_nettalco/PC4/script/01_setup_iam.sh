#!/bin/bash
# ====================================
# SETUP IAM - Configuración de Roles
# ====================================
# Configura los roles granulares de IAM para usuarios y service accounts
# en el proyecto nettalco-data-478503 de Google Cloud Platform

PROJECT_ID="nettalco-data-478503"

# Usuarios con rol Owner
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:francisco.grijalva.p@uni.pe" --role="roles/owner"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:daniel.otero.v@uni.pe" --role="roles/owner"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:r.loayza.s@uni.pe" --role="roles/owner"

# Jefe de practicas con rol viewer
gcloud projects add-iam-policy-binding $PROJECT_ID  --member="user:fegarciaa@uni.pe" --role="roles/viewer"

# Service Accounts con roles de Dataproc
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:nettalco-cf-sa@nettalco-data-478503.iam.gserviceaccount.com" --role="roles/dataproc.editor"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:nettalco-cf-sa@nettalco-data-478503.iam.gserviceaccount.com" --role="roles/dataproc.viewer"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:nettalco-cf-sa@nettalco-data-478503.iam.gserviceaccount.com" --role="roles/dataproc.worker"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:467475048380-compute@developer.gserviceaccount.com" --role="roles/dataproc.worker"

# Service Accounts con roles Storage
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:467475048380-compute@developer.gserviceaccount.com" --role="roles/storage.objectCreator"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:467475048380-compute@developer.gserviceaccount.com" --role="roles/storage.objectViewer"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:nettalco-cf-sa@nettalco-data-478503.iam.gserviceaccount.com" --role="roles/storage.objectViewer"

# Service Accounts de Cloud Build
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:467475048380@cloudbuild.gserviceaccount.com" --role="roles/cloudbuild.builds.builder"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-cloudbuild.iam.gserviceaccount.com" --role="roles/cloudbuild.serviceAgent"

# Service Accounts de Cloud Functions
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcf-admin-robot.iam.gserviceaccount.com" --role="roles/cloudfunctions.serviceAgent"

# Service Accounts de Cloud Scheduler
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-cloudscheduler.iam.gserviceaccount.com" --role="roles/cloudscheduler.serviceAgent"

# Service Accounts de AI Platform
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-aiplatform.iam.gserviceaccount.com" --role="roles/aiplatform.serviceAgent"

# Service Accounts de Artifact Registry
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-artifactregistry.iam.gserviceaccount.com" --role="roles/artifactregistry.serviceAgent"

# Service Accounts de BigQuery Data Transfer
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com" --role="roles/bigquerydatatransfer.serviceAgent"

# Service Accounts de Cloud AI Companion
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-cloudaicompanion.iam.gserviceaccount.com" --role="roles/cloudaicompanion.serviceAgent"

# Service Accounts de Compute
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@compute-system.iam.gserviceaccount.com" --role="roles/compute.serviceAgent"

# Service Accounts de GKE / Container
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@container-engine-robot.iam.gserviceaccount.com" --role="roles/container.serviceAgent"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@containerregistry.iam.gserviceaccount.com" --role="roles/containerregistry.ServiceAgent"

# Service Accounts de Eventarc
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-eventarc.iam.gserviceaccount.com" --role="roles/eventarc.serviceAgent"

# Service Accounts de Pub/Sub
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@gcp-sa-pubsub.iam.gserviceaccount.com" --role="roles/pubsub.serviceAgent"

# Service Accounts de Cloud Run / Serverless
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:service-467475048380@serverless-robot-prod.iam.gserviceaccount.com" --role="roles/run.serviceAgent"

# Service Accounts con acceso a Logging y Secret Manager
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:nettalco-cf-sa@nettalco-data-478503.iam.gserviceaccount.com" --role="roles/logging.logWriter"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:nettalco-cf-sa@nettalco-data-478503.iam.gserviceaccount.com" --role="roles/secretmanager.secretAccessor"
