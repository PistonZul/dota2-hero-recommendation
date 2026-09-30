from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .load_model import load_all
from .opendota import fetch_match
from .recommend import recommend
from .heroes import get_hero_maps, normalize_name

app = FastAPI(title="Dota 2 Draft Recommendation API")

model, vec, lbl = load_all()
id_to_name, name_to_id, _ = get_hero_maps()


class RecommendRequest(BaseModel):
    match_id: int
    hero_name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend_hero(req: RecommendRequest):
    hero_norm = normalize_name(req.hero_name)

    if hero_norm not in name_to_id:
        raise HTTPException(status_code=400, detail="Nieznany bohater")

    hero_id = name_to_id[hero_norm]

    match = fetch_match(req.match_id)
    pb = match.get("picks_bans")

    if not pb:
        raise HTTPException(status_code=400, detail="Mecz nie zawiera draftu")

    picks = sorted(pb, key=lambda x: x["order"])

    picked_event = next(
        (x for x in picks if x["is_pick"] and x["hero_id"] == hero_id),
        None
    )

    if not picked_event:
        raise HTTPException(status_code=400, detail="Bohater nie występuje w tym meczu")

    pick_index = picked_event["order"]
    side = picked_event["team"]

    earlier = [x for x in picks if x["order"] < pick_index]

    pick_ctx = {
        "side": side,
        "pick_index": pick_index,
        "allies": [x["hero_id"] for x in earlier if x["is_pick"] and x["team"] == side],
        "enemies": [x["hero_id"] for x in earlier if x["is_pick"] and x["team"] != side],
        "bans": [x["hero_id"] for x in earlier if not x["is_pick"]],
    }

    recs = recommend(model, vec, lbl, pick_ctx, top_k=5)

    return {
        "match_id": req.match_id,
        "picked_hero": {
            "id": hero_id,
            "name": id_to_name[hero_id]
        },
        "side": "radiant" if side == 0 else "dire",
        "pick_index": pick_index,
        "recommendations": recs
    }
