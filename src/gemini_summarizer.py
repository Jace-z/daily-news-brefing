from google import genai
from google.genai import types
from typing import List, Dict
import os
import json

class GeminiSummarizer:
    """
    Summarizes news articles using Gemini 3.1 Flash-Lite on Vertex AI.
    Outputs structured JSON for programmatic formatting.
    """

    def __init__(self, project_id: str, location: str = "global"):
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location="global" # Hardcoded for 3.1-lite availability
        )
        self.model_id = "gemini-3.1-flash-lite-preview"

    def summarize_articles(self, articles: List[Dict], user_interests: List[str] = None) -> Dict:
        """
        Generates a structured JSON summary of the articles.
        """
        if not articles:
            return {"sections": []}

        # Prepare context focusing on LINKS
        context = "Here are today's top news stories:\n\n"
        for i, article in enumerate(articles):
            context += f"{i+1}. {article['title']}\n"
            context += f"   URL: {article['link']}\n"
            context += f"   Source: {article['source']}\n\n"

        # Schema for the response
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "sections": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "section_title": {"type": "STRING"},
                            "stories": {
                                "type": "ARRAY",
                                "items": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "title": {"type": "STRING"},
                                        "summary": {"type": "STRING"},
                                        "link": {"type": "STRING"},
                                        "source": {"type": "STRING"}
                                    },
                                    "required": ["title", "summary", "link", "source"]
                                }
                            }
                        },
                        "required": ["section_title", "stories"]
                    }
                }
            },
            "required": ["sections"]
        }

        prompt = (
            "You are a senior editor at The New York Times. Create 'The Morning Brief'.\n\n"
            "INSTRUCTION: Use your Google Search tool to research the provided URLs and "
            "synthesize a deep, analytical summary for each story.\n\n"
            "OUTPUT REQUIREMENT: Return a valid JSON object matching the requested schema. "
            "Group stories into 2-3 logical thematic sections. Summaries should be 2-3 sentences, "
            "sophisticated, and objective."
        )

        if user_interests:
            prompt += f"\n\nFocus on: {', '.join(user_interests)}."

        prompt += f"\n\nArticles to Research:\n{context}"

        # Generate structured content
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        
        # Parse and return the JSON
        try:
            return json.loads(response.text)
        except Exception as e:
            print(f"Error parsing Gemini JSON: {e}")
            return {"sections": []}

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    project_id = os.getenv("PROJECT_ID")
    summarizer = GeminiSummarizer(project_id=project_id)
    
    sample_articles = [
        {
            "title": "SpaceX Starship Sixth Flight Test",
            "link": "https://www.spacex.com/launches/mission/?missionId=starship-flight-6",
            "source": "SpaceX"
        }
    ]
    
    result = summarizer.summarize_articles(sample_articles, user_interests=["SpaceX"])
    print(json.dumps(result, indent=2))
