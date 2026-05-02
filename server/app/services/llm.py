from openai import OpenAI
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


def generate_response(query: str, context: str) -> str:
    api_key = settings.openai_api_key

    if not api_key or api_key in ["your_openai_api_key_here", "", "sk-...", "sk-test"]:
        return "OpenAI API key is not configured. Please add your real API key to the .env file as OPENAI_API_KEY."

    try:
        client = OpenAI(api_key=api_key)

        if context == "No relevant context found.":
            prompt = f"""You are a helpful AI assistant. Answer the user's question directly.

User Question: {query}

Answer:"""
        else:
            prompt = f"""You are a helpful AI assistant. Use the following context to answer the user's question.

Context:
{context}

User Question: {query}

Answer:"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        error_str = str(e)
        if "image" in error_str.lower() and ("does not support" in error_str.lower() or "input" in error_str.lower()):
            return "This model does not support image input. Please send text-only queries."
        elif "api key" in error_str.lower() or "invalid" in error_str.lower() or "authentication" in error_str.lower():
            return f"OpenAI API authentication error. Please verify your API key is valid and not expired. Error: {error_str}"
        else:
            logger.error(f"OpenAI API error: {e}")
            return f"I encountered an error: {error_str}"