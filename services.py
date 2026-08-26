import os

import httpx
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
from fastapi import HTTPException

from schemas import DriverStanding, RaceResult


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
            f"Jesteś ekspertem w Formule 1. Bazując na podsumowaniu sezonu {year}, "
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

async def fetch_race_results(year: int, country: str) -> list[RaceResult]:
    base_url = os.environ["F1_STATS_BASE_URL"]
    url = f"{base_url.rstrip('/')}/results/{year}/{country}/"

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Race not found for {country} in {year}"
                ) from e
            raise
        data = response.json()

    return [RaceResult.model_validate(item) for item in data]

def build_analysis_prompt(year: int, country: str, results: list[RaceResult]) -> str:

    def format_result(result: RaceResult) -> str:
        if result.dnf:
            return f"DNF: {result.full_name} (#{result.driver_number})"
        if result.dns:
            return f"DNS: {result.full_name} (#{result.driver_number})"
        if result.dsq:
            return f"DSQ: {result.full_name} (#{result.driver_number})"
        return (
            f"{result.position}. {result.full_name} "
            f"(#{result.driver_number}) - Gap to leader: {result.gap_to_leader}"
        )

    results_txt = "\n".join(
        format_result(result) for result in results
    )

    return (
        f"Jesteś ekspertem w Formule 1. Bazując na wynikach wyścigu w {country} w sezonie {year}, "
        f"napisz analizę w dwóch akapitach, obejmującą kluczowe momenty wyścigu, "
        f"strategię zespołów i wyróżniające się występy kierowców.\n\n"
        f"Wyniki wyścigu:\n{results_txt}"
    )


async def generate_race_analysis(
        year: int,
        country: str,
        results: list[RaceResult],
        anthropic_client: AsyncAnthropic
) -> str:
    prompt = build_analysis_prompt(year, country, results)

    message = await anthropic_client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        model="claude-haiku-4-5",
    )
    first_block =  message.content[0]
    if not isinstance(first_block, TextBlock):
        raise RuntimeError(f"Expected TextBlock, got {type(first_block).__name__}")

    return first_block.text
