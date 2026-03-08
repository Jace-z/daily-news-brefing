from google import genai
from google.genai import types
from typing import List, Dict
import os

class GeminiSummarizer:
    """
    Summarizes news articles using Gemini 3.1 Flash-Lite on Vertex AI.
    Uses Google Search Grounding to fetch full content from provided links.
    """

    def __init__(self, project_id: str, location: str = "global"):
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )
        self.model_id = "gemini-3.1-flash-lite-preview"

    def summarize_articles(self, articles: List[Dict], user_interests: List[str] = None) -> str:
        """
        Generates a summary by allowing Gemini to research the provided article links.
        """
        if not articles:
            return "<p>No new articles found today.</p>"

        # Prepare context focusing on LINKS
        context = "Here are today's top news stories. Please use these links to research the full details:\n\n"
        for i, article in enumerate(articles):
            context += f"{i+1}. {article['title']}\n"
            context += f"   URL: {article['link']}\n"
            context += f"   Source: {article['source']}\n\n"

        # Refined NYT-style prompt
        prompt = (
            "You are a senior editor at The New York Times. Your task is to write 'The Morning Brief'.\n\n"
            "CRITICAL INSTRUCTION: Do NOT rely solely on the provided titles. Use your Google Search tool "
            "to access the provided URLs and synthesize a deep, analytical summary of the actual article content.\n\n"
            "Guidelines:\n"
            "- Tone: Authoritative, objective, and sophisticated.\n"
            "- Structure: Organize into 2-3 thematic sections (e.g., Global Affairs, Science & Tech).\n"
            "- Citations: For each story, include a hyperlinked reference at the end of the summary (e.g., <a href='URL'>Source</a>).\n"
            "- Format: Clean HTML body. Use <h1> for the title, <h2> for sections, and <p> for paragraphs. "
            "Use <strong> for key entities."
        )

        if user_interests:
            prompt += f"\n\nFocus your research on these interests: {', '.join(user_interests)}."

        prompt += f"\n\nArticles to Research:\n{context}\n\nAnalytical Briefing:"

        # Generate content with Google Search Grounding enabled
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        return response.text

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    project_id = os.getenv("PROJECT_ID")
    location = "global"
    
    print(f"Testing Grounded GeminiSummarizer in {location}...")
    
    summarizer = GeminiSummarizer(project_id=project_id, location=location)
    # Using a real, recent link for testing grounding
    sample_articles = [
        {
            "title": "SpaceX Starship Sixth Flight Test",
            "link": "https://www.spacex.com/launches/mission/?missionId=starship-flight-6",
            "source": "SpaceX"
        }
    ]
    
    try:
        summary = summarizer.summarize_articles(sample_articles, user_interests=["SpaceX", "Starship"])
        print("\nSummary Generated with Grounding:")
        print("-" * 30)
        print(summary)
        print("-" * 30)
    except Exception as e:
        print(f"Error during testing: {e}")
