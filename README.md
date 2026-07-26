# User Management Agent

An OpenAI Agents SDK project that connects to a remote MCP server for user-management tasks. The agent is designed to answer questions by calling MCP tools rather than inventing user data.

## What Is In This Repo

- `main.py` - command-line chat loop for talking to the agent
- `app.py` - Streamlit UI for a simple browser-based chat experience
- `agent.py` - shared agent setup used by the Streamlit app
- `demo.py` - standalone OpenAI chat demo, separate from the MCP agent flow
- `tools_schema.txt` - exported tool schema/reference for the MCP server

## Features

- Uses the OpenAI Agents SDK
- Connects to a remote MCP server over Streamable HTTP
- Uses environment variables for configuration
- Supports both CLI and Streamlit interfaces

## Requirements

- Python 3.11+
- An OpenAI API key
- A reachable MCP server URL

## Setup

Create and activate your environment, then install dependencies:

```bash
uv sync
```

Create a `.env` file with the required values:

```env
OPENAI_API_KEY=your_openai_api_key
MCP_SERVER_URL=https://your-mcp-server.example.com
MCP_SERVER_NAME=User Management MCP
MODEL=gpt-4o-mini
MODEL_TEMPERATURE=0.2
```

Notes:

- `OPENAI_API_KEY` is required
- `MCP_SERVER_URL` is required for the agent to connect to tools
- `MCP_SERVER_NAME` is optional and used only for logging in `main.py`
- `MODEL` defaults to `gpt-4o-mini` if omitted
- `MODEL_TEMPERATURE` defaults to `0.2` in the agent entry points

## Run

### CLI chat

```bash
uv run python main.py
```

Type your question at the prompt. Enter `exit` to quit.

### Streamlit app

```bash
uv run streamlit run app.py
```

This opens a browser-based chat interface with conversation history.

## How It Works

1. The user asks a question.
2. The agent connects to the MCP server defined by `MCP_SERVER_URL`.
3. The agent selects the best available MCP tool.
4. The tool result is returned in simple English.

The system prompt explicitly tells the agent to:

- always use MCP tools
- avoid making up user information
- choose the best tool automatically
- respond politely when no suitable tool exists

## Troubleshooting

- If you see `OPENAI_API_KEY environment variable is not set`, make sure your `.env` file is present and loaded.
- If the agent cannot connect to tools, verify `MCP_SERVER_URL` is correct and reachable.
- If Streamlit does not start, confirm `streamlit` is installed in the same environment created by `uv sync`.

## Example

```text
You: Show all users older than 30
Assistant: ...
```
