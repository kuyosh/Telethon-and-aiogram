from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

API_ID = 10953300
API_HASH = "9c24426e5d6fa1d441913e3906627f87"
SESSION_NAME = 'user_session'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def take_screenshot(url, save_path="screenshot.png"):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)
        driver.save_screenshot(save_path)
    finally:
        driver.quit()

@client.on(events.NewMessage(pattern=r'\.webscreen (.+)'))
async def webscreen_handler(event):
    try:
        url = event.pattern_match.group(1)
        save_path = "screenshot.png"
        await event.reply("⏳ Skreenshot olinmoqda, biroz kuting...")
        take_screenshot(url, save_path)
        await event.reply(file=save_path)
        os.remove(save_path)

    except Exception as e:
        await event.reply(f"❌ Xatolik yuz berdi: {str(e)}")

print("✅ Telegram foydalanuvchi hisobidan bot ishga tushdi...")
client.start()
client.run_until_disconnected()
