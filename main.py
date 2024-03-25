from nicegui import app, ui
from discord.errors import LoginFailure
from discord import TextChannel

from data2 import Data
from typing import Type
from re import search
from client import TempClient
from asyncio import sleep

DATA: Type["Data"] = Data()

app.add_static_files("/static", "static")

ui.add_head_html(
    """ 
                    <link rel='stylesheet' type="text/css" href="/static/styles.css">
                   
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Prompt:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
                    
                    <link
                      rel="stylesheet"
                      href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
                      
                     
  />
                 """
)


@ui.refreshable
def select_account():
    with ui.card():
        if DATA.name:
            ui.label(DATA.name)
            with ui.splitter() as splitter:
                with splitter.before:
                    ui.label("PLACE HOLDER")
                with splitter.after:
                    ui.label("PLACE HOLDER")
        else:
            ui.label("No Account Selected")


@ui.refreshable
def show_account():
    for account in Data.get_account():
        with ui.card():
            ui.label(account)
            with ui.card_section():
                ui.button(
                    text="Select",
                    icon="send",
                    on_click=lambda account=account: (
                        DATA.load(account), select_account.refresh(), ui.notify(
                            "Account Loaded!", type="positive")
                    ),
                ).props("outline")

                ui.button(text="Remove", icon="delete",
                          on_click=lambda account=account: (
                              DATA.remove(account),
                              show_account.refresh(),
                              ui.notify("Account Removed!", type="positive"))
                          ).props("outline")


with ui.tabs().classes("main-tabs") as tabs:
    with ui.element("div").classes("tabs-box animate__animated  animate__bounceIn"):
        ui.tab("h", label="Home", icon="home").classes("tab-item")
        ui.tab("a", label="Settings", icon="settings").classes("tab-item")

with ui.tab_panels(tabs, value="h").classes("w-full"):
    with ui.tab_panel("h") as tab:
        with ui.element("div").classes("tab-panel-content"):
            ui.label("SELECT ACCOUNT").classes("tab-panel-title")

        with ui.element("div").classes("cards-layout"):
            show_account()
            ui.button(icon="add", on_click=lambda: new_account()
                      ).classes("add-button")

        with ui.element("div").classes("tab-panel-content"):
            ui.label("ACCOUNT INFO").classes("tab-panel-title")

        with ui.element("div").classes("cards-layout"):
            select_account()

    with ui.tab_panel("a"):
        with ui.element("div").classes("tab-panel-content"):
            ui.label("SETTINGS").classes("tab-panel-title")


