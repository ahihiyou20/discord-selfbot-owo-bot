import discord


class Client(discord.Client):
    async def setup_hook(self):
        ...

    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        self.guild_list = [guild for guild in self.guilds]

        self.channel_list = {
            guild.name: [
                channel for channel in guild.channels
                if isinstance(
                    channel, discord.TextChannel)]
            for guild in self.guilds}

        await self.close()

    async def on_message(self, message):
        ...
