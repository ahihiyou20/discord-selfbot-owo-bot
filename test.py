import asyncio
import threading

from nicegui import ui
from data2 import Data
from typing import Type
from re import search
from client import Client

DARK: ui.dark_mode = ui.dark_mode()
DATA: Type["Data"] = None


with ui.tabs().classes('w-50') as tabs:
    home = ui.tab('Home', icon="r_home")
    settings = ui.tab("Settings", icon="r_settings")
    settings.visible = False

with ui.tab_panels(tabs, value=home).classes("w-full"):
    with ui.tab_panel(home) as tab:
        ui.label('Select Account').classes('text-h4')

        def on_button(account):
            global DATA
            ui.notify(f"Selected: {account}!")
            if account == "new":
                new_account()
            else:
                DATA = Data().load(account)

            settings.visible = True

        for account in Data.get_account():
            with ui.card().tight().classes("width-100% max-width-300px"):

                ui.label(account).classes('text-h6')
                with ui.card_section():
                    ui.button("Select").classes(
                        "rounded-full w-20 h-10 ml-4").on("click", lambda: on_button(account))

    with ui.tab_panel(settings) as tab:

        switch = ui.switch("Dark Mode", on_change=lambda: ui.notify(
            "Setting Applied!", type='positive'))

        switch.bind_value_to(DARK, "value")


def new_account():
    token, channel, guild = None, None, None

    print("RUNNING")

    def create_data():
        data = {"token": token.value,
                "guild": guild.value,
                "channel": channel.value}
        ui.notify(str(data), type='positive')

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
                with ui.step('Now, Choose Your Preferred Guild!') as step:
                    guilds, channels = await load_account(token.value)
                    guild = ui.select(options=[guild.name for guild in guilds], with_input=True,
                                      on_change=lambda e: ui.notify(e.value))
                    with ui.stepper_navigation():
                        ui.button(
                            'Next', on_click=lambda: get_channel(channels))
                step.move(target_index=1)
        stepper.next()

    async def get_channel(channels: list):
        if stepper.default_slot.children:
            nonlocal channel
            stepper.next()
            with stepper:
                with ui.step('Finally, Choose Your Channel!') as step:
                    channel = ui.select(options=[channel.name for channel in channels[guild.value]], with_input=True,
                                        on_change=lambda e: ui.notify(e.value))

                    with ui.stepper_navigation():
                        ui.button("Done", on_click=create_data)
                step.move(target_index=2)
        stepper.next()

    with ui.dialog(value=True):
        with ui.stepper().props('vertical').classes('w-full') as stepper:
            with ui.step('First, Enter Your Token!'):
                token = ui.input(label='Token', password=True, password_toggle_button=True,
                                 validation={'Not a valid Token!': lambda value: search(r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", value)})
                with ui.stepper_navigation():
                    ui.button('Next', on_click=get_guild)


ui.run()
