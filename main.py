
import os
import asyncio

# FFmpeg setup
import imageio_ffmpeg
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_link = os.path.abspath("ffmpeg")

if not os.path.exists(ffmpeg_link):
    os.symlink(ffmpeg_exe, ffmpeg_link)

os.environ["PATH"] = os.path.dirname(ffmpeg_link) + os.pathsep + os.environ.get("PATH", "")

from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from yt_dlp import YoutubeDL

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
        "/play Song Name - Search and Play\n"
        "/pause - Pause\n"
        "/resume - Resume\n"
        "/stop - Stop"
    )

@bot.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage: /play Song Name"
        )

    query = message.text.split(maxsplit=1)[1]
    status = await message.reply_text("🔎 Searching YouTube...")

    try:
        def search_song():
            options = {
                "format": "bestaudio/best",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True
            }
            with YoutubeDL(options) as ydl:
                result = ydl.extract_info(
                    "scsearch1:" + query,
                    download=False
                )
                return result["entries"][0]

        song = await asyncio.to_thread(search_song)
        stream_url = song["url"]
        title = song.get("title", query)

        await calls.play(
            message.chat.id,
            MediaStream(
                stream_url,
                video_flags=MediaStream.Flags.IGNORE
            )
        )

        await status.edit_text(
            f"🎵 Now Playing:\n{title}"
        )

    except Exception as e:
        await status.edit_text(f"Play Error: {e}")

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
    async with bot:
        async with assistant:
            calls = PyTgCalls(assistant)
            await calls.start()

            print("ZAHRA MUSIC BOT STARTED!")

            await idle()

            await calls.stop()


if __name__ == "__main__":
    asyncio.run(main())

