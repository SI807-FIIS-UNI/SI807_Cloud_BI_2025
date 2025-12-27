#!/bin/bash
# ====================================
# VIEW IAM POLICIES
# ====================================
# Muestra todas las políticas de IAM configuradas en el proyecto

gcloud projects get-iam-policy nettalco-data-478503 --flatten="bindings[].members" --format="table(bindings.members, bindings.role)"
