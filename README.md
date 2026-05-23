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
