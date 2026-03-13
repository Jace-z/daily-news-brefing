# GEMINI.md - Project Context & Instructions

This project is an **AI-powered Daily News Briefing Agent** that automates the aggregation, summarization, and delivery of personalized news.

## 🚀 Project Overview

The system operates as a serverless pipeline on Google Cloud Platform (GCP). It fetches news from RSS feeds and the NewsAPI, uses **Gemini 1.5 Flash** (via Vertex AI) to synthesize the content into a structured briefing, and distributes the final report via email (Resend or SendGrid).

### Core Technologies
- **Runtime:** Python 3.11+
- **LLM:** Gemini 1.5 Flash (Vertex AI) with Google Search Grounding.
- **Database:** Cloud Firestore (Native Mode) for user profiles and state.
- **Compute:** Cloud Run Jobs (Serverless execution).
- **Secrets:** GCP Secret Manager for API keys.
- **Integrations:** NewsAPI.org, RSS (feedparser), Resend/SendGrid.

---

## 🤖 Comprehensive Multi-Agent Workflow

You are an Elite Software Engineering Team. Orchestrate the installed agents as follows:

### Phase 1: Context & Architecture (Lead: planning-with-files)
- **Action**: Use `planning-with-files` to index the repository and identify dependencies.
- **Output**: A comprehensive project map in memory or a `REPO_MAP.md`.
- **Constraint**: No code changes allowed until the "Terrain" is mapped.

### Phase 2: Design & Spec (Lead: Superpowers)
- **Command**: `/superpowers:brainstorm`
- **Goal**: Use Socratic questioning to refine the user's request into a technical spec.
- **Output**: A `SPEC.md` documenting architecture, edge cases, and tech stack choices.

### Phase 3: Tactical Planning (Lead: Superpowers)
- **Command**: `/superpowers:write-plan`
- **Action**: Break the `SPEC.md` into atomic, 2-5 minute tasks.
- **Verification**: Each task must include a specific test case (TDD approach).

### Phase 4: Implementation Loop (Lead: Conductor & Jules)
- **Workflow**: 
    - **Conductor**: Execute the primary feature tasks from the plan.
    - **Jules**: Offload background tasks (refactoring existing modules, boilerplate generation) using `/jules`.
- **Constraint**: Follow the `superpowers` Red-Green-Refactor protocol: Write a test → Watch it fail → Implement code → Watch it pass.

### Phase 5: Verification (Lead: Code Review)
- **Command**: `/code-review:audit`
- **Action**: Scan all modified files for security vulnerabilities and style consistency.
- **Final Gate**: The agent must manually verify the `/execute-plan` checklist is 100% complete before finishing the session.

### Rules
1. **Methodology**: Never skip from Brainstorming to Coding. 
2. **Persistence**: Maintain a `PLAN.md` file; update it after every successful task.
3. **Validation**: Use `/superpowers:verify` after every file edit to ensure no hallucinations occurred.

---

## 🏗️ Architecture & Structure

The codebase is organized in the `src/` directory:

- `main.py`: The entry point and coordinator of the briefing pipeline.
- `gemini_summarizer.py`: Handles interaction with the Gemini API, including prompt engineering and structured JSON output.
- `news_fetcher.py`: Logic for retrieving articles from RSS feeds and the NewsAPI.
- `firestore_client.py`: CRUD operations for user profiles and tracking the `last_sent` timestamp.
- `email_distributor.py`: Handles sending emails via Resend or SendGrid REST APIs.
- `email_formatter.py`: Converts the structured summary into a polished HTML email template.
- `seed_user.py`: Utility script to initialize a test user in Firestore.

---

## 🛠️ Building and Running

### Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file based on `.env.example`:
   ```env
   PROJECT_ID=your-gcp-project-id
   LOCATION=us-central1
   SENDER_EMAIL=your-verified-email@example.com
   NEWS_API_KEY=your-newsapi-key
   EMAIL_API_KEY=your-resend-or-sendgrid-key
   EMAIL_PROVIDER=resend # or sendgrid
   USE_SECRET_MANAGER=false

   # Database Configuration
   DB_PROVIDER=firestore # or sqlite
   SQLITE_DB_PATH=users.db
   ```


3. **Seed Firestore:**
   Ensure you have GCP credentials configured (`gcloud auth application-default login`).
   ```bash
   python src/seed_user.py
   ```

4. **Run the Pipeline:**
   ```bash
   python src/main.py
   ```

### Docker
```bash
docker build -t daily-news-brief .
docker run --env-file .env daily-news-brief
```

### Deployment (GCP)
1. **Build:** `gcloud builds submit --tag gcr.io/[PROJECT_ID]/daily-news-brief`
2. **Deploy Job:** `gcloud run jobs create daily-news-job --image gcr.io/[PROJECT_ID]/daily-news-brief`
3. **Schedule:** Create a Cloud Scheduler trigger pointing to the Cloud Run Job URL.

---

## 📝 Development Conventions

- **State Management:** The agent uses a `last_sent` timestamp in Firestore to ensure it only summarizes news published since the last briefing (minimum 48h window).
- **Structured Output:** Gemini is configured to return JSON. Always update the `response_schema` in `gemini_summarizer.py` if the UI/Email format changes.
- **Grounding:** The `GeminiSummarizer` uses `google_search` tool to research and synthesize deeper insights beyond just the headline.
- **Security:** In production (`USE_SECRET_MANAGER=true`), secrets are fetched from GCP Secret Manager rather than environment variables.
