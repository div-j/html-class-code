import os
from dotenv import load_dotenv
from groq import Groq, AuthenticationError, RateLimitError

# Load environment variables
load_dotenv()
os.environ.pop("SSL_CERT_FILE", None) 
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize the Groq client
client = Groq(api_key=api_key)

def call_llm(user_message: str) -> dict:
    try:
        response = client.chat.completions.create(
            messages=[
                   {
                        "role": "system",
                        "content": "you are a study assistant"
                      },
                        {
                            "role": "user",
                            "content": user_message,
                        }
            ],
            model="openai/gpt-oss-120b",
            temperature=0.3,
            max_tokens=700,
            # max_completion_tokens=700
        )
        
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else 0
        
        return {
            "answer": answer,
            "model": response.model,
            "tokens_used": tokens_used
        }
        
    except AuthenticationError:
        return {
            "answer": "Invalid Groq API key. Please check your backend configuration.",
            "model": "error",
            "tokens_used": 0
        }
    except RateLimitError:
        return {
            "answer": "The Groq service rate limit was exceeded. Please try again shortly.",
            "model": "rate_limited",
            "tokens_used": 0
        }
    except Exception as error:
        return {
            "answer": f"Unexpected Groq service error: {str(error)}",
            "model": "error",
            "tokens_used": 0
        }


