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

