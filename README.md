# Dota 2 Draft Recommendation System

Aplikacja wspomagająca decyzje w fazie draftu gry Dota 2
na podstawie analizy danych historycznych meczów.

## Funkcjonalności
- rekomendacja bohaterów na podstawie aktualnego draftu
- model XGBoost uczony na danych z OpenDota
- interfejs użytkownika w Streamlit
- backend REST API (FastAPI)

## Uruchomienie

1. Instalacja zależności:
pip install -r requirements.txt

2. Uruchom backend:
uvicorn app.main:app --reload

3. Uruchom frontend:
streamlit run streamlit_app.py

## Dane wejściowe
- Match ID (OpenDota)
- Nazwa bohatera (case-insensitive)

## Autor
Mateusz Maciej Bugaj
