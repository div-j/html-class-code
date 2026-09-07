# AI Study Assistant API

FastAPI backend providing interactive study assistant features powered by OpenAI or Mistral models.

## Features
- **Provider Agnostic**: Switch seamlessly between Mistral and OpenAI using `LLM_PROVIDER`.
- **Streaming Chat (`/chat`)**: Real-time response streaming via `StreamingResponse`.
- **Structured Quiz Generation (`/quiz`)**: Generates schema-validated JSON quiz questions.
- **Resilient**: Exponential backoff and retry for 429 Rate Limit errors.

---

## Setup & Running

1. **Clone & Setup Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt


LLM_PROVIDER=mistral
MISTRAL_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

2. **Run the APP**

uvicorn app.main:app --reload