# MCP Agent Client

This project demonstrates how to connect a LangChain AI agent to tools exposed by an **MCP (Model Context Protocol) server**.

The agent uses:

* Python
* LangChain
* Ollama
* `llama3.2`
* `langchain-mcp-adapters`
* MCP

---

## Project Structure

```text
project/
│
├── server.py
├── agentClient.py
└── README.md
```

### `server.py`

Contains the MCP server and the tools exposed to the AI agent.

### `agentClient.py`

Connects to the MCP server, discovers its tools, creates the AI agent, sends a user request, and displays the agent's execution.

---

# 1. How It Works

The overall architecture is:

```text
                 USER
                   │
                   │
                   ▼
             LangChain Agent
                   │
                   │ decides which tool
                   ▼
          MCP Client Adapter
                   │
                   │
                   ▼
              MCP Server
             /     |      \
            /      |       \
          add   multiply   study tools
            \      |       /
             \     |      /
                   ▼
              Tool Result
                   │
                   ▼
             LangChain Agent
                   │
                   ▼
              Final Answer
```

The important idea is that the AI agent does not need to know the implementation of each tool.

It only needs to know:

* the tool name
* what the tool does
* the arguments it accepts

The MCP server provides this information.

---

# 2. Installing Dependencies

Install the required packages:

```bash
pip install langchain
pip install langchain-ollama
pip install langchain-mcp-adapters
pip install mcp
```

Make sure Ollama is installed and running.

You also need the model:

```bash
ollama pull llama3.2
```

---

# 3. MCP Tools

The MCP server exposes tools such as:

```text
add
multiply
explain_topic
create_study_plan
generate_revision_checklist
```

The client does not manually define these tools.

Instead, this code discovers them:

```python
tools = await client.get_tools()
```

We can then print them:

```python
for tool in tools:
    print("-", tool.name)
```

Example output:

```text
Available tools:
- add
- multiply
- explain_topic
- create_study_plan
- generate_revision_checklist
```

This demonstrates one of the important benefits of MCP:

> The client can discover tools provided by the server.

---

# 4. Connecting to the MCP Server

The client connects to `server.py` using the `stdio` transport:

```python
client = MultiServerMCPClient(
    {
        "calculator": {
            "transport": "stdio",
            "command": "python",
            "args": ["server.py"],
        }
    }
)
```

The important part is:

```text
transport = stdio
```

This means the MCP server runs as a subprocess and communicates with the client through standard input/output.

---

# 5. Getting the MCP Tools

The client retrieves the tools from the MCP server:

```python
tools = await client.get_tools()
```

The MCP tools are then converted into tools that LangChain understands.

So we have:

```text
MCP Tool
   ↓
langchain-mcp-adapters
   ↓
LangChain Tool
   ↓
LangChain Agent
```

---

# 6. Creating the AI Agent

The model is created using Ollama:

```python
model = ChatOllama(
    model="llama3.2",
    temperature=0
)
```

Then the agent is created:

```python
agent = create_agent(
    model,
    tools
)
```

The agent now has access to all the tools discovered from the MCP server.

---

# 7. Agent-Style Demonstration

We send the agent:

```text
what is 3 + 5?
```

The agent looks at the available tools and decides that:

```text
add
```

is the appropriate tool.

It then generates arguments:

```python
{
    "a": "3",
    "b": "5"
}
```

The execution becomes:

```text
User Request
     │
     ▼
"What is 3 + 5?"
     │
     ▼
LLM Agent
     │
     ▼
Select Tool
     │
     ▼
add
     │
     ▼
a = 3
b = 5
     │
     ▼
MCP Server
     │
     ▼
add(3, 5)
     │
     ▼
8
     │
     ▼
LLM
     │
     ▼
"The answer is 8."
```

---

# 8. Printing the Selected Tool

The agent's response contains the tool call.

We inspect it with:

```python
if hasattr(message, "tool_calls") and message.tool_calls:

    for tool_call in message.tool_calls:

        print("Tool name:", tool_call["name"])
        print("Arguments:", tool_call["args"])
```

Example:

```text
MCP TOOL SELECTED
-----------------
Tool name: add
Arguments: {'a': '3', 'b': '5'}
```

This allows us to see what the agent decided to do.

---

# 9. Validating the Tool

We first create a list of tools that the MCP server actually exposed:

```python
allowed_tools = []

for tool in tools:
    allowed_tools.append(tool.name)
```

For example:

```python
[
    "add",
    "multiply",
    "explain_topic",
    "create_study_plan",
    "generate_revision_checklist"
]
```

When the agent selects a tool, we check:

```python
if tool_name in allowed_tools:
    print("VALIDATION PASSED")
else:
    print("VALIDATION FAILED")
```

This gives us a basic safety check.

The agent should only be allowed to use tools that the MCP client actually received from the server.

---

# 10. Different Tools Can Have Different Arguments

One important advantage of using the LangChain MCP adapter is that we do not need to manually write:

```python
if tool_name == "add":
    ...

if tool_name == "create_study_plan":
    ...

if tool_name == "explain_topic":
    ...
```

