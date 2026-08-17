import os
from datetime import datetime

from anthropic import AsyncAnthropic
from fastapi import Depends, FastAPI, Path
from pydantic import BaseModel

from schemas import AnalysisResponse, SummaryResponse
from services import (
    fetch_driver_standings,
    fetch_race_results,
    generate_race_analysis,
    generate_season_summary,
)

CURRENT_YEAR = datetime.now().year


app = FastAPI(
    title="F1-Analyst",
    description="AI-powered F1 race analysis using Anthropic Claude",
    version="0.1.0",
)

def get_anthropic_client() -> "AsyncAnthropic":
    """
    Create and return an instance of the AsyncAnthropic client.
    """
    return AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@app.get('/summary/{year}/', response_model=SummaryResponse)
async def get_season_summary(
    year: int = Path(..., ge=2023, le=CURRENT_YEAR),
    anthropic_client: AsyncAnthropic = Depends(get_anthropic_client) # noqa: B008
) -> SummaryResponse:
    """
    Endpoint to fetch the F1 season summary for a given year.
    """
    standings = await fetch_driver_standings(year)
    summary_text = await generate_season_summary(year, standings, anthropic_client)

    return SummaryResponse(
        year=year,
        model="claude-haiku-4-5",
        summary=summary_text
    )


@app.get('/analyze/{year}/{country}/', response_model=AnalysisResponse)
async def get_race_analysis(
    year: int = Path(..., ge=2023, le=CURRENT_YEAR),
    country: str = Path(..., min_length=2, max_length=20),
    anthropic_client: AsyncAnthropic = Depends(get_anthropic_client) # noqa: B008
) -> AnalysisResponse:
    """
    Endpoint to fetch the F1 race analysis for a given year and country.
    """
    results = await fetch_race_results(year, country)
    analysis_text = await generate_race_analysis(year, country, results, anthropic_client)

    return AnalysisResponse(
        year=year,
        country=country,
        model="claude-haiku-4-5",
        analysis=analysis_text
    )

class HealthResponse(BaseModel):
    status: str

@app.get("/health/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify that the API is running.
    """
    return HealthResponse(status="ok")