def new_account():
    (
        token,
        channel,
        guild,
        gem,
        pray,
        exp,
        url,
        ping,
        ping_self,
        commands,
        daily,
        sell,
        solve,
    ) = (None,) * 13

    def create_data(client: TempClient):
        global DATA

        data = {
            "token": token.value,
            "guild": guild.value,
            "channel": channel.value,
            "gem": gem.value,
            "pray": pray.value,
            "exp": exp.value,
            "webhook": {
                "url": url.value,
                "ping": (
                    [
                        int(ping.value) if ping.value else None,
                        client.user.id if ping_self.value else None,
                    ]
                    if (ping.value or ping_self.value)
                    else None
                ),
            },
            "commands": commands.value if commands.value else None,
            "daily": daily.value,
            "sell": (
                sell.value if (not sell.value) or (
                    not "All" in sell.value) else "All"
            ),
            "solve": solve.value,
        }

        ui.notify(str(data), type="positive")
        DATA = DATA.save(client.user.name, data)
        show_account.refresh()
        dialog.close()

    async def load_account(token: str) -> TempClient:
        print(token)

        if not search(r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", token):
            raise LoginFailure

        ui.notify("Logging In...", type="positive")
        client = TempClient(max_messages=None, guild_subscriptions=False)
        await client.start(token)

        return client

    async def get_guild(button):
        if stepper.default_slot.children:
            nonlocal guild

            button.disable()
            try:
                client = await load_account(token.value)

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
                        options={
                            guild.id: guild.name for guild in client.guilds},
                        with_input=True,
                        on_change=lambda e: ui.notify(e.value),
                    )
                    with ui.stepper_navigation():
                        ui.button("Next", on_click=lambda: get_channel(client)).props(
                            "outline"
                        )
                step.move(target_index=1)
        stepper.next()

    async def get_channel(client: TempClient):
        if stepper.default_slot.children:
            nonlocal channel
            with stepper:
                with ui.step("Finally, Choose Your Channel!") as step:
                    Guild = client.get_guild(guild.value)
                    channel = ui.select(
                        options={
                            channel.id: channel.name
                            for channel in Guild.channels
                            if isinstance(channel, TextChannel)
                            and channel.permissions_for(Guild.me).send_messages
                        },
                        with_input=True,
                        on_change=lambda e: ui.notify(e.value),
                    )

                    with ui.stepper_navigation():
                        ui.button("Next", on_click=lambda: get_features(client)).props(
                            "outline"
                        )
                step.move(target_index=2)
        stepper.next()

    async def get_features(client: TempClient):
        nonlocal gem, pray, exp, daily, solve, commands, sell, url, ping, ping_self
        if stepper.default_slot.children:
            with stepper:
                with ui.step("Select Features!") as step:
                    with ui.stepper_navigation():
                        with ui.card().classes("w-full q-card-features"):
                            gem = ui.checkbox("Use Gems Automatically")
                            pray = ui.checkbox("Pray Automatically")
                            exp = ui.checkbox(
                                "Send Messages To Level Up Automatically")
                            daily = ui.checkbox("Claim Daily Automatically")
                            solve = ui.checkbox("Enable Captcha Solving")
                            with ui.expansion(
                                "Webhook", icon="settings_applications"
                            ).classes("w-full"):
                                checkbox = ui.checkbox("Enable Webhook")

                                url = ui.input(
                                    "Webhook URL",
                                    password=True,
                                    password_toggle_button=True,
                                    validation={
                                        "Invalid Webhook URL": lambda value: value.startswith(
                                            "https://discord.com/api/webhooks"
                                        )
                                    },
                                ).bind_visibility_from(checkbox, "value")

                                ping = ui.input(
                                    "USER ID To Ping",
                                    validation={
                                        "Invalid ID": lambda value: value.isnumeric()
                                        and len(value) > 15
                                    },
                                ).bind_visibility_from(checkbox, "value")

                                ping_self = ui.checkbox(
                                    "Ping YourSelf Too?"
                                ).bind_visibility_from(checkbox, "value")

                            with ui.expansion(
                                "Selfbot Commands", icon="settings_applications"
                            ).classes("w-full"):
                                checkbox = ui.checkbox(
                                    "Enable Selfbot Commands")

                                commands = ui.input(
                                    "Enter Selfbot Prefix",
                                    validation={
                                        "Prefix Is Too Long Don't You Think?": lambda value: len(
                                            value
                                        )
                                        < 5
                                    },
                                ).bind_visibility_from(checkbox, "value")

                            with ui.expansion(
                                "Sell Animals", icon="settings_applications"
                            ).classes("w-full"):
                                checkbox = ui.checkbox(
                                    "Enable Selling Animals")

                                sell = (
                                    ui.select(
                                        [
                                            "Common",
                                            "Uncommon",
                                            "Rare",
                                            "Epic",
                                            "Mythical",
                                            "Gem",
                                            "Legendary",
                                            "Fabled",
                                            "All",
                                        ],
                                        multiple=True,
                                        validation={
                                            'You Should Only Select "All" Alone': lambda value: (
                                                len(value) < 8 and not "All" in value
                                            )
                                            or (len(value) == 1 and "All" in value),
                                            "Please Pick Animal Type(s) To Sell": lambda value: len(
                                                value
                                            )
                                            > 0,
                                        },
                                    )
                                    .bind_visibility_from(checkbox, "value")
                                    .props("use-chips")
                                )

                            ui.button(
                                "Done!", on_click=lambda: create_data(client)
                            ).props("outline")
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
                    ui.button(
                        "Next!", icon="login", on_click=lambda e: get_guild(e.sender)
                    ).props("outline")


ui.run(title="OwO Selfbot", favicon="favicon.ico")
