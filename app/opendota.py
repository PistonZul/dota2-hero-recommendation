# app/opendota.py
import requests

ODOTA = "https://api.opendota.com/api"

def fetch_match(match_id: int) -> dict:
    r = requests.get(f"{ODOTA}/matches/{match_id}", timeout=30)
    r.raise_for_status()
    return r.json()
