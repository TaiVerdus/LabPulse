"""Bounded LSL recorder and explicit simulated source for offline integration."""
import argparse
import csv
import json
import math
import time
from pathlib import Path

import numpy as np


def capture(output, seconds=10, name="LabPulse-SIM-EEG", marker_name="LabPulse-SIM-Markers", simulate=False):
    import pylsl
    if seconds <= 0 or seconds > 600:
        raise ValueError("Duration must be 0 < seconds <= 600")
    candidates = pylsl.resolve_byprop("name", name, timeout=5)
    if len(candidates) != 1:
        raise ValueError(f"Expected exactly one stream named {name}; found {len(candidates)}")
    info = candidates[0]
    if info.type() != "EEG" or info.nominal_srate() <= 0 or info.channel_count() != 16:
        raise ValueError("Expected 16-channel regularly sampled EEG; verify GUI configuration")
    xml = info.as_xml()
    is_sim = name.startswith("LabPulse-SIM-") or "labpulse-sim" in info.source_id()
    if is_sim and not simulate:
        raise ValueError("SIM stream requires --simulate, cannot label simulation live")
    markers = pylsl.resolve_byprop("name", marker_name, timeout=2) if marker_name else []
    if len(markers) > 1:
        raise ValueError("Ambiguous marker stream")
    inlet = pylsl.StreamInlet(info, processing_flags=pylsl.proc_clocksync)
    mi = pylsl.StreamInlet(markers[0], processing_flags=pylsl.proc_clocksync) if markers else None
    output.mkdir(parents=True, exist_ok=True)
    (output / "stream.xml").write_text(xml, encoding="utf-8")
    ts_all, event_rows, count = [], [], 0
    start = time.monotonic()
    with (output / "samples.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lsl_timestamp_s"] + [f"ch{i+1}" for i in range(16)])
        while time.monotonic() - start < seconds:
            samples, ts = inlet.pull_chunk(timeout=0.2, max_samples=2000)
            if samples:
                values = np.asarray(samples)
                if values.shape[1] != 16 or not np.isfinite(values).all():
                    raise ValueError("Invalid channel shape or non-finite sample")
                writer.writerows([[t] + row for t, row in zip(ts, samples)])
                ts_all.extend(ts); count += len(ts)
            if mi:
                while True:
                    value, stamp = mi.pull_sample(timeout=0)
                    if stamp is None:
                        break
                    event_rows.append({"lsl_timestamp_s": stamp, "value": value})
    inlet.close_stream()
    if mi:
        mi.close_stream()
    with (output / "markers.jsonl").open("w", encoding="utf-8") as f:
        for row in event_rows:
            f.write(json.dumps(row) + "\n")
    ts = np.asarray(ts_all)
    dt = np.diff(ts)
    rate = (len(ts) - 1) / (ts[-1] - ts[0]) if len(ts) > 1 and ts[-1] > ts[0] else None
    summary = {"mode": "simulation" if simulate or is_sim else "live_unverified_device",
               "samples": count, "nominal_rate": info.nominal_srate(), "observed_rate": rate,
               "markers": len(event_rows), "nonmonotonic_intervals": int((dt <= 0).sum()),
               "gap_intervals_gt_3x_nominal": int((dt > 3 / info.nominal_srate()).sum()),
               "timestamp_median_interval_ms": float(np.median(dt) * 1000) if len(dt) else None,
               "status": "captured" if count else "no_data",
               "physical_sync": "not_measured", "loss_count": "unknown_without_device_sequence_counter",
               "note": "Clock-corrected LSL timestamps preserved; gap heuristic is not proof of no packet loss"}
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if count == 0:
        raise ValueError("No data received before wall-clock timeout")
    return summary


def publish(seconds):
    import pylsl
    eeg = pylsl.StreamOutlet(pylsl.StreamInfo("LabPulse-SIM-EEG", "EEG", 16, 1000, "float32", "labpulse-sim-eeg"))
    marker = pylsl.StreamOutlet(pylsl.StreamInfo("LabPulse-SIM-Markers", "Markers", 1, 0, "string", "labpulse-sim-marker"))
    start, n, last = pylsl.local_clock(), 0, -1
    print("SIMULATION ONLY: synthetic sine waves, not EEG or ErrP", flush=True)
    while pylsl.local_clock() - start < seconds:
        target = int((pylsl.local_clock() - start) * 1000)
        while n < target:
            eeg.push_sample([math.sin(n / 1000 * 2 * math.pi * (8 + c / 10)) for c in range(16)], start + n / 1000)
            n += 1
        block = int(pylsl.local_clock() - start)
        if block != last:
            marker.push_sample([str(block % 3 + 1)])
            last = block
        time.sleep(0.002)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["list", "capture", "publish"])
    p.add_argument("--seconds", type=float, default=10)
    p.add_argument("--name", default="LabPulse-SIM-EEG")
    p.add_argument("--marker-name", default="")
    p.add_argument("--simulate", action="store_true")
    p.add_argument("--output", type=Path, default=Path("local_runs/lsl"))
    a = p.parse_args()
    try:
        if a.mode == "publish":
            publish(a.seconds)
        elif a.mode == "list":
            import pylsl
            for i in pylsl.resolve_streams(wait_time=3):
                print(i.name(), i.type(), i.channel_count(), i.nominal_srate())
        else:
            capture(a.output, a.seconds, a.name, a.marker_name, a.simulate)
    except (ValueError, RuntimeError, ImportError) as exc:
        p.exit(2, f"LSL 操作失败：{exc}\n")
