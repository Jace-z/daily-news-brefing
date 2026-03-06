# DailyNews AI Agent 📰

An automated LLM-powered pipeline that aggregates global news, synthesizes key takeaways, and delivers a concise daily brief directly to your inbox.

---

## ✨ Features

* **Intelligent Summarization**: Uses GPT-4o / Claude 3.5 to transform long articles into 3-bullet point summaries.
* **Custom Topics**: Configure the agent to follow specific industries, stocks, or regions.
* **Automated Delivery**: Scheduled via GitHub Actions or Cron to hit your inbox every morning.
* **Source Verification**: Cross-references multiple sources to reduce bias and identify key facts.

---

## 🛠️ Tech Stack

| Component | Technology |
| --- | --- |
| **Language** | Python 3.10+ |
| **LLM Framework** | LangChain / CrewAI |
| **Data Sources** | NewsAPI / RSS Feeds / BeautifulSoup |
| **Email Service** | SendGrid / Amazon SES / SMTP |
| **Automation** | GitHub Actions |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/daily-news-brief.git
cd daily-news-brief

```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
# API Keys
OPENAI_API_KEY=your_openai_key
NEWS_API_KEY=your_newsapi_org_key

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-bot@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=you@example.com

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Run Manually

```bash
python src/main.py

```

---

## 🤖 Pipeline Architecture

1. **Ingestion**: Scrapes top headlines from configured RSS feeds and News APIs.
2. **Filtering**: The LLM agent discards clickbait and redundant stories.
3. **Synthesis**: The agent writes a cohesive brief in Markdown/HTML.
4. **Distribution**: The system packages the brief and sends it via the configured SMTP server.

---

## 📅 Automation (GitHub Actions)

To run this daily at 8:00 AM UTC, use the provided `.github/workflows/daily_brief.yml`:

```yaml
name: Daily News Brief
on:
  schedule:
    - cron: '0 8 * * *'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Agent
        run: python src/main.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          # ... add other secrets here

```

---

## 🤝 Contributing

Feel free to open an issue or submit a pull request if you want to add new news scrapers or email templates.

---
