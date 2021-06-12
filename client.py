from typing import Optional

from aiohttp import ClientSession


class WebClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None

    def get_session(self) -> ClientSession:
        if self.session is None:
            self.session = ClientSession()
        return self.session

    def client(self):
        return self.session

    def shutdown(self):
        self.session.close()

    async def get(self, url: str, headers: dict = None) -> dict:
        async with self.get_session().get(url, headers=headers) as response:
            return await response.json()
