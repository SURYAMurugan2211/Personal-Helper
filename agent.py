from dotenv import load_dotenv
import os
os.environ["LIVEKIT_AGENTS_IPC_TIMEOUT"] = "600"
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from prompt import SESSION_INSTRUCTION, AGENT_INSTRUCTION
from livekit.plugins import (
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins import google
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                model="models/gemini-live-2.5-flash-preview",
                voice="Puck",
                temperature=0.8,
                api_key="AIzaSyBEXrD5URUyt3U55MtpLLBH8aPPJLttPJI",
            ),
        )


async def entrypoint(ctx: agents.JobContext):
    # Initialize Cartesia TTS
    tts = cartesia.TTS(api_key="sk_car_Ghdkt71W5J69P3UrkPisYF")

    # 🔧 Increase connection timeout (default ~10s, now 30s)
    tts._pool._connect_timeout = 30

    # Use the customized TTS instance in your session
    session = AgentSession(
        tts=tts,
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
