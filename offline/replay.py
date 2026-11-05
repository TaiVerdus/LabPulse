"""Replay held-out predictions to a local prompt; no external actions."""
import argparse
import json
import time
from pathlib import Path


def replay(source, limit=10, delay=0.3):
    if limit < 1 or delay < 0:
        raise ValueError("Invalid replay limit or delay")
    seen = set()
    print("【公开数据回放】无设备、无机械臂、无 Jarvis；播放间隔不是推理延迟。")
    for line in source.read_text(encoding="utf-8").splitlines()[:limit]:
        p = json.loads(line)
        if p["mode"] != "replay":
            raise ValueError("Unexpected replay mode")
        if p["event_id"] in seen:
            continue
        seen.add(p["event_id"])
        print(f"{p['event_id']} | score={p['score']:.3f} | {p['message']}", flush=True)
        time.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("reports/offline/predictions.jsonl"))
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()
    replay(args.source, args.limit, args.delay)
