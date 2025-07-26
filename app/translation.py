from dotenv import load_dotenv
import os
from openai import OpenAI
import time

load_dotenv()

def translate_text_to_chinese(text: str, model="gpt-4o-mini") -> str:
    """
    Translates English text into fluent Mandarin using GPT.

    Args:
        text (str): The English text to translate.
        model (str): OpenAI model to use ("gpt-4o-mini", "gpt-4o", etc).

    Returns:
        str: Translated Mandarin Chinese text.
        
    Raises:
        ValueError: If text is empty or invalid
        RuntimeError: If API key is missing or invalid
        Exception: For other API or network errors
    """
    
    # Validate input
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in environment variables")
    
    try:
        # Create client
        client = OpenAI(api_key=api_key)
        
        system_prompt = "You are a professional translator. Translate the following English text into natural, fluent Mandarin Chinese."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3
        )

        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")