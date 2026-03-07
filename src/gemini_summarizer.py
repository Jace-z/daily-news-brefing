import vertexai
from vertexai.generative_models import GenerativeModel, Part
from typing import List, Dict

class GeminiSummarizer:
    """
    Summarizes news articles using Gemini 1.5 Flash on Vertex AI.
    """

    def __init__(self, project_id: str, location: str = "global"):
        vertexai.init(project=project_id, location="global")
        self.model = GenerativeModel("gemini-3.1-flash-lite-preview")

    def summarize_articles(self, articles: List[Dict], user_interests: List[str] = None) -> str:
        """
        Generates a summary of the provided articles.
        """
        if not articles:
            return "No new articles found today."

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
            "similar stories."
        )

        if user_interests:
            prompt += f"\n\nTailor the summary to focus on these interests: {', '.join(user_interests)}."

        prompt += f"\n\nArticles:\n{context}\n\nSummary:"

        # Generate content
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    # Test (requires GCP authentication)
    # summarizer = GeminiSummarizer(project_id="your-project-id")
    # articles = [{"title": "Test article", "summary": "This is a test summary", "source": "Test Source"}]
    # print(summarizer.summarize_articles(articles))
    pass
