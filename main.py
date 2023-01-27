import discord
import aiohttp
import logging
import asyncio

from logging.config import dictConfig
from os import path
from discord.ext import tasks
from discord import Webhook, AsyncWebhookAdapter
from json import load
from random import randrange
from re import findall
from datetime import timedelta
from time import time
from base64 import b64encode


class CustomFormatter(logging.Formatter):
    """A Custom Formatter Class For Logging"""

    GREY = "\x1b[38;5;240m"
    YELLOW = "\x1b[0;33m"
    CYAN = "\x1b[1;94m"
    RED = "\x1b[1;31m"
    BRIGHT_RED = "\x1b[1;41m"
    RESET = "\x1b[0m"
    FORMAT = "\x1b[0;43m%(asctime)s\x1b[0m - {}%(levelname)s{} - %(message)s"

    FORMATS = {
        logging.DEBUG: FORMAT.format(GREY, RESET) + "(%(filename)s:%(lineno)d)",
        logging.INFO: FORMAT.format(CYAN, RESET),
        logging.WARNING: FORMAT.format(YELLOW, RESET),
        logging.ERROR: FORMAT.format(RED, RESET) + "(%(filename)s:%(lineno)d)",
        logging.CRITICAL: FORMAT.format(BRIGHT_RED, RESET)
        + "(%(filename)s:%(lineno)d)",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%d %b %Y %H:%M:%S")
        return formatter.format(record)


class Data:
    """A Class Which Load The Data From "config.json" or From Specified Path"""

    def __init__(self):
        self.CONFIG_PATH = (
            "conf.json"
            if path.exists("conf.json")
            else input("Enter Path To Your Config File: ")
        )
        self.loader()

    def loader(self):
        with open(self.CONFIG_PATH, "r") as file:
            data = load(file)
            self.token = data["token"]
            self.channel = data["channel"]
            self.gm = data["gm"]
            self.pm = data["pm"]
            self.em = data["em"]
            self.sm = data["sm"]
            self.sbcommands = data["sbcommands"]
            self.webhook = data["webhook"]
            self.daily = data["daily"]
            self.sell = data["sell"]
            self.solve = data["solve"]


class Gems:
    def __init__(self):
        self.available = [1, 3, 4]
        self.gemtypes = [1, 3, 4]
        self.regex = r"gem(\d):\d+>`\[(\d+)"

    async def use_gems(self, target=[1, 3, 4]):
        for index, value in enumerate(target):
            if value == 1:
                target[index] = 0
            elif value == 3:
                target[index] = 1
            else:
                target[index] = 2

        await self.channel.trigger_typing()
        await asyncio.sleep(3)
        await self.channel.send("owo inv")
        logger.info("Using Gems...")
        await asyncio.sleep(3)
        async for message in self.channel.history(limit=15):
            if message.author == self.get_user(self.owo) and (
                await self.message_includes(message, "Inventory", True)
            ):
                inv = findall(r"`(.*?)`", message.content)
                break

        if not inv:
            logger.error("Couldn't Fetch Inventory Due To Unexpected Reason")
            return

        if "050" in inv:
            await self.channel.send("owo lootbox all")
            logger.info("Opened All Lootboxes")
            await asyncio.sleep(3)
            self.available = [1, 3, 4]
            await self.use_gems(target)

        inv = [
            item
            for item in inv
            if item.isdigit() and int(item) < 100 and int(item) > 50
        ]
        tier = [[], [], []]
        logger.info(f"Found {len(inv)} Gem(s)")
        for gem in inv:
            gem = int(gem)
            if 50 < gem < 58:
                tier[0].append(gem)
            elif 64 < gem < 72:
                tier[1].append(gem)
            elif 71 < gem < 79:
                tier[2].append(gem)
        self.available = []
        if tier[0]:
            self.available.append(1)
        if tier[1]:
            self.available.append(3)
        if tier[2]:
            self.available.append(4)
        use = []

        for level in target:
            if len(tier[level]) > 0:
                use.append(str(max(tier[level])))

        if use:
            await asyncio.sleep(3)
            await self.channel.send(f"owo use {' '.join(use)}")
            logger.info(f"Used Gem(s): {' '.join(use)}")
            return
        logger.warning("You Don't Have Any Available Gems")

    async def detect_gems(self, message):
        if not (await self.message_includes(message, "**🌱", True)):
            return

        current_gems = [
            gem for gem in findall(self.regex, message.content) if not gem[1] == "0"
        ]
        use = [1, 3, 4]
        if len(current_gems) == 3:
            return

        for gem in current_gems:
            use.remove(int(gem[0]))

        use = [gem for gem in use if gem in self.available]

        if use:
            await self.use_gems(use)


class CaptchaSolver:
    def __init__(self):
        self.api = "https://autofarmsupport.tk"
        self.retries = 0

    async def __solve(self, image, length):
        data = {"data": image, "len": length, "id": str(self.user.id)}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api, json=data, timeout=300) as resp:
                if resp.ok:
                    return await resp.json()
                return False

    async def __report(self, captcha_id, is_correct):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api + "/report",
                json={"captchaId": captcha_id, "correct": is_correct},
                timeout=120,
            ):
                return

    async def solver(self, message):
        try:
            await self.runner(False)
            logger.info("Solving Captcha...")
            captcha_image = b64encode(await message.attachments[0].read()).decode(
                "utf-8"
            )
            resp = await self.__solve(
                captcha_image,
                message.content[message.content.find("letter word") - 2],
            )
            if resp:
                logger.debug(resp)
                logger.info(f"Solved Captcha [Code: {resp['code']}]")
                await self.get_user(self.owo).send(resp["code"])
                await asyncio.sleep(10)
                message = (
                    await self.get_user(self.owo).dm_channel.history(limit=1).flatten()
                )[0]
                if (
                    message.author == self.get_user(self.owo)
                    and "verified" in message.content
                ):
                    await self.__report(resp["captchaId"], "True")
                    await self.runner(True)
                    return True
                logger.critical("Selfbot Stopped Since The Captcha Code Is Wrong")
                await self.__report(resp["captchaId"], "False")
            return False
        except Exception as e:
            logger.critical(str(e))
            await self.close()


