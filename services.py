import os

import httpx

from schemas import DriverStanding


async def fetch_driver_standings(year: int) -> list[DriverStanding]:
    base_url = os.environ["F1_STATS_BASE_URL"]
    url = f"{base_url.rstrip('/')}/standings/{year}/"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    return [DriverStanding.model_validate(item) for item in data]
