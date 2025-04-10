import edge_tts
import asyncio

async def generate_speech(text, path):
    communicate = edge_tts.Communicate(text=text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(path)
