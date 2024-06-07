from aiohttp import ClientSession, CookieJar

from src.logger import logger


class Oauth2:
    def __init__(self, token, oauth, is_topgg):
        self.token = token
        self.oauth_refer = oauth
        self.oauth_req = (
            oauth.split("/oauth2")[0] + "/api/v9/oauth2" + oauth.split("/oauth2")[1]
        )
        self.is_topgg = is_topgg

    async def __submit_oauth(self, res):
        response = await res.json()
        locauri = response.get("location")
        host = locauri.replace("https://", "").replace("http://", "").split("/")[0]

        if self.is_topgg:
            return locauri

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.5",
            "connection": "keep-alive",
            "host": host,
            "referer": "https://discord.com/",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        }
        logger.warning(locauri)

        session = ClientSession(cookie_jar=CookieJar())

        async with session.get(locauri, headers=headers, allow_redirects=False) as res2:
            if res2.status in (302, 307):
                logger.warning("(+) Token Added To OAuth")
                return session
            else:
                print(f"{str(res)}")
                return print(f"(-) Failed to add token to oauth | {res2.status}")

    async def get_oauth(self):
        async with ClientSession() as session:
            payload = {"permissions": "0", "authorize": True}

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "Authorization": self.token,
                "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExMS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTg3NTk5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
                "X-Debug-Options": "bugReporterEnabled",
                "Origin": "https://discord.com",
                "Connection": "keep-alive",
                "Referer": self.oauth_refer,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers",
            }

            async with session.post(
                self.oauth_req, headers=headers, json=payload
            ) as res:
                if res.status == 401:
                    print(f"(!) Invalid Token [{self.token[:25]}...]")
                elif res.status == 200:
                    result_session = await self.__submit_oauth(res)
                    logger.warning(result_session)
                    return result_session
                else:
                    print(f"(!) Error | {await res.text()}")
