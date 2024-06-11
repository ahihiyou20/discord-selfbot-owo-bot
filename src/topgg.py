from selenium_driverless import webdriver

from selenium.webdriver.common.by import By
from src.oauth2 import Oauth2
from src.logger import logger


class Topgg:
    """
    A Class To Vote for OwO Automatically on Top.gg
    """

    def __init__(self, token: str) -> None:
        """
        :param token: The account's token, required for oauth2
        """
        self.token: str = token
        self.authorize_link: str = (
            "https://discord.com/oauth2/authorize?scope=identify%20guilds%20email&redirect_uri=https%3A%2F%2Ftop.gg%2Flogin%2Fcallback&response_type=code&client_id=422087909634736160&state=Lw=="
        )

    @property
    def __chrome_options(self) -> webdriver.ChromeOptions:
        options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        options.headless = True
        return options

    async def __get_oauth(self) -> str:
        oauth: Oauth2 = Oauth2(self.token, self.authorize_link, is_topgg=True)
        oauth = await oauth.get_oauth()
        return oauth  # Link to top.gg/callback endpoint to login

    async def vote(self) -> None:
        """
        The Main Method to Vote

        """
        topgg: str = await self.__get_oauth()

        async with webdriver.Chrome(options=self.__chrome_options) as driver:
            await driver.maximize_window()  # Ensuring Buttons Are Found Correctly

            await driver.get(
                topgg, wait_load=True, timeout=10
            )  # Login at The Homepage or top.gg/callback

            logger.warning("Loaded Top.gg Homepage")
            await driver.sleep(5)  # Waiting for The Site to Fully Load

            button = await driver.find_element(
                by=By.XPATH, value='//a[@href="/bot/408785106942164992/vote"]'
            )  # Finding OwO's Vote Page Button

            await button.click(
                ensure_clickable=True
            )  # Click The Button to Get OwO's Vote Page

            logger.warning("Loaded OwO's Vote Page")
            await driver.sleep(10)

            button = await driver.find_element(
                by=By.XPATH, value=".//button[contains(text(),'Vote')]"
            )  # Look for Vote Button

            await button.click()  # Click The Vote Button

            logger.warning("Voted")
            await driver.sleep(3)
