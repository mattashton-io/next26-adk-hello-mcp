# Hello MCP - Local Testing Guide

This project demonstrates a simple integration of the Model Context Protocol (MCP) with an AI Agent using the Google ADK (Agent Development Kit).

This guide walks you through running both the **MCP Server** and the **AI Agent (Client)** locally for testing.

---

## Prerequisites

1.  **Python 3.13+** installed.
2.  **Environment Variables**: Ensure you have a `.env` file with your `GEMINI_API_KEY` configured (if required by the `google-adk` or Gemini models).
    ```bash
    GEMINI_API_KEY=your_actual_api_key_here
    ```

3.  **Dependencies**: Install the required packages. It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

---

## Step 1: Run the MCP Server

Open a terminal window, activate your virtual environment, and start the MCP server.

```bash
# Terminal 1
python3 mcp_server.py
```

*   **Default Port**: The server will start on `http://0.0.0.0:8080`.
*   **HTTP Endpoint**: The server exposes HTTP at `/mcp`.

Keep this terminal running.

---

## Step 2: Run the AI Agent (Web App)

Open a **second terminal window**, activate your virtual environment, and start the Flask web application.

```bash
# Terminal 2

# (Optional) If your server is running on a non-default port:
# export MCP_SERVER_URL=http://localhost:8080/mcp

python3 app.py
```

*   **Web UI**: The Flask application will start on `http://0.0.0.0:5001` (or the port specified in your environment).

---

## Step 3: Verify the Integration

1.  Open your browser and navigate to `http://localhost:5001`.
2.  Type a message in the chat interface testing the MCP tool, for example:
    > "Can you get a greeting for Alice using the MCP server?"
3.  **Observation**:
    *   The Agent should recognize the request.
    *   It will invoke the `call_mcp_greeting` tool (referencing `mcp_client.py`).
    *   The `mcp_client` will connect to `http://localhost:8080/mcp`, trigger the tool on the server, and return the response.
    *   The Agent will output something like: `Hello, Alice! This greeting is sent from the remote MCP Server.`

---

## Troubleshooting

*   **Connection Errors**: Ensure `mcp_server.py` is running *before* you send a message from the Agent. By default, the client assumes `http://localhost:8080/mcp`. If you change the server port, you must set the `MCP_SERVER_URL` environment variable for the agent.
*   **Port Conflicts**: If port 8080 or 5001 is in use, use the `PORT` environment variable to change it (e.g., `PORT=8081 python3 mcp_server.py`).
