import asyncio
from telethon import TelegramClient, events

from client import client
client = client.client

@events.register(events.NewMessage(pattern=r'^\.spam (\d+) (\d+)$'))
async def spam_command(event):
    args = event.pattern_match.groups()
    count = int(args[0])
    delay = int(args[1])
    if event.is_reply:
        replied_message = await event.get_reply_message()

        for i in range(count):
            await event.reply(file=replied_message.media, message=replied_message.text)
            await asyncio.sleep(delay)
    else:
        await event.respond("Iltimos, biror matn, rasm, video yoki faylga reply qilib .spam <count> <second> yozing.")

