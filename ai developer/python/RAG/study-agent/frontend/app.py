import os
import requests
import gradio as gr

LANGSERVE_URL = os.getenv("LANGSERVE_URL", "http://127.0.0.1:8000/agent/invoke")

def chat_with_agent(user_message, history):
    payload = {
        "input": {
            "input": user_message
        }
    }
    try:
        response = requests.post(LANGSERVE_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        output = data.get("output", {}).get("output", "No response generated.")
        return output
    except requests.exceptions.RequestException as e:
        return f"Error connecting to agent backend: {str(e)}"

demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="🚀 StudyPulse AI Agent",
    description="Interact with the Llama-3 powered LangChain agent served via LangServe.",
    examples=["Calculate study hours for 5 hard topics", "Explain gradient descent in simple terms"]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)