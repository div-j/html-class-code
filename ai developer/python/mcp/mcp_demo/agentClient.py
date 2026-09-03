
import os
del os.environ['SSL_CERT_FILE']

import asyncio

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    # 1. Connect to our MCP server
    client = MultiServerMCPClient(
        {
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"],
            }
        }
    )

    # 2. Get tools from the MCP server
    tools = await client.get_tools()
    
    allowed_tools = []

    print("Available tools:")

    for tool in tools:
        # print("-", tool.name)
        allowed_tools.append(tool.name)
    
    print("\nAllowed tools:")
    print(allowed_tools)
    
    # 3. Create our LLM
    model = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    # 4. Create the agent
    agent = create_agent(
        model,
        tools
    )
    
    user_request = "what is 3 + 5?"
    print("\n--- User Request ---")
    print(user_request)

    # 5. Ask the agent a question
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request
                }
            ]
        }
    )

    # 6. Print the final response
    print("\n--- Agent Execution ---")

    for message in response["messages"]:

        print("\nMessage type:", type(message).__name__)

        # Check if the LLM called a tool
        if hasattr(message, "tool_calls") and message.tool_calls:

            for tool_call in message.tool_calls:
                tool_name = tool_call["name"]
                arguments = tool_call["args"]
                print("\nMCP TOOL CALLED:")
                print("Tool name:", tool_name)
                print("Arguments:", arguments)
                
                print("\nValidating tool...") 
                if tool_name in allowed_tools: 
                    print("VALIDATION PASSED") 
                    print( f"'{tool_name}' is an allowed MCP tool." )
                    
                else: 
                    print("VALIDATION FAILED") 
                    print( f"'{tool_name}' is NOT an allowed MCP tool." )

        # Print normal AI response
        if type(message).__name__ == "AIMessage":
            if message.content:
                print("\nAI RESPONSE:")
                print(message.content)
                
if __name__ == "__main__":
    asyncio.run(main())