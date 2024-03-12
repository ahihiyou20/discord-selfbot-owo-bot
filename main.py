import discord
import asyncio

from src.logger import logger
from src.data import data
from src.misc import logo
from src.captcha_handler import is_captcha

logo(clear=True)

NEW_ACCOUNT = data.check_data()


class Client(discord.Client):
    async def setup_hook(self):
        ...

    async def on_ready(self):
        data.setup(self, NEW_ACCOUNT)
        logger.info(f"Logged on as {self.user}!")
        print(data.guild)

    async def on_message(self, message):
        if is_captcha(message, data.guild):
            logger.warning("Captcha Found, Stopping Tasks...")
   #     ...


async def main():
    global NEW_ACCOUNT

    if NEW_ACCOUNT:
        data.get_token()
    else:
        account = data.get_account()
        if account == "add":
            data.get_token()
            NEW_ACCOUNT = True
        else:
            data.load(account)

    client = Client()
    await client.start(data.token)

try:
    asyncio.run(main())
except asyncio.exceptions.CancelledError:
    logger.warning("Stopped")
