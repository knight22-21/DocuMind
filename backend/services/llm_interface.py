import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_answer(query: str, context_chunks: list[str]) -> str:
    prompt = f"""You are a research assistant.
Use the following context to answer the question. Be accurate and concise.
If the answer is not in the context, say "Not found in context."

Context:
{'\n\n'.join(context_chunks)}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
