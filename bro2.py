import asyncio

import base64

import json

import time

import hashlib

import requests

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

from aiohttp import ClientSession, ClientSession

import event_emitter as events





COMMON_FETCH = {

  'headers': {

    'accept-language': 'en-US,en;q=0.8',

    'cache-control': 'no-cache',

    'Content-Type': 'application/json',

    'pragma': 'no-cache',

    'referer': 'https://discord.com/login',

    'sec-fetch-dest': 'empty',

    'sec-fetch-mode': 'cors',

    'sec-fetch-site': 'same-origin',

    'sec-gpc': 1,

    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

  },

  'referrer': 'https://discord.com/login',

}





class RemoteAuthClient(events.EventEmitter):

  def __init__(self):

    super().__init__()

    self.debug = True

    self.intervals = []

    self.key_pair = rsa.generate_private_key(

      public_exponent=65537, key_size=2048

    )

    self.canceled = False

    self._ping = None

    self._last_heartbeat = None

    self._pending_captcha = None

  async def emit(self, event, *args, **kwargs):
    await super().emit(event, *args, **kwargs)

  async def on_close(self, *args, **kwargs):
    # Handle events or logic when the WebSocket connection closes
    print("WebSocket connection closed")  # Example placeholder

  async def connect(self):

    async with ClientSession() as session:

      async with session.ws_connect('wss://remote-auth-gateway.discord.gg/?v=2', headers={'Origin': 'https://discord.com'}) as ws:

        self.ws = ws

        self.ws.on_message = self.on_message

        self.ws.on_close = self.on_close



        # Initiate communication and start heartbeats

        await self.ws.receive()

        self.intervals.append(

          asyncio.create_task(self.send_heartbeat_task(5000))
        )




  async def disconnect(self):

    if self.ws:

      await self.ws.close()

      for task in self.intervals:

        task.cancel()



  async def send(self, data):

    data_str = json.dumps(data)

    if self.debug:

      print(f"[RemoteAuthClient] -> {data_str}")

    await self.ws.send_text(data_str)



  async def send_heartbeat(self):

    self._last_heartbeat = time.time()

    await self.send({"op": "heartbeat"})



  async def send_heartbeat_task(self, interval):

    while True:

      await asyncio.sleep(interval)

      if self.canceled:

        break

      await self.send_heartbeat()



  async def decrypt_payload(self, payload):

    return await self.key_pair.private_key().decrypt(

      payload,

      encryption_algorithm=rsa.PKCS1v15(mgf=hashes.SHA256()),

      padding_algorithm=PKCS1v15(padding=base64.b64decode(payload))

    )



  async def on_message(self, message):

    if self.debug:

      print(f"[RemoteAuthClient] <- {message}")

    try:

      p = json.loads(message)

      await self.on_message_handler(p)

    except Exception as error:

      if self.debug:

        print(f"[RemoteAuthClient] Error: {error}")

      else:

        raise error



  async def on_message_handler(self, payload):

    op = payload['op']

    if op == 'hello':

      encoded_public_key = await self.key_pair.public_key().export(

        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo

      )

      await self.send({

        "op": "init",

         "encoded_public_key": encoded_public_key.decode('utf-8'),

      })

    elif op == 'nonce_proof':

            decrypted_nonce = await self.decrypt_payload(payload['encrypted_nonce'])

            nonce_hash = hashlib.sha256(decrypted_nonce)

            await self.send({

                "op": "nonce_proof",

                "proof": nonce_hash.digest().replace(b'=', b'').replace(b'+', b'-').replace(b'/', b'_')

            })

    elif op == 'pending_remote_init':

           self.emit('pendingRemoteInit', payload['fingerprint'])

    elif op == 'pending_ticket':
           decrypted_user = await self.decrypt_payload(payload['encrypted_user_payload'])
           user_data = decrypted_user.decode().split(':')
           self.emit('pendingFinish', {

               'id': user_data[0],

               'discriminator': user_data[1],

               'avatar': user_data[2],

               'username': user_data[3]

           })

    elif op == 'pending_login':
           headers = {**COMMON_FETCH['headers']}

           if self._pending_captcha and self._pending_captcha['service'] == 'hcaptcha':
               headers['x-captcha-key'] = self._pending_captcha['data']['key']

               headers['x-captcha-rqtoken'] = self._pending_captcha['data']['rqtoken']



           try:

               async with ClientSession() as session:

                   async with session.post('https://discord.com/api/v9/users/@me/remote-auth/login', json={'ticket': payload['ticket']}, headers=headers) as response:

                       data = await response.json()

                       if response.status == 200:

                           self._pending_captcha = None

                           decrypted_token = await self.decrypt_payload(data['encrypted_token']).decode()

                           self.emit('finish', decrypted_token)

                       elif response.status == 400 and data.get('captcha_key') and data['captcha_key'][0] in ['captcha-required', 'invalid-response']:

                           captcha_service = data['captcha_service']

                           if captcha_service == 'hcaptcha':

                               if self._pending_captcha:

                                   self._pending_captcha['data']['key'] = None

                                   self._pending_captcha['retries'] += 1

                                   self._pending_captcha['data']['rqtoken'] = data['captcha_rqtoken']

                               else:

                                   self._pending_captcha = {

                                       'ticket': payload['ticket'],

                                       'service': 'hcaptcha',

                                       'retries': 0,

                                       'data': {

                                           'key': None,

                                           'rqtoken': data['captcha_rqtoken'],

                                       }

                                   }

                               self.emit('hcaptcha', {

                                   'sitekey': data['captcha_sitekey'],

                                   'rqdata': data['captcha_rqdata'],

                                   'pageurl': 'https://discord.com/login',

                                   'userAgent': COMMON_FETCH['headers']['user-agent'],

                                   'retries': self._pending_captcha['retries'],

                               })

                           else:

                               raise Exception(f'Unknown captcha service: "{captcha_service}"')

                       else:

                           raise Exception(f'Unexpected response status: {response.status}')

           except Exception as e:

               if self.debug:

                   print(f"[RemoteAuthClient] Error: {e}")

               self.emit('error', e)

    elif op == 'cancel':

           self.canceled = True

           self.emit('cancel')

    elif op == 'heartbeat_ack':

           self._ping = time.time() - self._last_heartbeat
           self.emit('raw', payload)

  def solve_captcha(self, key):  # Method for solving CAPTCHA (not provided)

        # Implement a secure way to obtain and utilize a CAPTCHA solution

        # This method is omitted due to ethical considerations.

        raise NotImplementedError("CAPTCHA handling not implemented")

