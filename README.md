# User Management Agent

An agent project that connects to a remote MCP server for user-management tasks. The agents are designed to answer questions by calling MCP tools rather than inventing user data.

## Project Structure

```text
user-management-agent/
├── Dockerfile
├── .dockerignore
├── user_management_agent/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   ├── mcp.py
│   ├── openai_agent.py
│   ├── langgraph_agent.py
│   ├── streamlit_app.py
│   ├── cli_openai.py
│   └── cli_langgraph.py
├── app.py
├── main.py
├── agent_openai.py
├── agent_langgrap.py
├── demo.py
├── tools_schema.txt
├── pyproject.toml
├── uv.lock
└── README.md
```

- `user_management_agent/` - main Python package
- `app.py` - compatibility wrapper for the Streamlit app
- `main.py` - compatibility wrapper for the OpenAI CLI
- `agent_openai.py` - compatibility wrapper for the OpenAI agent module
- `agent_langgrap.py` - compatibility wrapper for the LangGraph agent module
- `demo.py` - standalone OpenAI chat demo, separate from the MCP agent flow
- `tools_schema.txt` - exported tool schema reference for the MCP server
- `Dockerfile` - container image for the Streamlit app
- `.dockerignore` - excludes local environment and build artifacts from Docker

## Features

- OpenAI Agents SDK support
- LangChain and LangGraph support
- Remote MCP server integration over Streamable HTTP
- Environment-based configuration
- CLI and Streamlit entry points

## Requirements

- Python 3.11+
- An OpenAI API key
- A reachable MCP server URL

## Setup

Install dependencies:

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
- `MCP_SERVER_NAME` is optional and used for logging and the LangGraph MCP client
- `MODEL` defaults to `gpt-4o-mini` if omitted
- `MODEL_TEMPERATURE` defaults to `0.2`

## Docker

Build the container image:

```bash
docker build -t user-management-agent .
```

Run the Streamlit app in Docker:

```bash
docker run --rm -p 8501:8501 --env-file .env user-management-agent
```

The container starts Streamlit by default on `0.0.0.0:8501`. If you want to run a CLI entry point instead, override the command when starting the container.

## Run

### LangGraph CLI

```bash
uv run python -m user_management_agent.langgraph_agent
```

### OpenAI Agents CLI

```bash
uv run python -m user_management_agent.openai_agent
```

### Streamlit app

```bash
uv run streamlit run app.py
```

### Compatibility wrappers

```bash
uv run python main.py
uv run python agent_openai.py
uv run python agent_langgrap.py
```

## How It Works

1. The user asks a question.
2. The agent connects to the MCP server defined by `MCP_SERVER_URL`.
3. The agent selects the best available MCP tool.
4. The tool result is returned in simple English.

The shared system prompt tells the agent to:

- always use MCP tools
- avoid making up user information
- choose the best tool automatically
- respond politely when no suitable tool exists

## Troubleshooting

- If you see `OPENAI_API_KEY environment variable is not set`, make sure your `.env` file is present and loaded.
- If the agent cannot connect to tools, verify `MCP_SERVER_URL` is correct and reachable.
- If Streamlit does not start, confirm `streamlit` is installed in the same environment created by `uv sync`.
- If Docker cannot reach the app, make sure port `8501` is published and the container was started with `--env-file .env`.

## Example

```text
You: Show all users older than 30
Assistant: ...
```
