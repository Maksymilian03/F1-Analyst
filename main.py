from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="F1-Analyst",
    description="AI-powered F1 race analysis using Anthropic Claude",
    version="0.1.0",
)

class HealthResponse(BaseModel):
    status: str

@app.get("/health/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify that the API is running.
    """
    return HealthResponse(status="ok")
