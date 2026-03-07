# Findings & Research

## Architecture
- **Trigger**: Cloud Scheduler (Cron)
- **Compute**: Cloud Run Jobs (Serverless execution)
- **LLM**: Gemini 1.5 Flash (Vertex AI)
- **DB**: Cloud Firestore (User state)
- **Email**: Resend/SendGrid (REST API)

## GCP Configuration
### Firestore Schema
- **Collection**: `users`
  - `email`: string
  - `interests`: list[string]
  - `rss_feeds`: list[string]
  - `last_sent`: timestamp (managed by the app)
  - `created_at`: timestamp

### Secret Manager
- `NEWS_API_KEY`: NewsAPI.org API Key
- `EMAIL_API_KEY`: Resend or SendGrid API Key

## GCP Deployment Guide

### 1. Enable APIs
```bash
gcloud services enable \
    artifactregistry.googleapis.com \
    run.googleapis.com \
    aiplatform.googleapis.com \
    secretmanager.googleapis.com \
    firestore.googleapis.com \
    cloudscheduler.googleapis.com
```

### 2. Setup Artifact Registry
```bash
# Create a repository
gcloud artifacts repositories create news-brief-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository for News Briefing Agent"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 3. Build and Push Image
```bash
# Define variables
PROJECT_ID=$(gcloud config get-value project)
IMAGE_NAME=us-central1-docker.pkg.dev/$PROJECT_ID/news-brief-repo/news-agent:latest

# Build and push
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME
```

### 4. Create Cloud Run Job
```bash
gcloud run jobs create daily-news-job \
    --image $IMAGE_NAME \
    --region us-central1 \
    --set-env-vars="PROJECT_ID=$PROJECT_ID,LOCATION=us-central1,EMAIL_PROVIDER=resend,SENDER_EMAIL=your-verified-email@example.com,USE_SECRET_MANAGER=true" \
    --service-account=[SERVICE_ACCOUNT_EMAIL]
```

### 5. IAM Permissions
Ensure the runtime Service Account has:
- `roles/aiplatform.user`
- `roles/datastore.user` (for Firestore)
- `roles/secretmanager.secretAccessor`

### 6. Schedule Job
```bash
gcloud scheduler jobs create http daily-news-trigger \
    --location=us-central1 \
    --schedule="0 8 * * *" \
    --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/daily-news-job:run" \
    --http-method=POST \
    --oauth-service-account-email=[SERVICE_ACCOUNT_EMAIL]
```

## Local Development
1. Copy `.env.example` to `.env`.
2. Fill in the required variables.
3. Run `pip install -r requirements.txt`.
4. Run `python src/main.py`.


