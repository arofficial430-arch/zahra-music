import os
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "ZahraMusic",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Me In Your Group", url=f"https://t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton("📚 Help And Commands", callback_data="help")],
        [
            InlineKeyboardButton("🛠️ Support", callback_data="support"),
            InlineKeyboardButton("🌐 Updates", callback_data="updates")
        ],
        [InlineKeyboardButton("👑 Owner", callback_data="owner")]
    ])

    await message.reply_text(
        "🎵 WELCOME TO ZAHRA MUSIC 🎵\n\n"
        "I am your Telegram Music Player Bot!\n\n"
        "🔥 Music Player\n"
        "❤️ Smooth Playback\n"
        "🎧 Group Voice Chat",
        reply_markup=buttons
    )

@app.on_callback_query()
async def callbacks(client, query):
    texts = {
        "help": "📚 ZAHRA MUSIC COMMANDS\n\n/play - Play music\n/pause - Pause music\n/resume - Resume music\n/skip - Skip music\n/stop - Stop music",
        "support": "🛠️ Contact support soon!",
        "updates": "🌐 ZAHRA MUSIC Updates coming soon!",
        "owner": "👑 ZAHRA MUSIC Owner"
    }

    await query.answer()
    await query.message.reply_text(
        texts.get(query.data, "Welcome to ZAHRA MUSIC!")
    )

print("ZAHRA MUSIC BOT IS STARTING...")
app.run()

