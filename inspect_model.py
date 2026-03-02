# inspect_model.py
import joblib, os, sys

p = "models/crop_yield_model.pkl"
if not os.path.exists(p):
    print("MISSING: models/crop_yield_model.pkl not found")
    sys.exit(1)

obj = joblib.load(p)
print("TYPE:", type(obj))
if isinstance(obj, dict):
    print("KEYS:", list(obj.keys()))
else:
    try:
        print("REPR (short):", repr(obj)[:200])
    except Exception:
        print("REPR: <could not display>")
