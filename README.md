# CTI Automation - Deep Research Pipeline

An automated, serverless pipeline designed to conduct comprehensive Cyber Threat Intelligence (CTI) research using the Google GenAI SDK (Interactions API). This system autonomously synthesizes monthly reports focusing on threat actors, TTP evolution, and systemic risks targeting the Banking, Financial Services, and Fintech sectors.

## Architecture

This project is fully deployed on Google Cloud Platform (GCP) to ensure autonomous, zero-maintenance execution.

* **Google Cloud Functions (Gen 2):** Provides the scalable, serverless Python 3.12 runtime. Configured with an extended timeout (3600s) to accommodate long-running agentic research.
* **Google Cloud Scheduler:** Triggers the pipeline automatically on the first day of every month at 02:00 AM (Europe/Lisbon).
* **Google Secret Manager:** Securely stores and injects the Gemini API key into the runtime environment.
* **Google GenAI SDK:** Utilizes the experimental Interactions API to spawn the `deep-research-preview` agent for asynchronous web intelligence gathering.

## Repository Structure

* `main.py` - The entry point for the Cloud Function (Functions Framework HTTP wrapper). Contains the deterministic prompt engineering, threshold mandates, and polling logic.
* `requirements.txt` - Python dependencies (`functions-framework`, `google-genai`).
* `.gcloudignore` - Deployment optimization file to exclude local virtual environments (`venv/`) and cache directories from the cloud build process.

## Prerequisites

* Google Cloud Platform account with active billing.
* Google Cloud CLI (`gcloud`) installed and authenticated locally.
* A valid Gemini API Key with access to the Deep Research agent.

## Deployment Guide

Run the following commands via the Google Cloud CLI to provision the infrastructure from scratch.

### 1. Enable Required Cloud APIs
```bash
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com cloudscheduler.googleapis.com secretmanager.googleapis.com run.googleapis.com

````
2. Secure the API Key
Create a secret container and inject your API key:

Bash
gcloud secrets create cti_api_key --replication-policy="automatic"
echo -n "YOUR_API_KEY_HERE" | gcloud secrets versions add cti_api_key --data-file=-


3. Configure IAM Permissions
Grant the default compute service account permission to build containers and access the Secret Manager:

Bash
# Substitute YOUR_PROJECT_ID and YOUR_PROJECT_NUMBER below
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role="roles/secretmanager.secretAccessor"
4. Deploy the Cloud Function
Navigate to the root directory containing main.py and deploy the Gen 2 function:

Bash
gcloud functions deploy cti-deep-research \
  --gen2 \
  --runtime=python312 \
  --region=europe-west1 \
  --source=. \
  --entry-point=run_cti_research \
  --trigger-http \
  --timeout=3600 \
  --set-secrets="GEMINI_API_KEY=cti_api_key:latest"
5. Schedule the Automation
Configure Cloud Scheduler to trigger the function monthly:

Bash
gcloud scheduler jobs create http trigger-cti-research \
  --schedule="0 2 1 * *" \
  --time-zone="Europe/Lisbon" \
  --uri="YOUR_CLOUD_FUNCTION_TRIGGER_URL" \
  --http-method=GET \
  --location="europe-west1"
