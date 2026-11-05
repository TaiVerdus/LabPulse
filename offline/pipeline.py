"""Fixed exploratory baseline. Training/held-out labels never enter features."""
import argparse
import csv
import hashlib
import json
import platform
from collections import Counter
from pathlib import Path

import numpy as np
import scipy
from scipy.io import loadmat
from scipy.signal import butter, sosfilt
import sklearn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import joblib

CONFIG = {"band_hz": [1.0, 10.0], "filter_order": 2,
          "epoch_seconds": [-0.2, 0.8], "feature_seconds": [0.2, 0.6],
          "bins": 8, "peak_to_peak_uv": 200.0, "threshold": 0.5,
          "seed": 20261105, "eog_excluded": True,
          "description": "Fixed exploratory parameters, not optimized or physiological proof"}


def normalize(code):
    return "".join(str(code).split())


def trial_events(events):
    """FB1/2/3 is direction-feedback onset; subsequent S4/5/6 is truth only."""
    rows, segment = [], []
    for event in events:
        code = normalize(event["type"])
        segment.append(event)
        if code == "S9":
            feedback = [e for e in segment if normalize(e["type"]) in ("FB1", "FB2", "FB3")]
            outcomes = [e for e in segment if normalize(e["type"]) in ("S4", "S5", "S6")]
            if len(feedback) != 1 or len(outcomes) != 1:
                raise ValueError("Trial needs exactly one direction feedback and outcome")
            fb, outcome = feedback[0], outcomes[0]
            code = normalize(outcome["type"])
            onset = float(fb["latency"]) - 1.0
            rows.append({"trial": len(rows), "sample_float": onset,
                         "feedback_direction": normalize(fb["type"]), "outcome": code,
                         "human_error": code == "S5", "label": 1 if code == "S6" else 0,
                         "outcome_delay_samples": float(outcome["latency"]) - 1 - onset})
            segment = []
    if any(normalize(e["type"]) in ("S4", "S5", "S6", "FB1", "FB2", "FB3") for e in segment) or not rows:
        raise ValueError("Incomplete feedback/outcome events")
    return rows


def load_session(path):
    eeg = loadmat(path, simplify_cells=True)["EEG"]
    if eeg["trials"] != 1:
        raise ValueError("Reader supports documented continuous EEGLAB sessions only")
    channels = [c["labels"] for c in eeg["chanlocs"]]
    fdt = path.with_suffix(".fdt")
    count = int(eeg["nbchan"]) * int(eeg["pnts"])
    if fdt.stat().st_size != count * 4:
        raise ValueError("FDT size mismatch or incomplete download")
    # EEGLAB external FDT: little-endian float32, channel-major MATLAB dimensions.
    data = np.fromfile(fdt, dtype="<f4").reshape((int(eeg["pnts"]), int(eeg["nbchan"]))).T
    if not np.isfinite(data).all():
        raise ValueError("Non-finite raw data")
    return data.astype(np.float64), float(eeg["srate"]), channels, trial_events(eeg["event"])


def extract(data, sfreq, channels, trials):
    if data.ndim != 2 or len(channels) != data.shape[0] or not np.isfinite(data).all():
        raise ValueError("Invalid EEG shape or non-finite values")
    keep = [i for i, c in enumerate(channels) if not c.upper().startswith("EOG")]
    eeg = data[keep]
    filtered = sosfilt(butter(CONFIG["filter_order"], CONFIG["band_hz"],
                              btype="bandpass", fs=sfreq, output="sos"), eeg, axis=1)
    names = [channels[i] for i in keep]
    features, labels, accepted, all_rows = [], [], [], []
    for trial in trials:
        row = dict(trial)
        center = int(np.rint(trial["sample_float"]))
        lo, hi = [center + int(round(v * sfreq)) for v in CONFIG["epoch_seconds"]]
        reason = "human_error" if trial["human_error"] else ""
        if not reason and (lo < 0 or hi > eeg.shape[1] or center < 2 * sfreq):
            reason = "incomplete_window_or_filter_warmup"
        if not reason and np.ptp(eeg[:, lo:hi], axis=1).max() > CONFIG["peak_to_peak_uv"]:
            reason = "amplitude_artifact"
        row["reason"] = reason
        row["quality"] = "excluded" if reason else "accepted"
        all_rows.append(row)
        if reason:
            continue
        baseline = filtered[:, lo:center].mean(axis=1, keepdims=True)
        a, b = [center + int(round(v * sfreq)) for v in CONFIG["feature_seconds"]]
        epoch = filtered[:, a:b] - baseline
        feat = np.concatenate([x.mean(axis=1) for x in np.array_split(epoch, CONFIG["bins"], axis=1)])
        features.append(feat)
        labels.append(trial["label"])
        accepted.append(row)
    return np.asarray(features), np.asarray(labels), accepted, all_rows, names


