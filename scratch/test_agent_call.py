
from agent import root_agent
import asyncio

async def test_agent():
    response = await root_agent.run_async(
        input={"text": "Hello, who are you?"},
        config={"userId": "test", "sessionId": "test-session"}
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(test_agent())
