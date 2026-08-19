from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app
from schemas import RaceResult

client = TestClient(app)

@patch('main.generate_race_analysis', new_callable=AsyncMock)
@patch('main.fetch_race_results', new_callable=AsyncMock)
def test_analyze_endpoint_returns_200_with_analysis(mock_fetch_race_results, mock_generate_race_analysis):
    # Arrange
    mock_fetch_race_results.return_value = [
        RaceResult(
            position=1,
            full_name="Max VERSTAPPEN",
            driver_number=1,
            gap_to_leader=0,
            dnf=False,
            dns=False,
            dsq=False
        )
    ]
    mock_generate_race_analysis.return_value = "Analyze for race"

    # Act
    response = client.get("/analyze/2023/France/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['year'] == 2023
    assert data['country'] == "France"
    assert data['model'] == "claude-haiku-4-5"
    assert data['analysis'] == "Analyze for race"

    mock_fetch_race_results.assert_awaited_once_with(2023, "France")
    mock_generate_race_analysis.assert_awaited_once()


def test_analyze_endpoint_returns_422_when_year_below_2023():
    # Act
    response = client.get("/analyze/2022/France/")

    # Assert
    assert response.status_code == 422


def test_analyze_endpoint_returns_422_when_year_above_current():
    # Act
    response = client.get("/analyze/2100/France/")

    # Assert
    assert response.status_code == 422
