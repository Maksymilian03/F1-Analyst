from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app, get_anthropic_client
from schemas import DriverStanding

client = TestClient(app)

@patch("main.generate_season_summary", new_callable=AsyncMock)
@patch("main.fetch_driver_standings", new_callable=AsyncMock)
def test_summary_endpoint_return_200_with_summary(mock_fetch_driver_standings, mock_generate_season_summary):
    # Arrange
    app.dependency_overrides[get_anthropic_client] = lambda: AsyncMock()

    mock_fetch_driver_standings.return_value = [
        DriverStanding(
            position=1,
            full_name="Max Verstappen",
            team="Red Bull Racing",
            points=395,
            wins=14,
            driver_number=3
        ),
    ]
    mock_generate_season_summary.return_value = "Summary for Max Verstappen"

    try:
        # Act
        response = client.get("/summary/2023/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["year"] == 2023
        assert data["model"] == "claude-haiku-4-5"
        assert data["summary"] == "Summary for Max Verstappen"

        mock_fetch_driver_standings.assert_awaited_once_with(2023)
        mock_generate_season_summary.assert_awaited_once()
    finally:
        app.dependency_overrides.clear()
