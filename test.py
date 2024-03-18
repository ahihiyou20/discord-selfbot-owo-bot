import threading
import asyncio
import test2

from nicegui import ui
from data2 import Data
from typing import Type
from re import search


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
                ui.navigate.to(new_account)
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


@ui.page("/new")
def new_account():
    data = {"token": None}
    channels = {}
    guilds = {}

    def create_data():
        data.update({"token": token.value})
        ui.notify(f"Token: {data['token']}", type='positive')

    def load_account(token: str) -> test2.Client:
        print(token)

        def runner():
            client = test2.Client()
            _loop = asyncio.new_event_loop()
            _thr = threading.Thread(target=_loop.run_forever,
                                    daemon=True)
            _thr.start()

            future = asyncio.run_coroutine_threadsafe(
                client.start(token), _loop)
            return future.result()

        runner()
        guilds, channels = test2.guilds, test2.channels

    with ui.stepper().props('vertical').classes('w-full') as stepper:
        with ui.step('First, Enter Your Token!'):
            token = ui.input(label='Token', password=True, password_toggle_button=True,
                             validation={'Not a valid Token!': lambda value: search(r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", value)})
            with ui.stepper_navigation():
                ui.button('Next', on_click=lambda: (
                    stepper.next, load_account(token.value)))
        with ui.step('Now, Choose Your Preferred Guild!'):
            ui.select(options=[guild.name for guild in guilds], with_input=True,
                      on_change=lambda e: ui.notify(e.value)).classes('w-40')
            with ui.stepper_navigation():
                ui.button('Next', on_click=stepper.next)
                ui.button('Back', on_click=stepper.previous).props('flat')
        with ui.step('Bake'):
            ui.label('Bake for 20 minutes')
            with ui.stepper_navigation():
                ui.button('Done', on_click=lambda: ui.notify(
                    'Yay!', type='positive'))
                ui.button('Back', on_click=stepper.previous).props('flat')

    ui.button("Save").on("click", lambda: create_data())


ui.run()
