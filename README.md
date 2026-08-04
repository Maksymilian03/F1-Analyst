# F1-Analyst

AI-powered analysis and prediction API for Formula 1 races. Uses Anthropic Claude 
as reasoning engine over historical F1 data from F1-Stats API.

## Concept

F1-Analyst consumes race data from [F1-Stats](link) and adds an AI layer that:
- Analyzes completed races with human-quality commentary
- Generates predictions for upcoming races with reasoning

## Tech Stack

- Python 3.13
- FastAPI
- Anthropic Claude API (claude-sonnet-4-5 or claude-haiku-4-5)
- httpx (async client for F1-Stats API)
- Pydantic (structured LLM output)
- Docker + docker-compose
- GitHub Actions CI/CD (pytest + ruff + mypy)

## Endpoints (planned MVP)

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | /analyze/{year}/{country}/ | Analiza zakończonego wyścigu |
| POST | /predict/{year}/{country}/ | Predykcja nadchodzącego wyścigu z uzasadnieniem |
| GET | /health/ | Health check |

## Roadmap

### v0.1 MVP (target: 1 miesiąc)
- [ ] Integration z F1-Stats API (httpx client)
- [ ] Anthropic API integration
- [ ] Endpoint /analyze/ — race analysis z LLM
- [ ] Structured LLM output przez Pydantic
- [ ] Docker Compose setup
- [ ] Podstawowe testy (unit + integration z mocked LLM)

### v0.2
- [ ] Endpoint /predict/ z uzasadnieniem
- [ ] Caching odpowiedzi LLM (drogo strzelać za każdym razem)
- [ ] Structured logging (structlog)
- [ ] Deploy live

### v1.0
- [ ] Frontend prosty (opcjonalnie React albo Streamlit)
- [ ] Rate limiting
- [ ] Cost monitoring (token usage per request)

## Related projects

- [F1-Stats](link) — backend data provider used by F1-Analyst