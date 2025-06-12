from option1_mono_agent.agent import SentientAgent
import uuid, asyncio

async def main():
    agent = SentientAgent(llm=None)  # replace with real LLM later
    await agent.answer_remaining(user_id=str(uuid.uuid4()), traits={})
if __name__ == "__main__":
    asyncio.run(main())
