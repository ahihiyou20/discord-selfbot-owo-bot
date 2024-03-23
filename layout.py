from nicegui import app, ui
from discord.errors import LoginFailure

from data2 import Data
from typing import Type
from re import search
from client import Client
from asyncio import sleep

DATA: Type["Data"] = None

app.add_static_files("/static", "static")

ui.add_head_html(
    """ 
                    <link rel='stylesheet' type="text/css" href="/static/style.css">
                   
                    <link href="https://fonts.cdnfonts.com/css/minecraft-4" rel="stylesheet">
                    
                    <link
                      rel="stylesheet"
                      href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
                      
                     
  />
                 """
)


def on_button(account):
    global DATA
    if account == "new":
        new_account()
    else:
        DATA = Data().load(account)


with ui.tabs().classes("main-tabs") as tabs:
    with ui.element("div").classes("tabs-box animate__animated  animate__bounceIn"):
        ui.tab("h", label="Home", icon="home").classes("tab-item")
        ui.tab("a", label="Settings", icon="settings").classes("tab-item")

with ui.tab_panels(tabs, value="h").classes("w-full"):
    with ui.tab_panel("h") as tab:
        with ui.element("div").classes("tab-panel-content"):
            ui.label("SELECT ACCOUNT").classes("tab-panel-title")

        with ui.element("div").classes("cards-layout"):
            for account in Data.get_account():
                with ui.card():
                    with ui.element("div"):
                        ui.label(account)
                        with ui.card_section():
                            ui.button(text="Select", icon="send", on_click=lambda account=account: on_button(account)).props(
                                "outline"
                            ).classes("")

    with ui.tab_panel("a"):
        with ui.element("div").classes("tab-panel-content"):
            ui.label("SETTINGS").classes("tab-panel-title")


def new_account():
    token, channel, guild, gem, pray, exp, url, ping, ping_self, commands, daily, sell, solve = (
        None,) * 13

    def create_data():
        data = {"token": token.value,
                "guild": guild.value,
                "channel": channel.value,
                "gem": gem.value,
                "pray": pray.value,
                "exp": exp.value,
                "webhook": {
                    "url": url.value,
                    "ping": [ping.value, ping_self.value] if ping_self.value else [ping.value]
                },
                "commands": commands.value,
                "daily": daily.value,
                "sell": sell.value if (not sell.value) or (not "All" in sell.value) else "All",
                "solve": solve.value}

        ui.notify(str(data), type="positive")

    async def load_account(token: str) -> Client:
        print(token)

        if not search(r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", token):
            raise LoginFailure

        ui.notify("Logging In...", type="info")
        client = Client(chunk_guilds_at_startup=False,
                        request_guilds=False)
        await client.start(token)
        return client.guild_list, client.channel_list

    async def get_guild(button):
        if stepper.default_slot.children:
            nonlocal guild

            button.disable()
            try:
                guilds, channels = await load_account(token.value)
            except LoginFailure:
                ui.notify("Invalid Token!", type="negative")
                dialog.classes("animate__animated animate__shakeX")
                button.enable()
                await sleep(1)
                dialog.classes(remove="animate__animated animate__shakeX")
                return

            with stepper:
                with ui.step("Now, Choose Your Preferred Guild!") as step:
                    guild = ui.select(
                        options=[guild.name for guild in guilds],
                        with_input=True,
                        on_change=lambda e: ui.notify(e.value),
                    )
                    with ui.stepper_navigation():
                        ui.button(
                            "Next", on_click=lambda: get_channel(channels))
                step.move(target_index=1)
        stepper.next()

    async def get_channel(channels: list):
        if stepper.default_slot.children:
            nonlocal channel
            with stepper:
                with ui.step("Finally, Choose Your Channel!") as step:
                    channel = ui.select(
                        options=[
                            channel.name for channel in channels[guild.value]],
                        with_input=True,
                        on_change=lambda e: ui.notify(e.value),
                    )

                    with ui.stepper_navigation():
                        ui.button("Done", on_click=get_features)
                step.move(target_index=2)
        stepper.next()

    async def get_features():
        nonlocal gem, pray, exp, daily, solve, commands, sell, url, ping, ping_self
        if stepper.default_slot.children:
            with stepper:
                with ui.step("Select Features!") as step:
                    with ui.stepper_navigation():
                        with ui.card().classes("w-full"):
                            gem = ui.checkbox('Use Gems Automatically')
                            pray = ui.checkbox("Pray Automatically")
                            exp = ui.checkbox(
                                "Send Messages To Level Up Automatically")
                            daily = ui.checkbox("Claim Daily Automatically")
                            solve = ui.checkbox("Enable Captcha Solving")
                            with ui.expansion('Webhook', icon='settings_applications').classes('w-full'):
                                checkbox = ui.checkbox('Enable Webhook')

                                url = ui.input(
                                    "Webhook URL", password=True, password_toggle_button=True).bind_visibility_from(checkbox, 'value')

                                ping = ui.input(
                                    "USER ID To Ping", validation={"Invalid ID": lambda value: value.isnumeric() and len(value) > 15}
                                ).bind_visibility_from(checkbox, 'value')

                                ping_self = ui.checkbox(
                                    "Ping YourSelf Too?").bind_visibility_from(checkbox, 'value')

                            with ui.expansion('Selfbot Commands', icon='settings_applications').classes('w-full'):
                                checkbox = ui.checkbox(
                                    'Enable Selfbot Commands')

                                commands = ui.input(
                                    "Enter Selfbot Prefix",
                                    validation={
                                        "Prefix Is Too Long Don't You Think?": lambda value: len(value) < 5}
                                ).bind_visibility_from(checkbox, 'value')

                            with ui.expansion('Sell Animals', icon='settings_applications').classes('w-full'):
                                checkbox = ui.checkbox(
                                    'Enable Selling Animals')

                                sell = ui.select([
                                    "Common", "Uncommon", "Rare", "Epic", "Mythical", "Gem", "Legendary", "Fabled", "All"],
                                    multiple=True, validation={
                                        "You Should Only Select \"All\" Alone": lambda value:
                                            (len(value) < 8 and not "All" in value) or (
                                                len(value) == 1 and "All" in value),
                                        "Please Pick Animal Type(s) To Sell": lambda value: len(value) > 0
                                }).bind_visibility_from(checkbox, 'value').props('use-chips')

                            ui.button("Done!", on_click=create_data
                                      )
                step.move(target_index=3)
        stepper.next()

    with ui.dialog(value=True) as dialog:
        with ui.stepper().props("vertical").classes("w-full") as stepper:
            with ui.step("First, Enter Your Token!"):
                token = ui.input(
                    label="Token",
                    password=True,
                    password_toggle_button=True,
                    validation={
                        "Not a valid Token!": lambda value: search(
                            r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", value
                        )
                    },
                )
                with ui.stepper_navigation():
                    ui.button("Next!", icon="login",
                              on_click=lambda e: get_guild(e.sender))


ui.run(title="OwO Selfbot", favicon="favicon.ico")
