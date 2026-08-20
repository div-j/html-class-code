from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(
    api_key=api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
         {
        "role": "system",
        "content": "you are a study assistant"
      },
        {
            "role": "user",
            "content": "hi",
        }
    ],
    model="openai/gpt-oss-120b",
)

print(chat_completion.choices[0].message.content)

