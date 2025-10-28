from fastapi import FastAPI, Request
import requests
import asyncio
import os

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

    return {"status": "ok"}


async def async_notify(message: str):
    """Async wrapper for Discord notification"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, notify, message)
