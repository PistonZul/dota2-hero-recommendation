# app/features.py
def build_features(pick_ctx: dict) -> dict:
    d = {}

    for h in pick_ctx["allies"]:
        d[f"ally_{h}"] = 1
    for h in pick_ctx["enemies"]:
        d[f"enemy_{h}"] = 1
    for h in pick_ctx["bans"]:
        d[f"ban_{h}"] = 1

    d["side"] = pick_ctx["side"]
    d["pick_order"] = pick_ctx["pick_index"]
    d["n_allies"] = len(pick_ctx["allies"])
    d["n_enemies"] = len(pick_ctx["enemies"])
    d["n_bans"] = len(pick_ctx["bans"])

    if pick_ctx["pick_index"] <= 4:
        d["draft_phase"] = 0
    elif pick_ctx["pick_index"] <= 9:
        d["draft_phase"] = 1
    else:
        d["draft_phase"] = 2

    return d
