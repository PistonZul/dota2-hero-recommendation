import requests
from functools import lru_cache

ODOTA = "https://api.opendota.com/api"
STEAM_CDN = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heroes"

def normalize_name(name: str) -> str:
    return name.strip().lower()

@lru_cache(maxsize=1)
def get_hero_maps():
    r = requests.get(f"{ODOTA}/heroes", timeout=30)
    r.raise_for_status()
    heroes = r.json()

    id_to_name = {}
    name_to_id = {}
    id_to_icon = {}

    for h in heroes:
        hid = h["id"]
        localized = h["localized_name"]
        api_name = h["name"].replace("npc_dota_hero_", "")

        id_to_name[hid] = localized
        name_to_id[normalize_name(localized)] = hid
        id_to_icon[hid] = f"{STEAM_CDN}/{api_name}_full.png"

    return id_to_name, name_to_id, id_to_icon
