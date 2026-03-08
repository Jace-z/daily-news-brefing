from google import genai
from typing import List, Dict
import os

class GeminiSummarizer:
    """
    Summarizes news articles using Gemini 3.1 Flash-Lite on Vertex AI via the google-genai SDK.
    """

    def __init__(self, project_id: str, location: str = "global"):
        # Initialize the GenAI client configured for Vertex AI
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )
        self.model_id = "gemini-3.1-flash-lite-preview"

    def summarize_articles(self, articles: List[Dict], user_interests: List[str] = None) -> str:
        """
        Generates a summary of the provided articles.
        """
        if not articles:
            return "<p>No new articles found today.</p>"

        # Prepare context
        context = "Here are today's news headlines and summaries:\n\n"
        for i, article in enumerate(articles):
            context += f"{i+1}. {article['title']}\n"
            context += f"   Source: {article['source']}\n"
            context += f"   Summary: {article['summary']}\n\n"

        # Prepare prompt
        prompt = (
            "You are a professional news editor. Please provide a concise daily briefing "
            "based on the following articles. Focus on key takeaways and deduplicate "
            "similar stories.\n\n"
            "Format the output as clean HTML suitable for an email body. "
            "Use <h1> for the title, <h2> for section headers, <ul> and <li> for bullet points, "
            "and <strong> for emphasis. Do not include <html> or <body> tags, just the content."
        )

        if user_interests:
            prompt += f"\n\nTailor the summary to focus on these interests: {', '.join(user_interests)}."

        prompt += f"\n\nArticles:\n{context}\n\nSummary:"

        # Generate content using the new SDK
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        
        return response.text

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    project_id = os.getenv("PROJECT_ID")
    # Force global for 3.1 lite test
    location = "global"
    
    print(f"Testing GeminiSummarizer with google-genai in {location}...")
    
    summarizer = GeminiSummarizer(project_id=project_id, location=location)
    sample_articles = [
        {
            "title": "SpaceX Launches Next-Gen Starlink Satellites",
            "summary": "SpaceX successfully launched a batch of its next-generation Starlink satellites today, aimed at increasing bandwidth and reducing latency.",
            "source": "SpaceNews"
        }
    ]
    
    try:
        summary = summarizer.summarize_articles(sample_articles, user_interests=["Space", "Tech"])
        print("\nSummary Generated Successfully:")
        print("-" * 30)
        print(summary)
        print("-" * 30)
    except Exception as e:
        print(f"Error during testing: {e}")
