from pydantic import BaseModel


class DriverStanding(BaseModel):
    position: int
    full_name: str
    team: str
    points: float
    wins: int
    driver_number: int


class SummaryResponse(BaseModel):
    year: int
    model: str
    summary: str


class RaceResult(BaseModel):
    position: int | None
    full_name: str
    driver_number: int
    gap_to_leader: float | str | None
    dnf: bool
    dns: bool
    dsq: bool


class AnalysisResponse(BaseModel):
    year: int
    country: str
    model: str
    analysis: str


