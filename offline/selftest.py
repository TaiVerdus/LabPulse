"""Local synthetic LSL integration check, clearly separated from EEG evaluation."""
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    root = Path("local_runs/sim_check")
    root.mkdir(parents=True, exist_ok=True)
    with (root / "publisher.log").open("wb") as log:
        publisher = subprocess.Popen([sys.executable, "-X", "utf8", "-m", "offline.stream", "publish", "--seconds", "25"],
                                     stdout=log, stderr=log)
        try:
            time.sleep(2)
            result = subprocess.run([sys.executable, "-X", "utf8", "-m", "offline.stream", "capture",
                                     "--seconds", "5", "--simulate", "--marker-name", "LabPulse-SIM-Markers",
                                     "--output", str(root)], capture_output=True, timeout=20)
            (root / "receiver.log").write_bytes(result.stdout + result.stderr)
            if result.returncode:
                print("模拟接收失败；见 local_runs/sim_check/receiver.log。请检查防火墙和本机流发现。")
                return result.returncode
            summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
            passed = (summary["mode"] == "simulation" and summary["samples"] >= 3000
                      and summary["markers"] >= 2 and summary["nonmonotonic_intervals"] == 0)
            summary["software_selftest_passed"] = passed
            Path("reports/offline").mkdir(parents=True, exist_ok=True)
            Path("reports/offline/lsl_simulation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
            print("合成 LSL 软件联调：", "通过" if passed else "失败", "；不代表设备验证。")
            return 0 if passed else 2
        finally:
            publisher.terminate()
            publisher.wait(timeout=5)


if __name__ == "__main__":
    sys.exit(main())
