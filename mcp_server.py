import os
import uvicorn
from fastmcp import FastMCP

# Create a simple FastMCP server
mcp = FastMCP("HelloServer")

@mcp.tool()
def get_greeting(name: str) -> str:
    """Get a personalized greeting from the Model Context Protocol Server."""
    return f"Hello, {name}! This greeting is sent from the remote MCP Server."

if __name__ == "__main__":
    # For Cloud Run, default to 8080 or use the PORT env var
    port = int(os.environ.get("PORT", "8080"))
    # Run the MCP server over HTTP
    mcp.run(transport='http', host="0.0.0.0", port=port)
