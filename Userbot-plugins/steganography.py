from telethon import TelegramClient, events
from PIL import Image
import stepic
import io
#hevorix
api_id = 10953300
api_hash = "9c24426e5d6fa1d441913e3906627f87"

client = TelegramClient('user_session', api_id, api_hash)

@client.on(events.NewMessage(pattern='.steg (.*)'))
async def on_steg(event):
    text = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()

    if reply_message and reply_message.media:
        file = await client.download_media(reply_message)
        image = Image.open(file)
        encoded_image = stepic.encode(image, text.encode())

        with io.BytesIO() as output:
            encoded_image.save(output, format="PNG")
            output.seek(0)
            await client.send_file(event.chat_id, output, caption="Decoded Image", reply_to=reply_message)
    else:
        await event.reply("Iltimos, rasmga javob bering va .steg <matn> buyrug'ini yuboring.")

@client.on(events.NewMessage(pattern='.steg de'))
async def on_steg_de(event):
    reply_message = await event.get_reply_message()

    if reply_message and reply_message.media:
        file = await client.download_media(reply_message)
        image = Image.open(file)
        decoded_text = stepic.decode(image)
        
        if decoded_text:
            await event.reply(f"Yashirilgan matn: {decoded_text}")
        else:
            await event.reply("Rasmda hech qanday yashirilgan matn yo'q.")
    else:
        await event.reply("Iltimos, yashirilgan rasmga javob bering va .steg de buyrug'ini yuboring.")

client.start()
client.run_until_disconnected()
