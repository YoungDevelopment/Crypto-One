from fastapi import FastAPI, Request
import asyncio
import os
import random
import httpx
import json
import time

app = FastAPI()

DISCORD_WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL",
    # replace with a confirmed working webhook. prefer "discord.com" not "canary.discord.com"
    "https://discord.com/api/webhooks/1432739969767575622/REPLACE_WITH_REAL_TOKEN"
)

# Shared async HTTP client for reuse
http_client = httpx.AsyncClient(timeout=10.0)

async def post_with_retries(url: str, json_payload: dict, max_retries: int = 3):
    """Post JSON to a URL with simple exponential backoff retries and detailed logging."""
    backoff = 0.5
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            r = await http_client.post(url, json=json_payload)
            # Log status and small response body for debugging
            text = r.text[:1000] if r.text else ""
            print(f"[Discord] attempt={attempt} status={r.status_code} body={text}")
            # 2xx -> success
            if 200 <= r.status_code < 300:
                return r
            # 429 -> rate limited. respect Retry-After if present
            if r.status_code == 429:
                try:
                    retry_after = r.json().get("retry_after")
                except Exception:
                    retry_after = None
                if retry_after:
                    wait = float(retry_after)
                    print(f"[Discord] rate limited. sleeping {wait}s")
                    await asyncio.sleep(wait)
                    continue
            # For other 4xx/5xx, retry after backoff
            await asyncio.sleep(backoff)
            backoff *= 2
        except Exception as exc:
            last_exc = exc
            print(f"[Discord] network/exception on attempt {attempt}: {exc}")
            await asyncio.sleep(backoff)
            backoff *= 2
    raise RuntimeError(f"Failed to post to Discord after {max_retries} attempts") from last_exc


async def async_notify(message: str):
    """Send a message to Discord webhook asynchronously with retries and logging."""
    if not DISCORD_WEBHOOK_URL:
        print("DISCORD_WEBHOOK_URL is not set.")
        return
    payload = {"content": message}
    try:
        await post_with_retries(DISCORD_WEBHOOK_URL, payload)
    except Exception as e:
        # Log full exception for diagnostics
        print("Failed to send discord message:", repr(e))


# Async trade simulators with delays
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
    print("Received:", json.dumps(data, default=str)[:2000])

    # immediate notification about incoming webhook
    asyncio.create_task(async_notify(f"📩 New webhook received:\n```json\n{json.dumps(data, indent=2)}\n```"))

    # Launch trade simulations concurrently
    asyncio.create_task(executeTradeonTradovate())
    asyncio.create_task(executeTradeonNinjaTrader())
    asyncio.create_task(executeTradeonEasyTrade())

    return {"status": "ok"}
