from functools import lru_cache
import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

os.environ.pop("SSL_CERT_FILE", None) 

api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not set")

client = Mistral(api_key=api_key)

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a friendly study assistant. "
        "Explain simply, use short sentences, "
        "and end with one practice question."
    )
}

def get_assistant_reply(user_message: str, history: list[dict] | None = None) -> str:
    """
    Generate a reply from Mistral.
    
    - user_message: the new message from the user
    - history: optional list of previous messages 
               (each item: {"role": "user"|"assistant", "content": "..."})
    """
    
    messages = [SYSTEM_PROMPT]
    
    if history:
        messages.extend(history)


    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=messages,
            temperature=0.3,
            max_tokens=300,
        )

        reply = response.choices[0].message.content
        return reply

        # Keep conversation history
        messages.append({"role": "assistant", "content": reply})

    except Exception as error:
        print("Something went wrong:", error)
        return "Sorry, I couldn't generate a reply right now. Please try again."
    
    
@lru_cache(maxsize=128)
def get_cached_reply(user_message: str) -> str:
    """
    Cache is temporary (lives only in memory).
    Database is the permanent source of truth.
    Only use this for repeated, non-sensitive questions.
    """
    return get_assistant_reply(user_message)