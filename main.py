from fastapi import FastAPI, Request
import requests
import asyncio
import os
import random

app = FastAPI()

# Use environment variable if available, otherwise use default
DISCORD_WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL",
    "https://canary.discord.com/api/webhooks/1432739969767575622/saX2e1tX66FMpFUksozEoBRc-fGmZGyj7bsliBKF7LrBF1lVuBc59Td7oTtKqrfGI44Y"
)


def notify(message: str):
    """Send a message to Discord webhook."""
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print("Sent:", response.status_code)


@app.post("/")
async def receive_webhook(request: Request):
    """Webhook endpoint"""
    data = await request.json()
    print("Received:", data)

    # You can customize the message formatting here
    message = f"📩 New webhook received:\n```json\n{data}\n```"

    # Send notification asynchronously
    asyncio.create_task(async_notify(message))

    # Trigger simulated trade executions asynchronously
    asyncio.create_task(executeTradeonTradovate(details=data))
    asyncio.create_task(executeTradeonNinjaTrader(details=data))

    return {"status": "ok"}


async def async_notify(message: str):
    """Async wrapper for Discord notification"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, notify, message)


async def executeTradeonTradovate(details=None):
    """Simulate executing a trade on Tradovate and notify Discord."""
    await asyncio.sleep(random.uniform(0.5, 2.5))
    message = "this is the TradeonTradovate function"
    await async_notify(message)


async def executeTradeonNinjaTrader(details=None):
    """Simulate executing a trade on NinjaTrader and notify Discord."""
    await asyncio.sleep(random.uniform(0.5, 2.5))
    message = "this is the TradeonNinjaTrader function"
    await async_notify(message)
