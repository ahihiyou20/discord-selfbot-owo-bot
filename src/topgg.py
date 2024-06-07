from selenium_driverless import webdriver
import asyncio

from selenium.webdriver.common.by import By
from src.oauth2 import Oauth2
from src.logger import logger


class Topgg:
    def __init__(self, token):
        self.token = token
        self.authorize_link = "https://discord.com/oauth2/authorize?scope=identify%20guilds%20email&redirect_uri=https%3A%2F%2Ftop.gg%2Flogin%2Fcallback&response_type=code&client_id=422087909634736160&state=Lw=="

    async def _get_oauth(self):
        oauth = Oauth2(self.token, self.authorize_link, is_topgg=True)
        oauth = await oauth.get_oauth()
        return oauth  # Link to top.gg/callback

    async def vote(self):
        options = webdriver.ChromeOptions()
        options.headless = True

        topgg = await self._get_oauth()
        async with webdriver.Chrome(options=options) as driver:
            await driver.get(topgg, wait_load=True, timeout=10)
            logger.warning("Loaded Top.gg Homepage")

            await asyncio.sleep(5)
          
            button = await driver.find_element(
                by=By.XPATH, value='//a[@href="/bot/408785106942164992/vote"]'
            )

            await button.click(ensure_clickable=True, scroll_to=True)
            logger.warning("Loaded OwO's Vote Page")

            await asyncio.sleep(10)
            button = await driver.find_element(
                by=By.XPATH, value=".//button[contains(text(),'Vote')]"
            )
            await button.click(ensure_clickable=True)
            logger.warning("Voted")
            await asyncio.sleep(3)
