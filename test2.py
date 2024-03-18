import discord

guilds = None
channels = {}


class Client(discord.Client):
    async def setup_hook(self):
        ...

    async def on_ready(self):
        global guilds
        print(f"Logged on as {self.user}!")
        guilds = [guild for guild in self.guilds]

        for guild in guilds:
            channels.update({guild: [channel for channel in guild.channels if isinstance(
                channel, discord.TextChannel)]})
        await self.close()

        #     self.channel = self.get_channel([(channel.name, channel.id)
        #                                      for channel in channels if isinstance(channel, TextChannel)])

    async def on_message(self, message):
        ...
