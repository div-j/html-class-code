import os
del os.environ['SSL_CERT_FILE']

import asyncio
import json
import sys
from typing import Any

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()


# -----------------------------
# Ollama model (change if needed)
# -----------------------------
llm = ChatOllama(
    model="llama3.2",          # or "qwen2.5", "llama3.2", "mistral", etc.
    temperature=0,
)


def choose_tool(
    user_request: str,
    tools: list[Any]
) -> dict[str, Any]:

    tool_descriptions = []

    for tool in tools:
        tool_descriptions.append({
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        })

    prompt = f"""
You are an AI agent choosing an MCP tool.

Available MCP tools:
{json.dumps(tool_descriptions, indent=2)}

User request:
{user_request}

Choose the most appropriate tool.

Return ONLY valid JSON:

{{
    "tool_name": "name_here",
    "arguments": {{}}
}}

Rules:
- The tool_name MUST be one of the available tools.
- Arguments MUST follow the tool's input schema.
- Do not invent tools.
- Do not invent arguments.
- Return ONLY JSON.
"""

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    content = response.content.strip()

    if content.startswith("```"):
        content = content.strip("`")

        if content.startswith("json"):
            content = content[4:].strip()

    return json.loads(content)


def validate_tool_decision(
    decision: dict[str, Any],
    tools: list[Any]
) -> tuple[str, dict[str, Any]]:

    tool_name = decision.get("tool_name")
    arguments = decision.get("arguments", {})

    if not tool_name:
        raise ValueError(
            "The model did not return a tool_name."
        )

    if not isinstance(arguments, dict):
        raise ValueError(
            "Tool arguments must be a JSON object."
        )

    allowed_tools = []

    for tool in tools:
        allowed_tools.append(tool.name)

    if tool_name not in allowed_tools:
        raise ValueError(
            f"Tool not allowed: {tool_name}"
        )

    return tool_name, arguments


async def main():
    user_request = "Create a 3-day plan to learn MCP."

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            tools_response = await session.list_tools()
            tools = tools_response.tools

            print("\nAvailable tools:")

            for tool in tools:
                print("-", tool.name)

            try:
                decision = choose_tool(user_request, tools)
                tool_name, arguments = validate_tool_decision(decision, tools)
                result = await session.call_tool(tool_name, arguments)

                print("\nUser request:", user_request)
                print("Tool chosen:", tool_name)
                print("Arguments:", arguments)
                print("Tool result:", result.content)

            except json.JSONDecodeError as e:
                print("The model did not return valid JSON:", e)
            except Exception as error:
                print("Agent workflow failed:", str(error))


if __name__ == "__main__":
    asyncio.run(main())