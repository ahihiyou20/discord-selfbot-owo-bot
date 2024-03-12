import asyncio
from twocaptcha import TwoCaptcha

from logger import logger
from oauth2 import get_oauth

solver = TwoCaptcha(**{
    'server':           "2captcha.com",
    'apiKey':           "210618b95e4f49c015d86c00fe3e65bf",
    'defaultTimeout':    300,
    'pollingInterval':   5,
})


def is_captcha(message, guild):
    if message.author.id == 408785106942164992:
        if message.guild and message.guild == guild:
            user = message.guild.me
            if (user in message.mentions) and ("a real human" in message.content):
                return True

    return False


async def solve_captcha(token):

    result = solver.hcaptcha(
        sitekey='a6a1d5ce-612d-472d-8e37-7601408fbc09',
        url="https://owobot.com/captcha",
    )

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US;en;q=0.8",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://owobot.com",
        "Referer": "https://owobot.com/captcha",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
    }

    async with (await get_oauth(token)) as session:
        cookies = {cookie.key: cookie.value for cookie in session.cookie_jar}

        async with session.post("https://owobot.com/api/captcha/verify",
                                headers=headers,
                                json={
                                    "token": result["code"]
                                },
                                cookies=cookies) as res:
            print(result["code"])
            print(res.status)

asyncio.run(
    solve_captcha("Token"))
