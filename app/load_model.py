# app/load_model.py
from pathlib import Path
import joblib
import xgboost as xgb

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"

MODEL_PATH = MODELS / "xgb_min40.json"
VEC_PATH   = MODELS / "vec_xgb_min40.joblib"
LBL_PATH   = MODELS / "lbl_xgb_min40.joblib"


def load_all():
    print("Ładowanie modelu XGBoost...")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Brak pliku modelu: {MODEL_PATH}")
    if not VEC_PATH.exists():
        raise FileNotFoundError(f"Brak pliku wektoryzatora: {VEC_PATH}")
    if not LBL_PATH.exists():
        raise FileNotFoundError(f"Brak pliku label encoder: {LBL_PATH}")

    # --- MODEL XGBOOST ---
    model = xgb.Booster()
    model.load_model(str(MODEL_PATH))

    # --- VEKTORYZATOR I LABELS ---
    vec = joblib.load(VEC_PATH)
    lbl = joblib.load(LBL_PATH)

    print("Model, wektoryzator i etykiety załadowane poprawnie.")

    return model, vec, lbl
