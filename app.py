import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket

from client import WebClient
from weather import WeatherClient

client = WebClient()
api = FastAPI()


@api.on_event('shutdown')
def shutdown():
    client.shutdown()


@api.get("/")
async def read_root():
    return {"Hello": "World"}


async def send_weather_data(websocket: WebSocket, weather_client: WeatherClient, data: dict):
    while True:
        weather = await weather_client.weather(data)
        await websocket.send_json(weather.dict())
        await asyncio.sleep(15)


@api.websocket("/ws/weather")
async def read_websocket(websocket: WebSocket):
    await websocket.accept()

    weather_client = WeatherClient(client)
    queue = asyncio.queues.Queue()

    async def read_from_socket():
        async for data in websocket.iter_json():
            queue.put_nowait(data)

    async def send_data():
        data = await queue.get()
        send_task = asyncio.create_task(send_weather_data(websocket, weather_client, data))
        while True:
            data = await queue.get()
            if data:
                print(f'Cancelling existing task since got new event={data}')
                send_task.cancel()
            send_task = asyncio.create_task(send_weather_data(websocket, weather_client, data))

    await asyncio.gather(read_from_socket(), send_data())


if __name__ == '__main__':
    uvicorn.run(api)
