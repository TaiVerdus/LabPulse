"""Check dependencies without starting hardware or downloading data."""
import importlib
import json
from pathlib import Path
import sys


def main():
    result = {"python": sys.version.split()[0], "modules": {}, "device_verified": False}
    ok = True
    for name in ("numpy", "scipy", "sklearn", "joblib", "pylsl", "threadpoolctl"):
        try:
            m = importlib.import_module(name)
            result["modules"][name] = getattr(m, "__version__", "imported")
        except Exception as e:
            ok = False
            result["modules"][name] = str(e)
    result["data_present"] = all((Path("data/public_errp") / f"{s}_robot.{ext}").exists()
                                 for s in ("s02", "s03") for ext in ("set", "fdt"))
    result["status"] = "dependencies_ready" if ok else "missing_dependency"
    Path("reports/offline").mkdir(parents=True, exist_ok=True)
    Path("reports/offline/environment.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
