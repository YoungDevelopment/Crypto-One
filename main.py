from fastapi import FastAPI, Request
import requests
import asyncio
import os
import random

app = FastAPI()

DISCORD_WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL",
    "https://canary.discord.com/api/webhooks/1432739969767575622/saX2e1tX66FMpFUksozEoBRc-fGmZGyj7bsliBKF7LrBF1lVuBc59Td7oTtKqrfGI44Y"
)


def notify(message: str):
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print("Sent:", response.status_code)


async def async_notify(message: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, notify, message)


# --- Async trade simulators ---
async def executeTradeonTradovate():
    await asyncio.sleep(random.uniform(1, 3))
    await async_notify("This is a trade on Tradovate")


async def executeTradeonNinjaTrader():
    await asyncio.sleep(random.uniform(1, 3))
    await async_notify("This is a trade on NinjaTrader")


async def executeTradeonEasyTrade():
    await asyncio.sleep(random.uniform(1, 3))
    await async_notify("This is a trade on EasyTrade")


@app.post("/")
async def receive_webhook(request: Request):
    data = await request.json()
    print("Received:", data)

        # Launch trade simulations concurrently
    asyncio.create_task(executeTradeonTradovate())
    asyncio.create_task(executeTradeonNinjaTrader())
    asyncio.create_task(executeTradeonEasyTrade())
    message = f"📩 New webhook received:\n```json\n{data}\n```"
    asyncio.create_task(async_notify(message))



    return {"status": "ok"}
