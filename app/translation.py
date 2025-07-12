from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def translate_text_to_chinese(text: str, model="gpt-4o-mini") -> str:
    """
    Translates English text to Chinese using OpenAI's Chat API.
    Returns the translated text as a string.
    """

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


def translate_file(input_path: str, output_path: str):
    """
    Reads a text file, translates it to Chinese, and writes the result.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        english_text = f.read()

    print("Translating to Chinese...")
    chinese_text = translate_text_to_chinese(english_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(chinese_text)

    print(f"Translation saved to: {output_path}")