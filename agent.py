import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# Get MCP_SERVER_URL from environment
# For Cloud Run deployment, this should be set to <YOUR_MCP_SERVER_URL>/mcp
mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")

# Configure McpToolset to connect to the remote server using Streamable HTTP
mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=mcp_url,
        headers={"Accept": "application/json, text/event-stream"}
    )
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions. You have access to remote tools via MCP.',
    instruction='Answer user questions to the best of your knowledge. If a user asks for a greeting, invoke the get_greeting tool.',
    tools=[mcp_toolset]
)
