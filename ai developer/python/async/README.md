# Async Upgrade Report

## Updated endpoint

`POST /conversations/{conversation_id}/messages`

- Converted to `async def`
- Calls the async AI service with `await`
- Protected by a 15-second timeout (`asyncio.wait_for`)
- Returns friendly HTTP errors for timeout (504), API failure (502) and unexpected errors (500)

## Async flow

1. Request arrives → FastAPI runs the endpoint on the event loop.
2. User message is saved to the database (sync SQLAlchemy is fine for short operations).
3. `await get_assistant_reply(...)` yields control while waiting for the AI.
4. Other requests can be handled during the wait.
5. When the AI answers (or times out), the endpoint continues and saves the reply.

## Concurrent study-pack endpoint

`POST /chat/study-pack`

Uses `asyncio.gather` to run three independent AI calls at the same time:

- summary
- quiz
- flashcards

## Timeout test

1. Temporarily change the timeout to `0.1` seconds.
2. Call the endpoint.
3. Expected response: `504` with message “The AI took too long to respond…”.
4. Restore the normal timeout (15 s).

## When async helps

Async is useful when the code spends most of its time **waiting** (network calls to an AI API, database, external services).  
It does **not** make pure CPU work faster.  
For three independent AI calls, concurrent execution with `gather` roughly reduces total waiting time from 3×latency to 1×latency.