def summarize(y, scores):
    if set(np.unique(y)) != {0, 1}:
        raise ValueError("Both classes required for evaluation")
    pred = scores >= CONFIG["threshold"]
    cm = confusion_matrix(y, pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return {"n": len(y), "class_counts": dict(zip(["correct", "machine_error"], np.bincount(y, minlength=2).tolist())),
            "confusion_matrix_true_rows_pred_columns": cm.tolist(),
            "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
            "error_recall": float(tp / (tp + fn)), "normal_false_alarm_rate": float(fp / (fp + tn)),
            "roc_auc": float(roc_auc_score(y, scores)), "majority_class_accuracy": float(max(np.bincount(y)) / len(y)),
            "constant_classifier_balanced_accuracy": 0.5}


def run(data_dir, output):
    output.mkdir(parents=True, exist_ok=True)
    prepared, sources = {}, []
    for subject in ("s02", "s03"):
        path = data_dir / f"{subject}_robot.set"
        data, sf, channels, trials = load_session(path)
        X, y, rows, all_rows, names = extract(data, sf, channels, trials)
        prepared[subject] = X, y, rows
        for row in all_rows:
            row["subject"] = subject
        with (output / f"{subject}_trials.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=all_rows[0].keys()); w.writeheader(); w.writerows(all_rows)
        sources.append({"subject": subject, "sfreq": sf, "channels_total": len(channels),
                        "eeg_channels": names, "duration_s": data.shape[1] / sf,
                        "trials": len(trials), "accepted": len(y),
                        "exclusions": dict(Counter(r["reason"] for r in all_rows if r["reason"])),
                        "set_sha256": hashlib.file_digest(path.open("rb"), "sha256").hexdigest(),
                        "fdt_sha256": hashlib.file_digest(path.with_suffix('.fdt').open("rb"), "sha256").hexdigest()})
    X, y, rows = prepared["s02"]
    if sources[0]["eeg_channels"] != sources[1]["eeg_channels"]:
        raise ValueError("Held-out session channel order mismatch")
    # Trial IDs keep their original sequence even after exclusions. No window shuffling.
    train = np.array([r["trial"] < 300 for r in rows])
    gap = np.array([300 <= r["trial"] < 350 for r in rows])
    test = np.array([r["trial"] >= 350 for r in rows])
    if set(np.unique(y[train])) != {0, 1}:
        raise ValueError("Training requires both classes")
    model = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))
    model.fit(X[train], y[train])
    joblib.dump({"model": model, "config": CONFIG, "channels": sources[0]["eeg_channels"]}, output / "baseline.joblib")
    sets = {"s02_late_holdout": (X[test], y[test], [r for r, t in zip(rows, test) if t]),
            "s03_cross_person_holdout": prepared["s03"]}
    results, predictions = {}, []
    rng = np.random.default_rng(CONFIG["seed"])
    for name, (test_X, test_y, test_rows) in sets.items():
        scores = model.predict_proba(test_X)[:, 1]
        results[name] = summarize(test_y, scores)
        # Evaluation-label permutation sanity reference; not a physiological significance test.
        null = [balanced_accuracy_score(rng.permutation(test_y), scores >= CONFIG["threshold"]) for _ in range(100)]
        results[name]["label_shuffle_reference_95pct"] = np.percentile(null, [2.5, 97.5]).tolist()
        for row, score in zip(test_rows, scores):
            alert = bool(score >= CONFIG["threshold"])
            predictions.append({"mode": "replay", "evaluation": name, "event_id": f"{name}-{row['trial']}",
                                "score": float(score), "alert": alert, "true_label_for_evaluation": row["label"],
                                "message": "疑似错误相关脑电反应，请核查" if alert else "未触发预警"})
    with (output / "predictions.jsonl").open("w", encoding="utf-8") as f:
        for p in predictions:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    report = {"mode": "public_data_offline_replay", "config": CONFIG, "sources": sources,
              "split": {"train_original_trial_ids": "s02 0..299", "gap_unused": "s02 300..349",
                        "test_original_trial_ids": "s02 350..499", "train_n": int(train.sum()), "gap_n": int(gap.sum())},
              "results": results, "environment": {"python": platform.python_version(), "numpy": np.__version__,
              "scipy": scipy.__version__, "sklearn": sklearn.__version__},
              "limitations": ["Public archived data, no device or synchronization validation", "Two subjects only; no tuning or population inference",
                              "Color feedback and return motion may confound labels; not proof of ErrP specificity",
                              "Existing reference/downsampling and acquisition delay are inherited",
                              "Posterior scores are not calibrated personal probabilities; artifacts may remain"]}
    (output / "metrics.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    from .report import write_report
    write_report(output)
    print(json.dumps(results, indent=2))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data/public_errp"))
    parser.add_argument("--output", type=Path, default=Path("reports/offline"))
    args = parser.parse_args()
    try:
        run(args.data, args.output)
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, f"数据或配置错误：{exc}\n")
