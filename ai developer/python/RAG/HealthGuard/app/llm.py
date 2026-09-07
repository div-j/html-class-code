import os
import json
from typing import AsyncGenerator, List, Dict, Any

from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

load_dotenv()

# Optional SSL workaround
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]


def get_llm_provider() -> str:
    return os.getenv("LLM_PROVIDER", "groq").lower()


def is_rate_limit_error(exception: BaseException) -> bool:
    """Detect 429 / rate-limit errors across providers."""
    # Mistral
    try:
        from mistralai.client.errors.sdkerror import SDKError
        if isinstance(exception, SDKError) and getattr(exception, "status_code", None) == 429:
            return True
    except ImportError:
        pass

    # Groq / OpenAI style
    status = getattr(exception, "status_code", None) or getattr(exception, "status", None)
    if status == 429:
        return True

    msg = str(exception).lower()
    return "429" in msg or "rate limit" in msg or "rate_limited" in msg or "too many requests" in msg


rate_limit_retry = retry(
    retry=retry_if_exception(is_rate_limit_error),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=3, max=30),
    reraise=True,
)


async def stream_chat_response(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    provider = get_llm_provider()
    print(f"Using LLM provider: {provider}")
    if provider == "groq":
        from groq import AsyncGroq
        client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        

        @rate_limit_retry
        async def _create():
            return await client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"), 
                messages=messages,
                stream=True,
            )

        stream = await _create()
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    elif provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        @rate_limit_retry
        async def _create():
            return await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=messages,
                stream=True,
            )

        stream = await _create()
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    elif provider == "mistral":
        from mistralai.client import Mistral
        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        print("Using Mistral provider for streaming chat responses.")

        @rate_limit_retry
        async def _create():
            return await client.chat.stream_async(
                model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
                messages=messages,
            )

        stream = await _create()
        async for chunk in stream:
            # Mistral stream structure
            if hasattr(chunk, "data") and chunk.data.choices:
                content = chunk.data.choices[0].delta.content
                if content:
                    yield content
            elif hasattr(chunk, "choices") and chunk.choices:
                # fallback for some SDK versions
                content = chunk.choices[0].delta.content
                if content:
                    yield content

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


async def generate_json_response(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    provider = get_llm_provider()

    if provider == "groq":
        from groq import AsyncGroq
        client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        

        @rate_limit_retry
        async def _call():
            return await client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),  # ← working default
                messages=messages,
                response_format={"type": "json_object"},
            )

        response = await _call()
        return json.loads(response.choices[0].message.content)

    elif provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        @rate_limit_retry
        async def _call():
            return await client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=messages,
                response_format={"type": "json_object"},
            )

        response = await _call()
        return json.loads(response.choices[0].message.content)

    elif provider == "mistral":
        from mistralai.client import Mistral
        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        print("Using Mistral provider.")

        @rate_limit_retry
        async def _call():
            return await client.chat.complete_async(
                model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
                messages=messages,
                response_format={"type": "json_object"},
            )

        response = await _call()
        return json.loads(response.choices[0].message.content)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")