"""Practice-only visual task; not an approved EEG experiment protocol."""
import argparse
import json
import random
import time
from pathlib import Path


def schedule(seed=20261105):
    # Practice engineering fixture, not a sample-size or research-design recommendation.
    trials = [(target, wrong) for target in ("←", "→") for wrong in ([False] * 7 + [True] * 3)]
    random.Random(seed).shuffle(trials)
    return [{"trial": i, "target": t, "outcome": ("→" if t == "←" else "←") if e else t,
             "planned_error": e} for i, (t, e) in enumerate(trials)]


def main(dry_run=False):
    rows = schedule()
    if dry_run:
        print(json.dumps({"mode": "practice_schedule_only", "trials": len(rows),
                          "errors": sum(r["planned_error"] for r in rows)}, ensure_ascii=False))
        return
    import tkinter as tk
    out = Path("local_runs") / ("practice-" + time.strftime("%Y%m%d-%H%M%S"))
    out.mkdir(parents=True, exist_ok=False)
    (out / "truth.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    root = tk.Tk(); root.title("LabPulse 屏幕练习｜无 EEG、无分类"); root.geometry("850x580")
    title = tk.Label(root, text="仅练习操作和记录流程，不采集 EEG，不产生 ErrP 识别结果", font=("Microsoft YaHei", 15))
    title.pack(pady=20)
    target = tk.Label(root, text="规则：观察系统方向是否符合目标方向。", font=("Microsoft YaHei", 22)); target.pack(pady=15)
    display = tk.Label(root, text="", font=("Microsoft YaHei", 42)); display.pack(pady=20)
    feedback = tk.Frame(root); feedback.pack()
    note = tk.Label(root, text="每次结果消失后，回答刚才系统是否出错。", font=("Microsoft YaHei", 14)); note.pack(pady=10)
    state = {"index": 0, "accept": False}

    def log(kind, value=""):
        with (out / "events.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({"mode": "practice_no_eeg", "trial": state["index"], "kind": kind,
                                "perf_counter_s": time.perf_counter(), "value": value}, ensure_ascii=False) + "\n")

    def next_trial():
        state["accept"] = False
        for b in buttons: b.config(state="disabled")
        i = state["index"]
        if i >= len(rows):
            target.config(text="练习完成"); display.config(text=""); note.config(text=f"记录位置：{out}")
            log("completed"); return
        target.config(text=f"目标方向：{rows[i]['target']}")
        display.config(text="＋")
        log("target_requested")
        root.after(1500, show_result)

    def show_result():
        display.config(text=rows[state["index"]]["outcome"])
        root.update_idletasks()
        log("outcome_software_update_returned")
        root.after(1000, ask)

    def ask():
        display.config(text="是否出错？")
        state["accept"] = True
        for b in buttons: b.config(state="normal")
        log("response_enabled")

    def answer(value):
        if not state["accept"]: return
        state["accept"] = False
        log("subjective_response", value)
        state["index"] += 1
        next_trial()

    buttons = [tk.Button(feedback, text=t, command=lambda v=v: answer(v), font=("Microsoft YaHei", 18))
               for t, v in [("出错", "error"), ("正常", "correct"), ("不确定", "unsure")]]
    for b in buttons: b.pack(side="left", padx=10); b.config(state="disabled")
    start = tk.Button(root, text="开始20次练习", command=lambda: (start.config(state="disabled"), next_trial()))
    start.pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", lambda: (log("closed"), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    main(parser.parse_args().dry_run)
