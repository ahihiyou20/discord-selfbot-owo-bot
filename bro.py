import requests
from bro2 import RemoteAuthClient
import os
import event_emitter as events
import asyncio

client = RemoteAuthClient()

em = events.EventEmitter()

@events.on(emitter=em, event='pending_remote_init')
def pending_remote_init(fingerprint):
    data = f"https://discordapp.com/ra/{fingerprint}"
    qr_code_url = f"https://kissapi-qrcode.vercel.app/api/qrcode?chs=250x250&chl={data}"
    qr_code_response = requests.get(qr_code_url)
    with open('code.png', 'wb') as qr_code_file:
        qr_code_file.write(qr_code_response.content)
    print('Scan ./code.png')

@events.on(emitter=em, event='pending_finish')
def pending_finish(user):
    os.remove('code.png')
    print('Incoming User:', user)

@events.on(emitter=em, event='finish')
def finish(token):
    print('Token:', token)

@events.on(emitter=em, event='close')
def close():
    if os.path.exists('code.png'):
        os.remove('code.png')

async def main():
    await client.connect()

asyncio.run(main())