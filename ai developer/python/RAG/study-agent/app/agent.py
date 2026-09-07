# agent.py

import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent   # ← keep this

load_dotenv()

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2"), temperature=0.3)

    elif provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.3,
        )

    elif provider == "mistral":
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(
            model=os.getenv("MISTRAL_MODEL", "mistral-small-latest"),
            api_key=os.getenv("MISTRAL_API_KEY"),
            temperature=0.3,
        )

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic math expression. Example: '25 * 4 + 10'"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


@tool
def get_current_topic() -> str:
    """Return the current study topic (demo tool)."""
    return "Python programming and LangChain agents"


tools = [calculator, get_current_topic]

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful study assistant. Use tools when needed."),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)