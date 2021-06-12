# fastapi-websockets-aiohttp-demo

A demo application which showcases how we can use [FastApi](https://fastapi.tiangolo.com) with [WebSockets](https://fastapi.tiangolo.com/advanced/websockets) and [aiohttp](https://docs.aiohttp.org/en/stable/).

While working on a project, I could not a find any proper sample code which could demonstrate this idea. Most of the examples were fairly basic and had a one file code which can be good for scripting but not for use in a proper application.

## About
This sample app exposes a WebSocket endpoint to query the weather of a place.
We connect to the endpoint: `ws://localhost:8000/ws/weather` and then send a message in the following format:
```json
{
  "city": "Bangalore",
  "country": "India"
}
```

Now the server sends back a `Weather` response every 1 minute. We can send another message with a different place, and the server would start sending the weather updates for that place. 
