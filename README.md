# F1-Analyst

API wykorzystujące AI do analizy i predykcji wyścigów Formuły 1. Używa Anthropic Claude jako silnika reasoning na danych historycznych z F1-Stats API.

## Koncept

F1-Analyst pobiera dane z projektu [F1-Stats](https://github.com/Maksymilian03/F1-Stats) i dodaje warstwę AI, która:
- Analizuje zakończone wyścigi generując komentarz
- Generuje predykcje nadchodzących wyścigów z uzasadnieniem

## Stack technologiczny

- Python 3.13
- FastAPI
- Anthropic Claude API (claude-haiku-4-5)
- httpx (async client do F1-Stats API)
- Pydantic (walidacja i structured output)
- Docker + docker-compose
- GitHub Actions CI/CD (pytest + ruff + mypy)

## Endpointy

### Dostępne

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | /health/ | Health check API |
| GET | /summary/{year}/ | Podsumowanie sezonu F1 wygenerowane przez AI |
| GET | /analyze/{year}/{country}/ | Analiza zakończonego wyścigu |

### Planowane (v0.2)

| Metoda | Endpoint | Opis |
|--------|----------|------|
| POST | /predict/{year}/{country}/ | Predykcja nadchodzącego wyścigu z uzasadnieniem |

## Przykład: GET /summary/2024/

Endpoint pobiera aktualną klasyfikację kierowców z F1-Stats API dla podanego sezonu i generuje 2-akapitowe podsumowanie sezonu przy użyciu Anthropic Claude (haiku-4-5). Podsumowanie zawiera walkę o mistrzostwo, kluczowych zawodników i najciekawsze historie sezonu.

**Odpowiedź:**

​```json
{
    "year":2024,
    "model":"claude-haiku-4-5",
    "summary":"# Podsumowanie Sezonu Formuły 1 2024\n\nMax Verstappen po raz czwarty z rzędu zdobył tytuł mistrza świata, choć tym razem jego dominacja została poddana poważniejszej próbie niż w poprzednich latach. Holender zakończył sezon z 434 punktami i 9 zwycięstwami..."
}
​```

Czas odpowiedzi: 2-5 sekund (generacja przez Claude).

## Roadmap

### Zrobione (v0.1)
- [x] Integracja z F1-Stats API (httpx client)
- [x] Integracja z Anthropic API
- [x] Endpoint /summary/{year}/ z generacją AI
- [x] Structured output przez Pydantic
- [x] Docker Compose setup
- [x] Testy integracyjne (happy path + walidacja)
- [x] CI/CD (pytest + ruff + mypy)
- [x] Endpoint /analyze/{year}/{country}/ — analiza pojedynczego wyścigu

### W planach (v0.2)
- [ ] Endpoint /predict/{year}/{country}/ — predykcje z uzasadnieniem
- [ ] Cache odpowiedzi LLM (Redis)
- [ ] Strukturalne logowanie (structlog)
- [ ] Deploy live (Render lub inne)

### v1.0
- [ ] Prosty frontend (React lub Streamlit)
- [ ] Rate limiting
- [ ] Monitorowanie kosztów (użycie tokenów per request)

## Powiązane projekty

- [F1-Stats](https://github.com/Maksymilian03/F1-Stats) — backend dostarczający dane wykorzystywany przez F1-Analyst