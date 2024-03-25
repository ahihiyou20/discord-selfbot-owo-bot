import discord
from discord.ext import tasks

from src.logger import logger


class TempClient(discord.Client):
    async def on_ready(self):
        await self.close()


class Client(discord.Client):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.owoid = 408785106942164992

    async def setup_hook(self) -> None:
        ...

    async def on_ready(self) -> None:
        logger.warning(f"Logged in as {self.user}")

    async def runner(self, state: bool) -> None:
        tasks = [

        ]

        for task in tasks:
            if state:
                try:
                    task.start()
                except RuntimeError:
                    continue
            else:
                task.cancel()

    @tasks.loop(seconds=20)
    async def hunt_battle(self):
        logger.warning("supposed to run here")
