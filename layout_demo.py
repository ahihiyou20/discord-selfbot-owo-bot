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
                    <link rel='stylesheet' type="text/css" href="/static/styles.css">
                   
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
            ui.navigate.to(new_account)
        else:
            DATA = Data().load(account)


ui.run()
