"""Fetch only the two documented public sessions; raw data stays local."""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

COMMIT = "4bc3e52469934aa0551a2261a6e4e899d156c28f"
BASE = f"https://raw.githubusercontent.com/stefan-ehrlich/dataset-ErrP-HRI/{COMMIT}/"
FILES = {f"robot/{s}_robot.{ext}": size for s, sizes in
         [("s02", (5514600, 53944320)), ("s03", (5516936, 53981280))]
         for ext, size in zip(("set", "fdt"), sizes)}
FILES["documentation_dataset-ErrP-HRI.pdf"] = None


def fetch(destination=Path("data/public_errp")):
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for remote, size in FILES.items():
        target = destination / ("documentation.pdf" if remote.endswith(".pdf") else Path(remote).name)
        if not target.exists() or (size and target.stat().st_size != size):
            partial = target.with_suffix(target.suffix + ".partial")
            print("Downloading", remote, flush=True)
            with urlopen(BASE + remote, timeout=45) as response, partial.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            if size and partial.stat().st_size != size:
                raise ValueError(f"Unexpected size: {remote}")
            partial.replace(target)
        digest = hashlib.file_digest(target.open("rb"), "sha256").hexdigest()
        records.append({"file": target.name, "source": BASE + remote,
                        "bytes": target.stat().st_size, "sha256": digest})
    (destination / "manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    return records


if __name__ == "__main__":
    fetch()
