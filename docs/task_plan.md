# Task Plan: Daily News Briefing AI Agent

## Project Overview
An automated news aggregation and summarization service using Gemini 1.5 Flash and GCP.

## Phases

### Phase 1: Environment Setup & Infrastructure (Current)
- [ ] Enable GCP APIs (Artifact Registry, Cloud Run, Vertex AI, Secret Manager, Firestore).
- [ ] Create Artifact Registry repository.
- [ ] Create Firestore Database (Native mode).
- [ ] Create Secrets in Secret Manager (`NEWS_API_KEY`, `EMAIL_API_KEY`).

### Phase 2: Core Logic Development
- [x] Implement News Fetcher (RSS/News API).
- [x] Implement Gemini Summarizer (Vertex AI SDK).
- [x] Implement Firestore Client (for user prefs and state).
- [x] Implement Email Distributor (Resend/SendGrid).

### Phase 3: Integration & Containerization
- [x] Create `main.py` to orchestrate the pipeline.
- [x] Create `Dockerfile`.
- [ ] Test local execution (Skipped per user request).

### Phase 4: Deployment & Scheduling
- [ ] Build and push image to Artifact Registry.
- [ ] Create Cloud Run Job.
- [ ] Configure IAM permissions for the Service Account.
- [ ] Create Cloud Scheduler trigger.

