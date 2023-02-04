# Import Necessary Modules
import discord
import aiohttp
import logging
import asyncio

# Import Extra Modules
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

    # Escape Color Character
    GREY = "\x1b[38;5;240m"
    YELLOW = "\x1b[0;33m"
    CYAN = "\x1b[1;94m"
    RED = "\x1b[1;31m"
    BRIGHT_RED = "\x1b[1;41m"
    RESET = "\x1b[0m"
    FORMAT = "\x1b[0;43m%(asctime)s\x1b[0m - {}%(levelname)s{} - %(message)s"

    # Format Color For Each Level
    FORMATS = {
        logging.DEBUG: FORMAT.format(GREY, RESET) + "(%(filename)s:%(lineno)d)",
        logging.INFO: FORMAT.format(CYAN, RESET),
        logging.WARNING: FORMAT.format(YELLOW, RESET),
        logging.ERROR: FORMAT.format(RED, RESET) + "(%(filename)s:%(lineno)d)",
        logging.CRITICAL: FORMAT.format(BRIGHT_RED, RESET)
        + "(%(filename)s:%(lineno)d)",
    }

    def format(self, record):
        """
        Format Function (Method)
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%d %b %Y %H:%M:%S")
        return formatter.format(record)


class Data:
    """A Class Which Load The Data From "config.json" or From Specified Path"""

    def __init__(self):
        """
        Initialize And Fetch conf.json
        """
        self.CONFIG_PATH = (
            "conf.json"
            if path.exists("conf.json")
            else input("Enter Path To Your Config File: ")
        )
        self.loader()

    def loader(self):
        """
        Function (Method) Which Loads Data From conf.json
        """
        with open(self.CONFIG_PATH, "r") as file:
            data = load(file)
            self.token = data["token"]  # Account's Token (str)
            self.channel = data["channel"]  # Channel ID (int)
            self.gm = data["gm"]  # Automatically Uses Gems (bool)
            self.pm = data["pm"]  # Automatically Pray (bool)
            self.em = data[
                "em"
            ]  # Automatically Send Random Text or "owo" For EXP ( {"text": bool, "owo": bool} )
            self.sm = data[
                "sm"
            ]  # Pause for 3 Minute Every 5 Min To Reduce Chance Getting Verification (bool)
            self.sbcommands = data[
                "sbcommands"
            ]  # Data About Selfbot's Commands ( {"enable": bool, "prefix": str, "allowed_id": int})
            self.webhook = data[
                "webhook"
            ]  # Webhook's Data, Which Used To Send Warning If There's Verification ( {"link": str, "ping": int} )
            self.daily = data["daily"]  # Automatically Claim Daily (bool)
            self.sell = data[
                "sell"
            ]  # Automatically Sell Animals ( {"enable": bool, "types": str})
            self.solve = data[
                "solve"
            ]  # Automatically Solve Verification Using Captcha Solving API (bool)


class Gems:
    """
    A Class Which Can Be Used To Equip Gems Automatically
    """

    def __init__(self):
        """
        Intialize Some Attribute
        """
        self.available = [1, 3, 4]
        self.gemtypes = [1, 3, 4]
        self.regex = r"gem(\d):\d+>`\[(\d+)"

    async def use_gems(self, target=[1, 3, 4]):
        """
        A Function (Method) That Uses Requested Gems
        """

        # This One Is Hard To Explain But...
        # It Convert Gem(s)' Code Into Index Number 0,1,2
        for index, value in enumerate(target):
            match value:
                case 1:
                    target[index] = 0
                case 3:
                    target[index] = 1
                case 4:
                    target[index] = 2

        # Fetch The Inventory
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

        # Couldn't Fetch The Inventory
        if not inv:
            logger.error("Couldn't Fetch Inventory Due To Unexpected Reason")
            return

        # Use Lootbox(es) If Available
        if "050" in inv:
            await self.channel.send("owo lootbox all")
            logger.info("Opened All Lootboxes")
            await asyncio.sleep(3)
            self.available = [1, 3, 4]
            await self.use_gems(target)

        # Convert Raw Inventory To A List of Gem Code (Intenger)
        inv = [
            item
            for item in inv
            if item.isdigit() and int(item) < 100 and int(item) > 50
        ]
        logger.info(f"Found {len(inv)} Gem(s)")

        # Parse Gems Into Multiple Types
        types = [[], [], []]
        for gem in inv:
            gem = int(gem)
            if 50 < gem < 58:
                types[0].append(
                    gem
                )  # Hunting (Diamond) Gems, Which Increases Numbers of Animals Caught
            elif 64 < gem < 72:
                types[1].append(
                    gem
                )  # Empowering (Round) Gems, Which Doubles The Number of Animals caught
            elif 71 < gem < 79:
                types[2].append(
                    gem
                )  # Lucky (Heart) Gems, Which Increases The Chance of Finding Gem Animals

        # Update Available Gems
        self.available = []
        if types[0]:
            self.available.append(1)
        if types[1]:
            self.available.append(3)
        if types[2]:
            self.available.append(4)

        # Use The Requested Gems
        use = []
        for level in target:
            if types[level]:
                use.append(str(max(types[level])))

        # Send Command
        if use:
            await asyncio.sleep(3)
            await self.channel.send(f"owo use {' '.join(use)}")
            logger.info(f"Used Gem(s): {' '.join(use)}")
            return
        logger.warning("You Don't Have Any Available Gems")

    async def detect_gems(self, message):
        """
        This Function (Method) Is The Reason Why The Selfbot Knows When The Gems Run Out
        """

        # Fetch Only Hunt Messages
        if not (await self.message_includes(message, "**🌱", True)):
            return

        # Fetch Available Gems
        current_gems = [
            gem for gem in findall(self.regex, message.content) if not gem[1] == "0"
        ]

        # Check If Any Gem Is Not Available
        use = [1, 3, 4]
        if len(current_gems) == 3:
            return

        # Calculate The Gem Which Needs To Be Used
        for gem in current_gems:
            use.remove(int(gem[0]))

        use = [gem for gem in use if gem in self.available]
        if use:
            # Use The Gem If necessary
            await self.use_gems(use)


class CaptchaSolver:
    """
    This Class Solve Verification For You
    """

    def __init__(self):
        """
        Initialize Attributes
        """
        self.api = "https://autofarmsupport.tk"  # API's URL
        self.retries = 0  # Coming Soon

    async def __solve(self, image, length):
        """
        A Private Function (Method) Which Is Required To Send And Receive Verification's Result
        """
        data = {"data": image, "len": length, "id": str(self.user.id)}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api, json=data, timeout=300) as resp:
                if resp.ok:
                    return await resp.json()
                return False

    async def __report(self, captcha_id, is_correct):
        """
        A Private Function (Method) Which Is Required To Fetch And Report The Result To Increase The Accuracy
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api + "/report",
                json={"captchaId": captcha_id, "correct": is_correct},
                timeout=120,
            ):
                return

    async def solver(self, message):
        """
        A Function (Method) That Solves Verification
        """
        try:
            await self.runner(False)  # Stop Other Progress
            logger.info("Solving Captcha...")
            captcha_image = b64encode(await message.attachments[0].read()).decode(
                "utf-8"
            )  # Convert The Image Into Base64
            resp = await self.__solve(
                captcha_image,
                message.content[message.content.find("letter word") - 2],
            )  # Send Request To Solve The Captcha
            if resp:  # Success
                logger.debug(resp)
                # Send The Captcha And Continue Grinding
                logger.info(f"Solved Captcha [Code: {resp['code']}]")
                await self.get_user(self.owo).send(resp["code"])
                await asyncio.sleep(10)

                # Check If The Captcha Was True or Not
                message = (
                    await self.get_user(self.owo).dm_channel.history(limit=1).flatten()
                )[0]
                if (
                    message.author == self.get_user(self.owo)
                    and "verified" in message.content
                ):
                    await self.__report(
                        resp["captchaId"], "True"
                    )  # Report Correct If Yes
                    await self.runner(True)  # Continue Grinding If Correct
                    return True
                logger.critical(
                    "Selfbot Stopped Since The Captcha Code Is Wrong"
                )  # Otherwise Stop Immediately
                await self.__report(resp["captchaId"], "False")
            return False
        except Exception as e:
            logger.critical(
                str(e)
            )  # Make Sure That No Bug Happens (To Keep It Safe, Just Print Out The Issue And Stop)
            await self.close()


