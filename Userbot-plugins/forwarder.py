from telethon import TelegramClient, events
import asyncio
from telethon.errors import FloodWaitError, RPCError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from datetime import datetime

API_ID = 10953300
API_HASH = "9c24426e5d6fa1d441913e3906627f87"

client = TelegramClient('session_name', API_ID, API_HASH)

DELAY_BETWEEN_MESSAGES = 2

DELAY_BY_MEDIA = {
    'text': 1,
    'photo': 2,
    'document': 2,
}

class ForwardBot:
    def __init__(self, client, delay):
        self.client = client
        self.delay = delay

    async def forward_messages(self, source, target, max_messages=None):
        print(f"Starting to forward messages from {source} to {target}...")
        try:
            count = 0
            start_time = datetime.now()
            async for message in self.client.iter_messages(source):
                if max_messages is not None and count >= max_messages:
                    break

                await self.client.forward_messages(target, message)

                message_type = self._get_message_type(message)

                await asyncio.sleep(DELAY_BY_MEDIA.get(message_type, self.delay))

                count += 1

                if count % 5 == 0:
                    print("⏳ Large number of messages sent, waiting for 5 seconds...")
                    await asyncio.sleep(5)

                self._show_progress(count, start_time)

            print(f"All messages from {source} have been forwarded to {target}!")
        except FloodWaitError as e:
            print(f"FloodWaitError: Need to wait for {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
            await self.forward_messages(source, target, max_messages)
        except RPCError as e:
            print(f"Network or other RPC error occurred: {e}")
            await asyncio.sleep(10)
            await self.forward_messages(source, target, max_messages)
        except Exception as e:
            print(f"An error occurred: {e}")

    def _get_message_type(self, message):
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                return 'photo'
            elif isinstance(message.media, MessageMediaDocument):
                return 'document'
        return 'text'

    def _show_progress(self, count, start_time):
        elapsed_time = datetime.now() - start_time
        elapsed_seconds = elapsed_time.total_seconds()
        if elapsed_seconds > 0:
            rate = count / elapsed_seconds
            print(f"🔄 {count} messages sent, rate: {rate:.2f} messages/second")
#by #hevorix
    async def parse_handler(self, event):
        try:
            target_username = event.pattern_match.group(1)
            source_chat = await event.get_chat()
            source_id = source_chat.id

            max_messages = None

            await event.reply(f"📤 Forwarding messages from this group/channel to {target_username}...")
            await self.forward_messages(source_id, target_username, max_messages)
            await event.reply("✅ All messages have been forwarded!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

if __name__ == '__main__':
    print("Bot is running. You can send commands!")
    forward_bot = ForwardBot(client, DELAY_BETWEEN_MESSAGES)

    @client.on(events.NewMessage(pattern=r'^\.parse (@\w+)( \d+)?$'))
    async def handler(event):
        await forward_bot.parse_handler(event)

    with client:
        client.run_until_disconnected()