Each MCP tool exposes its own schema.

For example:

```text
add
a: integer
b: integer
```

while:

```text
create_study_plan
topic: string
days: integer
```

and:

```text
explain_topic
topic: string
level: string
```

The agent can therefore select different tools and provide the appropriate arguments.

For example:

```text
User:
What is 3 + 5?

Agent:
add(a=3, b=5)
```

Another request:

```text
User:
Create a 3-day Java study plan.

Agent:
create_study_plan(
    topic="Java",
    days=3
)
```

Another:

```text
User:
Explain inheritance in Java to a beginner.

Agent:
explain_topic(
    topic="Java inheritance",
    level="beginner"
)
```

The tool arguments are determined from the tools' schemas rather than hardcoded in the client.

---

# 11. Tool Results

After the MCP tool executes, the result is returned to the agent as a `ToolMessage`.

We can inspect it:

```python
if type(message).__name__ == "ToolMessage":

    print("MCP TOOL RESULT")
    print(message.content)
```

For the calculator:

```text
MCP TOOL RESULT
---------------
8
```

The agent then receives the result and generates the final response.

---

# 12. Handling Tool Failures

A tool can fail.

For example, the MCP server may reject invalid input, encounter an internal problem, or return an error.

The tool result can be represented as an error `ToolMessage`.

We can check:

```python
if hasattr(message, "status"):

    if message.status == "error":

        print("MCP TOOL FAILURE")
        print("The MCP tool returned an error.")
```

The important flow is:

```text
Agent
  │
  ▼
MCP Tool
  │
  ├──── Success ────► Tool Result
  │
  └──── Failure ────► Error
                         │
                         ▼
                    ToolMessage
                    status="error"
```

For example, if a study-plan tool rejects an invalid number of days, the server might return an error such as:

```text
Invalid number of days.
```

The client can detect that the tool failed instead of assuming every tool call succeeded.

---

# 13. Why Tool Failures Matter

An AI agent operates in an environment where tools can fail.

For example:

```text
Database unavailable
API timeout
Invalid arguments
Permission denied
External service unavailable
Server exception
```

A robust agent should not simply assume:

```text
Tool call = Success
```

Instead:

```text
Tool call
    │
    ▼
Did it succeed?
   / \
 YES  NO
 │     │
 ▼     ▼
Use   Handle
result error
```

This becomes especially important when building production agents.

---

# 14. Running the Client

Start the client:

```bash
python agentClient.py
```

You should see something similar to:

```text
Available tools:
- add
- multiply
- explain_topic
- create_study_plan
- generate_revision_checklist

Allowed tools:
['add', 'multiply', 'explain_topic',
 'create_study_plan',
 'generate_revision_checklist']

========================================
USER REQUEST
========================================
what is 3 + 5?

========================================
AGENT EXECUTION
========================================

Message type: HumanMessage

Message type: AIMessage

MCP TOOL SELECTED
-----------------
Tool name: add
Arguments: {'a': '3', 'b': '5'}

Validating tool...
VALIDATION PASSED
'add' is an allowed MCP tool.

Message type: ToolMessage

MCP TOOL RESULT
---------------
8

Message type: AIMessage

AI RESPONSE
-----------
The answer to the question "what is 3 + 5?" is 8.
```

---

# 15. Key Concepts Learned

At this point, the application demonstrates:

### MCP Server

Provides tools:

```text
add
multiply
explain_topic
create_study_plan
generate_revision_checklist
```

### MCP Client

Connects to the MCP server:

```python
MultiServerMCPClient(...)
```

### Tool Discovery

Retrieves available tools:

```python
await client.get_tools()
```

### LangChain Agent

Uses the tools:

```python
create_agent(model, tools)
```

### Tool Selection

The LLM decides which tool is appropriate.

### Tool Arguments

The agent generates arguments based on the tool's schema.

### Tool Execution

The MCP server executes the selected tool.

### Tool Result

The result is returned to the agent.

### Error Handling

The client can detect a failed tool execution.

---

# 16. Complete Agent Flow

The complete system is:

```text
                 USER
                   │
                   ▼
             USER REQUEST
                   │
                   ▼
             LANGCHAIN AGENT
                   │
                   │
             ┌─────▼─────┐
             │ LLM DECIDES│
             │ TOOL       │
             └─────┬─────┘
                   │
                   ▼
          TOOL NAME + ARGUMENTS
                   │
                   ▼
             VALIDATION
                   │
              ┌────┴────┐
              │         │
            VALID     INVALID
              │         │
              ▼         ▼
          MCP TOOL    REJECT
              │
              ▼
          MCP SERVER
              │
              ▼
        TOOL EXECUTION
           /       \
       SUCCESS    FAILURE
          │          │
          ▼          ▼
     Tool Result   Error
          │          │
          └────┬─────┘
               ▼
           TOOL MESSAGE
               │
               ▼
          LANGCHAIN AGENT
               │
               ▼
          FINAL RESPONSE
               │
               ▼
              USER
```

