import discord


class Client(discord.Client):
    async def setup_hook(self):
        ...

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

        # self.channels = {channel.guild: channel for channel in self.get_all_channels()
        #                  if channel.permissions_for(self.user).send_messages}

        await self.close()

    async def on_message(self, message):
        ...
