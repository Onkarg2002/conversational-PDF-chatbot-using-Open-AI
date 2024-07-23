import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_response(question: str, context: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=f"Context: {context}\n\nQuestion: {question}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)
