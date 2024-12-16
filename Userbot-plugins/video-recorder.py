import pyautogui
import cv2
import numpy as np
import time
from telethon import TelegramClient, events
#hevorix
def record_screen(duration):
    screen_size = pyautogui.size()
    
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    output = cv2.VideoWriter("output.avi", fourcc, 20.0, screen_size)

    start_time = time.time()
    print("Videoga olish boshlandi...")

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            break

        img = pyautogui.screenshot()

        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        output.write(frame)

    output.release()
    print("Videoga olish tugadi. Foydalanuvchi fayl saqlandi: output.avi")

from client import client
client = client.client

@events.register(events.NewMessage(pattern=r"\.record\s+(-s|-m|-h)\s+(\d+)\s+@([\w_]+)"))
async def recorderuz(event):
    try:
        duration_type = event.pattern_match.group(1)  
        duration_value = int(event.pattern_match.group(2)) 
        username = event.pattern_match.group(3)  
        if duration_type == "-s":
            if not (1 <= duration_value <= 60):
                await event.reply("Iltimos, 1 dan 60 soniyagacha qiymat kiriting!")
                return
            duration = duration_value
        elif duration_type == "-m":
            if not (1 <= duration_value <= 60):
                await event.reply("Iltimos, 1 dan 60 daqiqagacha qiymat kiriting!")
                return
            duration = duration_value * 60
        elif duration_type == "-h":
            if not (1 <= duration_value <= 24):
                await event.reply("Iltimos, 1 dan 24 soatgacha qiymat kiriting!")
                return
            duration = duration_value * 3600
        else:
            await event.reply("Noto'g'ri buyruq formati. Iltimos, .record -s|-m|-h <raqam> <@username> formatida yuboring.")
            return

        await event.reply(f"{duration} soniya davomida ekranni videoga olish boshlandi...")
        record_screen(duration)

        await client.send_file(f"@{username}", "output.avi", caption="Videoga olish tugadi.")
        await event.reply(f"Videoga olish tugadi va @{username} ga yuborildi.")

    except Exception as e:
        await event.reply(f"Xatolik yuz berdi: {str(e)}")
