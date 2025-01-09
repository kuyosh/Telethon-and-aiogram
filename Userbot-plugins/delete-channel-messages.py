from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from client import client
client = client.client
channel_username = '@tg_monitoring_test'


async def delete_all_messages():
    await client.start()
    channel = await client.get_entity(channel_username)
    async for message in client.iter_messages(channel):
        await message.delete()

    print("Barcha xabarlar o'chirildi.")

with client:
    client.loop.run_until_complete(delete_all_messages())
