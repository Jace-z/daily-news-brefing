# Daily News Briefing AI Agent 📰

An automated, serverless pipeline that aggregates global news, synthesizes key takeaways using Gemini 1.5 Flash, and delivers a concise daily brief directly to your inbox.

---

## ✨ Features

*   **Intelligent Summarization**: Leverages **Gemini 1.5 Flash** via Vertex AI for high-performance, cost-effective news synthesis.
*   **Serverless Architecture**: Fully managed execution using **Cloud Run Jobs**, ensuring zero idle costs.
*   **User Preferences**: Personalized news topics and delivery settings stored in **Cloud Firestore**.
*   **Reliable Delivery**: Integrated with **Resend/SendGrid** REST APIs to ensure high deliverability.
*   **Deduplication**: Tracks "last-sent" timestamps in Firestore to prevent redundant summaries.

---

## 🏗️ Infrastructure Design

*   **Trigger**: **Cloud Scheduler** – A managed cron service to trigger the workflow once daily.
*   **Compute**: **Cloud Run Jobs** – Executes containerized tasks that scale to zero and shut down immediately after completion.
*   **Intelligence**: **Gemini 1.5 Flash (Vertex AI)** – Provides a massive 1M+ token context window for deep summarization at a lightweight price point.
*   **Database**: **Cloud Firestore (Native Mode)** – Serverless NoSQL database for managing user profiles and state.
*   **Email Gateway**: **Resend / SendGrid** – REST API-based email delivery to bypass traditional SMTP restrictions.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Cloud Provider** | Google Cloud Platform (GCP) |
| **Runtime** | Python 3.11+ / Docker |
| **LLM** | Gemini 1.5 Flash (Vertex AI) |
| **Database** | Cloud Firestore |
| **Scheduler** | Cloud Scheduler |
| **Email** | Resend or SendGrid (REST API) |

---

## 🤖 Pipeline Architecture

1.  **Trigger**: Cloud Scheduler sends a request to start the Cloud Run Job.
2.  **Fetch**: The job retrieves user profiles and news preferences from Firestore.
3.  **Ingest**: Aggregates latest headlines and articles from configured RSS feeds and News APIs.
4.  **Analyze**: Gemini 1.5 Flash processes the aggregated content, deduplicates stories, and generates a personalized summary.
5.  **Store**: Updates Firestore with the "last-sent" timestamp and history.
6.  **Distribute**: Sends the final brief via Resend/SendGrid REST API.

---

## 🚀 Deployment

### 1. GCP Project Setup
```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
gcloud services enable run.googleapis.com cloudscheduler.googleapis.com aiplatform.googleapis.com firestore.googleapis.com
```

### 2. Environment Variables
Configure your secrets in GCP Secret Manager or via environment variables in the Cloud Run Job:
*   `PROJECT_ID`: Your GCP Project ID
*   `LOCATION`: GCP Region (e.g., `us-central1`)
*   `EMAIL_API_KEY`: API Key for Resend or SendGrid
*   `SENDER_EMAIL`: Verified sender address

### 3. Build and Deploy
```bash
# Build the container
gcloud builds submit --tag gcr.io/[PROJECT_ID]/daily-news-brief

# Create the Cloud Run Job
gcloud run jobs create daily-news-job --image gcr.io/[PROJECT_ID]/daily-news-brief

# Schedule it
gcloud scheduler jobs create http daily-news-trigger \
    --schedule="0 8 * * *" \
    --uri="https://[REGION]-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/[PROJECT_ID]/jobs/daily-news-job:run" \
    --http-method=POST \
    --oauth-service-account-email=[SERVICE_ACCOUNT_EMAIL]
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for new feature ideas or bug fixes.
