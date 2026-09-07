
# AI Study Assistant API

FastAPI backend that provides interactive study and health-information features.  
Supports **Groq**, **Mistral**, and **OpenAI** through a single provider-agnostic interface.

## Features

- **Provider Agnostic** – Switch between `groq`, `mistral`, and `openai` with one environment variable (`LLM_PROVIDER`).
- **Streaming Chat** (`POST /chat`) – Real-time token streaming via `StreamingResponse`.
- **Structured Quiz Generation** (`POST /quiz`) – Returns schema-validated JSON quizzes.
- **Medical Chat with Safeguards** (`POST /medical/chat`) – Practical health information tailored for low-resource settings in Nigeria/Africa, with refusal of diagnosis and specific drug advice.
- **Resilient** – Automatic exponential backoff and retry on 429 rate-limit errors.

---

## Setup & Running

### 1. Clone & create virtual environment

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

```env
# Required
LLM_PROVIDER=groq                 # options: groq | mistral | openai

# API Keys (only the one matching LLM_PROVIDER is required)
GROQ_API_KEY=your_groq_key_here
MISTRAL_API_KEY=your_mistral_key_here
OPENAI_API_KEY=your_openai_key_here

# Optional model overrides
GROQ_MODEL=openai/gpt-oss-20b
MISTRAL_MODEL=mistral-small-latest
OPENAI_MODEL=gpt-4o-mini
```

> **Note**: Older Groq models (`llama-3.1-8b-instant`, `llama-3.3-70b-versatile`) were deprecated in August 2026. Use `openai/gpt-oss-20b` or `openai/gpt-oss-120b` instead.

### 3. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

## Main Endpoints

| Method | Path              | Description                                      |
|--------|-------------------|--------------------------------------------------|
| POST   | `/chat`           | Streaming study chat                             |
| POST   | `/quiz`           | Generate a validated JSON quiz                   |
| POST   | `/medical/chat`   | Health information with safety safeguards        |
| GET    | `/health`         | Simple health check                              |

---

## Medical Safeguard Summary

The `/medical/chat` endpoint is designed for users who may have limited access to hospitals or pharmacies. It:

- Refuses to diagnose or prescribe specific drugs/dosages.
- Provides practical general guidance (hydration, rest, danger signs).
- Encourages seeking help from the nearest available facility when symptoms are serious.
- Applies a lightweight content filter as a second safety layer.

---

## Switching Providers

Change only the `LLM_PROVIDER` value in `.env` and restart the server.  
No code changes are required.
