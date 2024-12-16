from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
import asyncio

api_id = 10953300
api_hash = '9c24426e5d6fa1d441913e3906627f87'
#hevorix
replygif_groups = set()

client = TelegramClient('replygif_bot', api_id, api_hash)

@client.on(events.NewMessage(pattern='^\.replygifon$'))
async def replygif_on(event):
    chat_id = event.chat_id
    if chat_id not in replygif_groups:
        replygif_groups.add(chat_id)
        await event.reply("✅ ReplyGIF funksiyasi yoqildi!")
    else:
        await event.reply("⚠️ ReplyGIF allaqachon yoqilgan.")

@client.on(events.NewMessage(pattern='^\.replygifoff$'))
async def replygif_off(event):
    chat_id = event.chat_id
    if chat_id in replygif_groups:
        replygif_groups.remove(chat_id)
        await event.reply("❌ ReplyGIF funksiyasi o'chirildi!")
    else:
        await event.reply("⚠️ ReplyGIF yoqilmagan.")

@client.on(events.NewMessage(pattern='^\.replygiflist$'))
async def replygif_list(event):
    if replygif_groups:
        group_list = '\n'.join([str(chat_id) for chat_id in replygif_groups])
        await event.reply(f"📋 ReplyGIF yoqilgan guruhlar:\n{group_list}")
    else:
        await event.reply("📋 ReplyGIF hech qaysi guruhda yoqilmagan.")

@client.on(events.NewMessage())
async def gif_reply(event):
    chat_id = event.chat_id
    if chat_id in replygif_groups and event.media:
        if isinstance(event.media, MessageMediaDocument) and event.file.mime_type in ['video/mp4', 'image/gif']:
            await event.reply("🤖 Videodagi yoki GIF'dagi narsa sizga o'xsharkan!")

print("Bot ishga tushdi... Press Ctrl+C to stop.")
client.start()
client.run_until_disconnected()
