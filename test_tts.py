import asyncio
import edge_tts

async def test():
    text = "Hello Saipadma. This is a test of Edge text to speech."
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )
    await communicate.save("test.mp3")
    print("✅ test.mp3 created successfully")

asyncio.run(test())
import asyncio
import edge_tts

async def test():
    text = "Hello Saipadma. This is a test of Edge text to speech."
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )
    await communicate.save("test.mp3")
    print("✅ test.mp3 created successfully")

asyncio.run(test())
