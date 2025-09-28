from dotenv import load_dotenv
import sounddevice as sd
print(sd.query_devices())
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
from livekit.plugins import cartesia
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
    llm=google.beta.realtime.RealtimeModel(
        voice="Aoede",
        api_key="AIzaSyB34JvZpY4K3ig8mZhqrCXL2xmts0Z9oL4",
    ),
    tts=cartesia.TTS(api_key="sk_car_WRV895u1aNrQV1ZaE2STS6"), 
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )
    await ctx.connect()

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))