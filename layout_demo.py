import client

from nicegui import app, ui

from data2 import Data
from typing import Type
from re import search
from client import Client

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
                            ui.button(text="Select", icon="send").props(
                                "outline"
                            ).classes("").on("click", lambda: on_button(account))
    with ui.tab_panel("a"):
        with ui.element("div").classes("tab-panel-content"):
            ui.label("SETTINGS").classes("tab-panel-title")

    def on_button(account):
        global DATA
        ui.notify(f"Selected: {account}!")
        if account == "new":
            new_account()
        else:
            DATA = Data().load(account)


def new_account():
    token, channel, guild = None, None, None

    print("RUNNING")

    def create_data():
        data = {"token": token.value, "guild": guild.value, "channel": channel.value}
        ui.notify(str(data), type="positive")

    async def load_account(token: str) -> Client:
        print(token)
        client = Client(chunk_guilds_at_startup=False, request_guilds=False)
        await client.start(token)
        return client.guild_list, client.channel_list

    async def get_guild():
        if stepper.default_slot.children:
            nonlocal guild
            # guilds, channels = load_account(token.value)

            with stepper:
                with ui.step("Now, Choose Your Preferred Guild!") as step:
                    guilds, channels = await load_account(token.value)
                    guild = ui.select(
                        options=[guild.name for guild in guilds],
                        with_input=True,
                        on_change=lambda e: ui.notify(e.value),
                    )
                    with ui.stepper_navigation():
                        ui.button("Next", on_click=lambda: get_channel(channels))
                step.move(target_index=1)
        stepper.next()

    async def get_channel(channels: list):
        if stepper.default_slot.children:
            nonlocal channel
            stepper.next()
            with stepper:
                with ui.step("Finally, Choose Your Channel!") as step:
                    channel = ui.select(
                        options=[channel.name for channel in channels[guild.value]],
                        with_input=True,
                        on_change=lambda e: ui.notify(e.value),
                    )

                    with ui.stepper_navigation():
                        ui.button("Done", on_click=create_data)
                step.move(target_index=2)
        stepper.next()

    with ui.dialog(value=True):
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
                    ui.button("Next", on_click=get_guild)


ui.run()
