# app/recommend.py
import numpy as np
import xgboost as xgb
from .features import build_features
from .heroes import get_hero_maps


def recommend(model, vec, lbl, pick_ctx, top_k=5):
    feats = build_features(pick_ctx)
    X = vec.transform([feats])
    dmat = xgb.DMatrix(X)

    probs = model.predict(dmat)[0]

    id_to_name, _, id_to_icon = get_hero_maps()

    banned = set(pick_ctx.get("bans", []))
    picked = set(pick_ctx.get("allies", [])) | set(pick_ctx.get("enemies", []))
    excluded = banned | picked

    order = np.argsort(probs)[::-1]

    results = []
    for i in order:
        hero_id = int(lbl.inverse_transform([i])[0])

        if hero_id in excluded:
            continue

        results.append({
            "hero_id": hero_id,
            "name": id_to_name.get(hero_id, f"Hero {hero_id}"),
            "icon_url": id_to_icon.get(hero_id),
            "probability": float(probs[i])
        })

        if len(results) >= top_k:
            break

    return results
