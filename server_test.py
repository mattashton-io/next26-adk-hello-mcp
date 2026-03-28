import httpx
import json

# URL of the MCP server
url = "https://mcp-server-396631018769.us-central1.run.app/mcp"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 1. Test listing tools (Standard MCP JSON-RPC)
list_tools_payload = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "listTools",
    "params": {}
}

# 2. Test calling a tool (Standard MCP JSON-RPC)
call_tool_payload = {
    "jsonrpc": "2.0",
    "id": "2",
    "method": "callTool",
    "params": {
        "name": "get_greeting",
        "arguments": {"name": "TestUser"}
    }
}

def run_test(name, payload):
    print(f"\n--- Running Test: {name} ---")
    try:
        response = httpx.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        except json.JSONDecodeError:
            print("Response Text (Not JSON):")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

def run_get_test(name, path=""):
    test_url = url + path
    print(f"\n--- Running GET Test: {name} (URL: {test_url}) ---")
    try:
        # Use stream to read SSE if it's an SSE stream
        with httpx.stream("GET", test_url, headers={"Accept": "text/event-stream"}) as response:
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            # Read first few bytes or lines
            count = 0
            for line in response.iter_lines():
                if line:
                    print(f"SSE Data: {line}")
                    count += 1
                if count >= 3: # Just get a few lines
                    break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 1. Try GET to root /
    # Correctly parse the root url
    root_url = "https://mcp-server-396631018769.us-central1.run.app"
    print(f"\n--- Running GET Test: GET root / (URL: {root_url}) ---")
    try:
        with httpx.stream("GET", root_url, headers={"Accept": "text/event-stream"}) as response:
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            count = 0
            for line in response.iter_lines():
                if line:
                    print(f"SSE Data: {line}")
                    count += 1
                if count >= 3:
                    break
    except Exception as e:
        print(f"Error: {e}")

    # 2. Try GET to /mcp
    run_get_test("GET /mcp")
    
    # Restore original POST tests
    run_test("List Tools", list_tools_payload)
