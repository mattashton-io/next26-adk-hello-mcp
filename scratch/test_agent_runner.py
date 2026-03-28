
import os
import asyncio
from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

async def test_agent():
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    runner = Runner(
        app_name="hello_agent_test",
        agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )
    
    user_id = "test_user"
    session = await session_service.create_session(app_name="hello_agent_test", user_id=user_id)
    session_id = session.id
    
    content = types.Content(role="user", parts=[types.Part(text="Hello, who are you?")])
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if hasattr(event, 'content'):
            print("Response:", "".join([p.text for p in event.content.parts if p.text]))

if __name__ == "__main__":
    asyncio.run(test_agent())
