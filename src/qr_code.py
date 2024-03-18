import base64
import json
import threading
import time

import asyncio
import qrcode
import websocket
from aiohttp import ClientSession
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

DEBUG = False


class Messages:
    HEARTBEAT = 'heartbeat'
    HELLO = 'hello'
    INIT = 'init'
    NONCE_PROOF = 'nonce_proof'
    PENDING_REMOTE_INIT = 'pending_remote_init'
    PENDING_TICKET = 'pending_ticket'
    PENDING_LOGIN = 'pending_login'


class DiscordUser:
    def __init__(self, **values):
        self.id = values.get('id')
        self.username = values.get('username')
        self.discrim = values.get('discrim')
        self.avatar_hash = values.get('avatar_hash')
        self.token = values.get('token')

    @classmethod
    def from_payload(cls, payload):
        values = payload.split(':')

        return cls(id=values[0],
                   discrim=values[1],
                   avatar_hash=values[2],
                   username=values[3])


class DiscordAuthWebsocket:
    WS_ENDPOINT = 'wss://remote-auth-gateway.discord.gg/?v=2'
    LOGIN_ENDPOINT = 'https://discord.com/api/v9/users/@me/remote-auth/login'

    def __init__(self, debug=False):
        self.debug = debug
        self.ws = websocket.WebSocketApp(self.WS_ENDPOINT,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         header={'Origin': 'https://discord.com'})
        self.key = RSA.generate(2048)
        self.cipher = PKCS1_OAEP.new(self.key, hashAlgo=SHA256)

        self.heartbeat_interval = None
        self.last_heartbeat = None
        self.qr_image = None
        self.user = None

    @property
    def public_key(self):
        pub_key = self.key.publickey().export_key().decode('utf-8')
        pub_key = ''.join(pub_key.split('\n')[1:-1])
        return pub_key

    def heartbeat_sender(self):
        while True:
            time.sleep(0.5)  # we don't need perfect accuracy

            current_time = time.time()
            time_passed = current_time - self.last_heartbeat + \
                1  # add a second to be on the safe side
            if time_passed >= self.heartbeat_interval:
                try:
                    self.send(Messages.HEARTBEAT)
                except websocket.WebSocketConnectionClosedException:
                    return
                self.last_heartbeat = current_time

    def run(self):
        self.ws.run_forever()

    def send(self, op, data=None):
        payload = {'op': op}
        if data is not None:
            payload.update(**data)

        if self.debug:
            print(f'Send: {payload}')
        self.ws.send(json.dumps(payload))

    def exchange_ticket(self, ticket):
        print(f'Exch ticket: {ticket}')

        async def post():
            async with ClientSession() as session:
                async with session.post(self.LOGIN_ENDPOINT, json={'ticket': ticket}) as r:
                    if not r.status == 200:
                        print("HELLOOOOO")
                        print(r.status)
                        print(await r.json())
                return (await r.json()).get('encrypted_token')

        _loop = asyncio.new_event_loop()
        _thr = threading.Thread(target=_loop.run_forever,
                                daemon=True)
        _thr.start()

        future = asyncio.run_coroutine_threadsafe(post(), _loop)
        return future.result()

    def decrypt_payload(self, encrypted_payload):
        payload = base64.b64decode(encrypted_payload)
        decrypted = self.cipher.decrypt(payload)

        return decrypted

    def generate_qr_code(self, fingerprint):
        img = qrcode.make(f'https://discordapp.com/ra/{fingerprint}')
        self.qr_image = img

        img.show(title='Discord QR Code')

    def on_open(self, ws):
        pass

    def on_message(self, ws, message):
        if self.debug:
            print(f'Recv: {message}')

        data = json.loads(message)
        op = data.get('op')

        if op == Messages.HELLO:
            print('Attempting server handshake...')

            self.heartbeat_interval = data.get('heartbeat_interval') / 1000
            self.last_heartbeat = time.time()

            thread = threading.Thread(target=self.heartbeat_sender)
            thread.daemon = True
            thread.start()

            self.send(Messages.INIT, {'encoded_public_key': self.public_key})

        elif op == Messages.NONCE_PROOF:
            nonce = data.get('encrypted_nonce')
            decrypted_nonce = self.decrypt_payload(nonce)

            proof = SHA256.new(data=decrypted_nonce).digest()
            proof = base64.urlsafe_b64encode(proof)
            proof = proof.decode().rstrip('=')
            self.send(Messages.NONCE_PROOF, {'proof': proof})

        elif op == Messages.PENDING_REMOTE_INIT:
            fingerprint = data.get('fingerprint')
            self.generate_qr_code(fingerprint)

            print('Please scan the QR code to continue.')

        elif op == Messages.PENDING_TICKET:
            encrypted_payload = data.get('encrypted_user_payload')
            payload = self.decrypt_payload(encrypted_payload)

            self.user = DiscordUser.from_payload(payload.decode())

        elif op == Messages.PENDING_LOGIN:
            ticket = data.get('ticket')
            encrypted_token = self.exchange_ticket(ticket)
            token = self.decrypt_payload(encrypted_token)

            if self.qr_image is not None:
                self.qr_image.close()

            self.user.token = token.decode()
            self.ws.close()
            print(self.user.token)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, status_code, msg):
        print('----------------------')
        print(f'Connection closed: {msg}')


auth_ws = DiscordAuthWebsocket(debug=True)
auth_ws.run()
