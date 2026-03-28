
import os
import logging
import asyncio
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types

# Import the root agent
from agent import root_agent

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ADK services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

# Initialize the Runner
runner = Runner(
    app_name=os.getenv("APP_NAME", "hello_agent_app"),
    agent=root_agent,
    artifact_service=artifact_service,
    session_service=session_service,
)

# In-memory store for session IDs per user (simplified for demo)
user_sessions = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Helper to run async code in a sync Flask route
    try:
        return asyncio.run(_handle_chat(request.json))
    except Exception as e:
        logger.error(f"Error in chat route: {e}")
        return jsonify({"error": str(e)}), 500

async def _handle_chat(data):
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    user_id = data.get("user_id", "default_user")
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Get or create session for the user
    if user_id not in user_sessions:
        session = await session_service.create_session(
            app_name=os.getenv("APP_NAME", "hello_agent_app"),
            user_id=user_id,
        )
        user_sessions[user_id] = session.id
    
    session_id = user_sessions[user_id]

    try:
        content = types.Content(role="user", parts=[types.Part(text=message)])
        full_response = ""
        
        # Run the agent and collect events
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if hasattr(event, 'content') and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response += part.text

        return jsonify({
            "response": full_response,
            "user_id": user_id,
            "session_id": session_id
        })

    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug_mode = os.environ.get("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