class Client(discord.Client, Data, Gems, CaptchaSolver):
    """
    The Main Client Class, Which Controls The Selfbot
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize Attributes And Methods From Inheritance
        """
        discord.Client.__init__(self, *args, **kwargs)
        Data.__init__(self)
        Gems.__init__(self)
        CaptchaSolver.__init__(self)

        self.total_cmds = 0
        self.next_daily = 0
        self.owo = 408785106942164992

    async def ask_for_confirmation(self, channel):
        """
        A Function (Method) Which Ask For Confirmation When Using Selfbot Commands
        """
        await channel.send(
            "Confirm (YES/NO)? Send Answer Into The Channel (Timeout: 5s)"
        )

        # Check For The Result
        try:
            confirm = await self.wait_for(
                "message",
                check=lambda message: message.author
                in [self.user, self.get_user(self.sbcommands["allowed_id"])]
                and message.content.lower() in ["yes", "y"],
                timeout=5.0,
            )
        except asyncio.TimeoutError:
            await channel.send("Cancelled")
            return False
        return confirm

    async def message_includes(self, message, content, includes_self=False):
        """
        A Function (Method) Which Checks If A Message Includes Something
        """
        if includes_self:
            return (
                content.lower() in message.content.lower()
                and self.user.name in message.content
            )
        return content.lower() in message.content.lower()

    async def get_balance(self):
        """
        A Function (Method) Which Fetch The Current Balance
        """
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
        return self.start_balance

    async def runner(self, mode, ignore=[]):
        """
        A Function (Method) Which Runs Tasks To Make The Selfbot Work
        """
        tasks = [
            self.main,
            self.pray,
            self.exp,
            self.claim_daily,
            self.sell_animal,
            self.presence,
            self.sleeper,
        ]

        try:
            for task in tasks:
                if task in ignore:
                    continue
                if mode:
                    task.start()
                    await asyncio.sleep(2)
                    continue
                task.cancel()
        except RuntimeError:
            return

    async def on_ready(self):
        """
        A Function (Method) Which Will Be Triggered On Ready
        """
        self.channel = (
            self.get_channel(self.channel)
            if type(self.channel) is int
            else self.channel
        )
        self.start_balance = await self.get_balance()

        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------" * 5)
        await self.runner(True)
        await self.runner(True)

    async def on_message(self, message):
        """
        A Function (Method) Which Will Be Triggered Everytime A Message Is Send From An User
        """

        # Check For Verification
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
            if self.gm:
                await self.detect_gems(message)

        # Selfbot Commands
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
        """
        A Function (Method) Which Initializes A Rich Presence And Display Infomation About The Selfbot (Update Every Minute)
        """
        await self.change_presence(
            status=discord.Status.dnd,
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
        """
        A Function (Method) That Sends Hunt/Battle
        """
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
        """
        A Function (Method) That Sends Pray
        """
        await self.channel.trigger_typing()
        await self.channel.send("owo pray")
        logger.info('Sent "owo pray"')
        await asyncio.sleep(randrange(4, 9))

    @tasks.loop(seconds=30)
    async def exp(self):
        """
        A Function (Method) Which Send Random Text or "owo" for EXP
        """
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
        """
        A Function (Method) Which Automatically Claim Daily
        """
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
        """
        A Function (Method) Which Sells Animal Automatically
        """
        await self.channel.trigger_typing()
        await asyncio.sleep(5)
        await self.channel.send(f"owo sell {self.sell['types']}")
        logger.info(f"Sold ({self.sell['types']}) Available Animal")

    @tasks.loop(minutes=5)
    async def sleeper(self):
        """
        A Function (Method) That Reduce Chance Getting Verification By Pausing The Bot For 3 Min Every 5 Min
        """

        # Skip The First 5 Minute
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

    # Functions (Methods) Which Will Be Ran Before It's Instance Run
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


# Disable discord.py-self's Logging
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

# Run The Selfbot
if __name__ == "__main__":
    logging.warning("Loading... Please be patient!")
    client = Client(guild_subscription_options=discord.GuildSubscriptionOptions.off())

    try:
        client.run(client.token)
    except (RuntimeError, KeyboardInterrupt):
        pass
