
import os
import asyncio
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
STRING_SESSION = os.environ["STRING_SESSION"]

bot = Client(
    "ZahraBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

assistant = Client(
    "ZahraAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

calls = PyTgCalls(assistant)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🎵 Welcome to ZAHRA MUSIC 🎵\n\n"
        "/play URL - Play audio\n"
        "/pause - Pause\n"
        "/resume - Resume\n"
        "/stop - Stop"
    )

@bot.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage: /play AUDIO_URL"
        )

    url = message.text.split(maxsplit=1)[1]

    try:
        await calls.play(message.chat.id, url)
        await message.reply_text("🎵 Playing in Voice Chat!")
    except Exception as e:
        await message.reply_text(f"Play Error: {e}")

@bot.on_message(filters.command("pause"))
async def pause(client, message):
    try:
        await calls.pause(message.chat.id)
        await message.reply_text("⏸ Paused")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@bot.on_message(filters.command("resume"))
async def resume(client, message):
    try:
        await calls.resume(message.chat.id)
        await message.reply_text("▶️ Resumed")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

@bot.on_message(filters.command("stop"))
async def stop(client, message):
    try:
        await calls.leave_call(message.chat.id)
        await message.reply_text("⏹ Stopped")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

async def main():
    await bot.start()
    await assistant.start()
    calls.start()
    print("ZAHRA MUSIC BOT STARTED!")
    await idle()
    calls.stop()
    await assistant.stop()
    await bot.stop()

asyncio.run(main())
