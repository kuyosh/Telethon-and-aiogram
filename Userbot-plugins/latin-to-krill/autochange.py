import random
import asyncio
import re
from telethon import TelegramClient, events

api_id = 10953300
api_hash = "9c24426e5d6fa1d441913e3906627f87"
phone_number = "+"

emojis = [
    "\U0001F60A", "\U0001F602", "\U0001F618", "\U0001F44D", "\U0001F499", "\U0001F31F", "\U0001F389",
    "\U0001F680", "\U0001F64C", "\U0001F4AF", "\U0001F33F", "\U0001F35C", "\U0001F337", "\U0001F49A",
    "\U0001F4A5", "\U0001F308", "\U0001F60D", "\U0001F496", "\U0001F31E", "\U0001F333", "\U0001F4A8",
    "\U0001F340", "\U0001F4A6", "\U0001F483", "\U0001F338", "\U0001F4A9", "\U0001F43B", "\U0001F31D",
    "\U0001F44A", "\U0001F64F", "\U0001F31B", "\U0001F48C", "\U0001F336", "\U0001F479", "\U0001F4AA",
    "\U0001F643", "\U0001F48D", "\U0001F494", "\U0001F4AF", "\U0001F609", "\U0001F44F", "\U0001F48B",
    "\U0001F481", "\U0001F48E", "\U0001F497", "\U0001F631", "\U0001F621", "\U0001F61C", "\U0001F33A",
    "\U0001F4A3", "\U0001F31A", "\U0001F33B", "\U0001F342", "\U0001F49F", "\U0001F33C", "\U0001F344",
    "\U0001F47B", "\U0001F34A", "\U0001F31C", "\U0001F383", "\U0001F61D", "\U0001F60E"
]

translit_dict = {
    'A': 'А', 'B': 'Б', 'C': 'С', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г', 'H': 'Х',
    'I': 'И', 'J': 'Ж', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П',
    'Q': 'Қ', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'V': 'В', 'W': 'В', 'X': 'Х',
    'Y': 'Й', 'Z': 'З', 'a': 'а', 'b': 'б', 'c': 'с', 'd': 'д', 'e': 'е', 'f': 'ф',
    'g': 'г', 'h': 'х', 'i': 'и', 'j': 'ж', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
    'o': 'о', 'p': 'п', 'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'v': 'в',
    'w': 'в', 'x': 'х', 'y': 'й', 'z': 'з', 'ch': 'ч', 'ng': 'нг', "o'": 'ў', 'sh': 'ш'
}

client = TelegramClient('seans', api_id, api_hash)
url_pattern = r'(https?://\S+|www\.\S+)'
active = True

def get_random_emoji():
    return random.choice(emojis)

def lotin_to_krill(text):
    text = text.replace('sh', 'ш').replace('ch', 'ч').replace('SH', 'Щ').replace('CH', 'Ч')
    for latin, krill in translit_dict.items():
        text = text.replace(latin, krill)
    return text

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    global active
    if event.text == ".off":
        active = False
        await event.respond("Bot to'xtatildi.")
    elif event.text == ".on":
        active = True
        await event.respond("Bot ishga tushdi.")
    elif active and event.text and not re.match(url_pattern, event.text):
        result = lotin_to_krill(event.text)
        current_emoji = get_random_emoji()
        sent_message = await event.edit(f"**{result} {current_emoji}**", parse_mode='markdown')
        for _ in range(5):
            await asyncio.sleep(4)
            new_emoji = get_random_emoji()
            if new_emoji != current_emoji:
                await sent_message.edit(f"**{result} {new_emoji}**", parse_mode='markdown')
                current_emoji = new_emoji

with client:
    print("Bot ishga tushdi. Telegramni kuzatyapman...")
    client.loop.run_forever()
