import os

import httpx
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock

from schemas import DriverStanding


async def fetch_driver_standings(year: int) -> list[DriverStanding]:
    base_url = os.environ["F1_STATS_BASE_URL"]
    url = f"{base_url.rstrip('/')}/standings/{year}/"

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    return [DriverStanding.model_validate(item) for item in data]

def build_summary_prompt(year: int, standings: list[DriverStanding]) -> str:
    standings_txt = "\n".join(
        f"{driver.position}. {driver.full_name} ({driver.team}) - "
        f"{driver.points} points, {driver.wins} wins"
        for driver in standings
    )
    return (
            f"Jesteś ekspertem w Formule 1. Bazujac na podsumowaniu sezonu {year}, "
            f"napisz podsumowanie w dwóch akapitach, obejmujące walkę o mistrzostwo, "
            f"kluczowych performerów i najciekawszych historii.\n\n"
            f"Podsumowanie:\n{standings_txt}"
        )

async def generate_season_summary(
        year: int,
        standings: list[DriverStanding],
        anthropic_client: AsyncAnthropic
) -> str:
    prompt = build_summary_prompt(year, standings)

    message = await anthropic_client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        model="claude-haiku-4-5",
    )
    first_block =  message.content[0]
    if not isinstance(first_block, TextBlock):
        raise RuntimeError(f"Expected TextBlock, got {type(first_block).__name__}")

    return first_block.text
