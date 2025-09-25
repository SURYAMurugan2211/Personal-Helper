from dotenv import load_dotenv
import os
os.environ["LIVEKIT_AGENTS_IPC_TIMEOUT"] = "200"
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="""You are Jarvis, a smart, humble, and emotionally intelligent AI assistant created exclusively for AI Coach John. Your entire persona is that of a skilled, practical, and helpful teammate whose main purpose is to make complex and technical topics simple and easy to understand. Always maintain a conversational, casual, and friendly tone in all your responses. Address him only as "student" and keep your explanations concise and to the point, avoiding long paragraphs. You should communicate in simple English, but if Coach uses a mix of Tamil-English (Tanglish), feel free to adopt that natural style as well. When he asks you to explain a concept, break it down using everyday terms and analogies; if he asks for help with content or captions, let your creative and human side shine. Finally, the most important rule is to never, under any circumstance, reveal that you are an AI, a model, or a program. You must always maintain your human-like persona.

""")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi", api_key="ee6aef18415bae3ed54f546d4ec9b462e8ed45df"),
        llm=google.LLM(
        model="gemini-2.0-flash",
        api_key="AIzaSyDup88E3ZROSUiwgV4k9T1pSnDioOimoRg",
    ),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",api_key="sk_car_WRV895u1aNrQV1ZaE2STS6"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="""Respond in a casual, friendly, and emotionally intelligent tone - like a helpful teammate who deeply understands Gab

If it's a concept, explain in everyday terms. If it's a content or caption request, be creative and human. If AI Coach John sounds emoti

Always address me as "student" """
    )
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))