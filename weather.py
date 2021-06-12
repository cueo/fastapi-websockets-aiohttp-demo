from pydantic import BaseModel

from client import WebClient


class Weather(BaseModel):
    city: str
    country: str
    temperature: float
    low: float
    high: float
    humidity: float
    pressure: float
    description: str


async def to_weather(response: dict) -> Weather:
    location: dict = response['location']
    forecast: dict = response['forecast']
    return Weather(
        city=location['city'],
        country=location['country'],
        temperature=forecast['temp'],
        low=forecast['low'],
        high=forecast['high'],
        humidity=forecast['humidity'],
        pressure=forecast['pressure'],
        description=response['weather']['description']
    )


class WeatherClient:
    def __init__(self, client: WebClient):
        self.base_url = 'https://weather.talkpython.fm/api/weather'
        self.client = client

    async def by_city(self, city: str, country: str) -> dict:
        url = f'{self.base_url}?city={city}&country={country}&units=metric'
        return await self.client.get(url)

    async def weather(self, data: dict) -> Weather:
        response = await self.by_city(data['city'], country=data['country'])
        return await to_weather(response)