class Client(discord.Client, Data, Gems, CaptchaSolver):
    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, *args, **kwargs)
        Data.__init__(self)
        Gems.__init__(self)
        CaptchaSolver.__init__(self)

        self.total_cmds = 0
        self.next_daily = 0
        self.owo = 408785106942164992

    async def ask_for_confirmation(self, channel):
        await channel.send(
            "Confirm (YES/NO)? Send Answer Into The Channel (Timeout: 5s)"
        )
        try:
            confirm = await self.wait_for(
                "message",
                check=lambda message: message.author == self.user
                and message.content.lower() in ["yes", "y"],
                timeout=5.0,
            )
        except asyncio.TimeoutError:
            await channel.send("Cancelled")
            return False
        return confirm

    async def message_includes(self, message, content, includes_self=False):
        if includes_self:
            return (
                content.lower() in message.content.lower()
                and self.user.name in message.content
            )
        return content.lower() in message.content.lower()

    async def get_balance(self):
        await self.channel.send("owo cash")
        await asyncio.sleep(3)
        async for message in self.channel.history(limit=15):
            if message.author == self.get_user(self.owo) and (
                await self.message_includes(message, "currently", True)
            ):
                content = message.content
                return int(
                    "".join(findall("[0-9]+", content[content.find("have") : :]))
                )
        return 0

    async def runner(self, mode, ignore=[]):
        tasks = [
            self.main,
            self.pray,
            self.exp,
            self.claim_daily,
            self.sell_animal,
            self.presence,
            self.sleeper,
        ]

        for task in tasks:
            if task in ignore:
                continue
            if mode:
                task.start()
                await asyncio.sleep(2)
                continue
            task.cancel()

    async def on_ready(self):
        self.channel = (
            self.get_channel(self.channel)
            if type(self.channel) is int
            else self.channel
        )
        self.start_balance = await self.get_balance()

        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------" * 5)
        if not self.presence.is_running() or not self.main.is_running():
            await self.runner(True)

    async def on_message(self, message):
        if message.author == self.get_user(self.owo):
            if await self.message_includes(message, "⚠", True):
                if self.webhook["link"]:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(
                            self.webhook["link"],
                            adapter=AsyncWebhookAdapter(session),
                        )
                        await webhook.send(
                            f"<@{self.webhook['ping']}> Verification Found!"
                        )
                if client.solve:
                    if message.attachments:
                        if await self.solver(message):
                            return
                    else:
                        async for message in self.channel.history(limit=15):
                            if (
                                message.author == self.get_user(self.owo)
                                and "captcha" in message.content
                                and message.attachments
                            ):
                                if await self.solver(message):
                                    return
                                break
                logger.critical("Detected Verification!")
                await self.close()
            await self.detect_gems(message)

        if not self.sbcommands["enable"]:
            return

        if message.author.id not in (
            self.user.id,
            self.sbcommands["allowed_id"],
        ):
            return

        if message.content.startswith(f"{self.sbcommands['prefix']}pr"):
            confirm = await self.ask_for_confirmation(message.channel)
            if not confirm:
                return

            if self.runner.is_running():
                self.runner(False)
                logger.info("Paused")
                return await confirm.reply("Paused!")
            self.runner.start()
            logger.info("Resumed")
            return await confirm.reply("Resumed!")

        if message.content.startswith(f"{self.sbcommands['prefix']}stop"):
            confirm = await self.ask_for_confirmation(message.channel)
            if not confirm:
                return

            await confirm.reply("Stopped!")
            logger.info("Stopped")
            await self.close()

    @tasks.loop(seconds=60)
    async def presence(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                application_id=1053928905288986684,
                type=discord.ActivityType.playing,
                name="Statistics (Update Every Minute)",
                state=f"Hunt/Battle: {self.total_cmds} times",
                details=f"Gained {(await self.get_balance()) - self.start_balance:,} Cowoncies",
                timestamps={"start": time() - (60 * self.presence.current_loop)},
                assets={
                    "large_image": "1059027556671705098",
                    "large_text": "OwO Self-bot",
                    "small_image": "1059360660204564510",
                    "small_text": "Made By ahihiyou20",
                },
            ),
        )

    @tasks.loop(seconds=randrange(14, 19))
    async def main(self):
        await self.channel.trigger_typing()
        await self.channel.send("owo hunt")
        logger.info('Sent "owo hunt"')
        self.total_cmds += 1
        await asyncio.sleep(3)

        await self.channel.send("owo battle")
        logger.info('Sent "owo battle"')
        self.total_cmds += 1

    @tasks.loop(minutes=4)
    async def pray(self):
        await self.channel.trigger_typing()
        await self.channel.send("owo pray")
        logger.info('Sent "owo pray"')
        await asyncio.sleep(randrange(4, 9))

    @tasks.loop(seconds=30)
    async def exp(self):
        if self.em["text"]:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get("http://api.quotable.io/random") as resp:
                    text = (await resp.json())["content"] if resp.ok else None

            if text:
                await self.channel.trigger_typing()
                await self.channel.send(text)
                logger.info("Sent Random Text For EXP")
                await asyncio.sleep(3)

        if self.em["owo"]:
            await self.channel.trigger_typing()
            await self.channel.send("owo")
            logger.info('Sent "owo"')
        await asyncio.sleep(randrange(4, 9))

    @tasks.loop(seconds=30)
    async def claim_daily(self):
        if not self.next_daily - time() <= 0:
            return

        await self.channel.trigger_typing()
        await asyncio.sleep(3)
        await self.channel.send("owo daily")
        logger.info("Claiming Daily...")
        await asyncio.sleep(3)
        target_message = None
        async for message in self.channel.history(limit=15):
            if message.author == self.get_user(self.owo) and (
                await self.message_includes(message, "your daily", True)
                or await self.message_includes(message, "Nu")
            ):
                target_message = message
                break
        if not target_message:
            logger.error("Couldn't Claim Daily Due To Unexpected Reason")
            return
        if "Nu" in target_message.content:
            next_daily = findall("[0-9]+", target_message.content)
            next_daily = [int(time) for time in next_daily]
            next_daily = next_daily[0] * 3600 + next_daily[1] * 60 + next_daily[2]
            self.next_daily = time() + next_daily
            logger.info(f"Next Daily: {str(timedelta(seconds=next_daily))}s")
        elif "Your next daily" in target_message.content:
            logger.info("Claimed Daily!")
        await asyncio.sleep(randrange(4, 9))

    @tasks.loop(minutes=2)
    async def sell_animal(self):
        await self.channel.trigger_typing()
        await asyncio.sleep(5)
        await self.channel.send(f"owo sell {self.sell['types']}")
        logger.info(f"Sold ({self.sell['types']}) Available Animal")

    @tasks.loop(minutes=10)
    async def sleeper(self):
        if self.sleeper.current_loop == 0:
            return
        tasks = [
            self.main,
            self.pray,
            self.exp,
            self.claim_daily,
            self.sell_animal,
            self.presence,
        ]
        interval_before = [task.seconds for task in tasks]

        for task in tasks:
            task.change_interval(seconds=360)

        logger.warning("Sleeping...")
        await asyncio.sleep(randrange(180, 360))

        for index, task in enumerate(tasks):
            task.change_interval(seconds=interval_before[index])

    @presence.before_loop
    async def before_presence(self):
        await self.wait_until_ready()

    @main.before_loop
    async def before_main(self):
        await self.wait_until_ready()

    @pray.before_loop
    async def before_pray(self):
        if not self.pm:
            self.pray.cancel()
        await self.wait_until_ready()

    @exp.before_loop
    async def before_exp(self):
        if not self.em["text"] and not self.em["owo"]:
            self.exp.cancel()
        await self.wait_until_ready()

    @claim_daily.before_loop
    async def before_claim_daily(self):
        if not self.daily:
            self.claim_daily.cancel()
        await self.wait_until_ready()

    @sell_animal.before_loop
    async def before_sell_animal(self):
        if not self.sell["enable"]:
            self.sell_animal.cancel()
        await self.wait_until_ready()

    @sleeper.before_loop
    async def before_sleeper(self):
        if not self.sm:
            self.sleeper.cancel()
        await self.wait_until_ready()


dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

logging.warning("Loading... Please be patient!")
client = Client(guild_subscription_options=discord.GuildSubscriptionOptions.off())

try:
    client.run(client.token)
except (RuntimeError, KeyboardInterrupt):
    pass
