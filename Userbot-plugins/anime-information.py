from telethon import TelegramClient, events
import requests
from io import BytesIO
import tempfile
#hevorix
api_id = 10953300
api_hash = '9c24426e5d6fa1d441913e3906627f87'
client = TelegramClient('user_session', api_id, api_hash)

def get_anime_info_and_image(anime_name):
    try:
        response = requests.get(f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1")
        data = response.json()
        
        if data['data']:
            anime = data['data'][0]
            title = anime['title']
            description = anime['synopsis']
            episodes = anime['episodes']
            score = anime['score']
            url = anime['url']
            image_url = anime['images']['jpg']['large_image_url']
            
            image_response = requests.get(image_url)
            image = BytesIO(image_response.content)
            
            anime_info = f"**Title:** {title}\n"
            anime_info += f"**Score:** {score}\n"
            anime_info += f"**Episodes:** {episodes}\n"
            anime_info += f"**Description:** {description}\n"
            anime_info += f"**More Info:** [Link]({url})"
            
            return anime_info, image
        else:
            return "Anime topilmadi. Iltimos, nomini tekshirib qayta urinib ko'ring.", None
    
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}", None

@client.on(events.NewMessage(pattern='.anime (.*)'))
async def anime_info(event):
    anime_name = event.pattern_match.group(1)
    
    anime_details, anime_image = get_anime_info_and_image(anime_name)
    
    if anime_image:
        if len(anime_details) > 1024:
            anime_details = anime_details[:1021] + "..."

        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(anime_image.getvalue())
            tmp_file.close()

            await event.client.send_file(event.chat_id, tmp_file.name, caption=anime_details, parse_mode='markdown')
    else:
        await event.reply(anime_details)

client.start()
client.run_until_disconnected()
