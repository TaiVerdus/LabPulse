# Product Requirements Document — LabPulse (Desktop Web Application)

**Course**: 44511105 Project-Based CST&AI Foundations (Fall 2026) — Projects, Stage 1 attachment
**Author**: Shixian Wang · **Date**: October 13, 2026 (draft v1.0, October 3)
**Companion document**: `Proposal_EEG_Workbench.md`
**Note on naming**: MVP (Oct 27) and Beta (Dec 1) are *milestones of this document's product*. The product itself is the complete desktop web application delivered at Demo Day.

---

## 1. Product Overview

LabPulse is a **desktop web application** for wet-lab operators: it runs locally on a Windows laptop, is used in a browser, requires no account and no internet, keeps all data on the machine, and starts from a one-click launcher (`.bat`). In one sentence: **"a black-box flight recorder for lab work."**

## 2. Final Product Module Map

| # | Module | What it does | Delivered | Fallback |
|---|---|---|---|---|
| 1 | Import & Trust | Load EDF/BDF/CSV; per-channel quality panel (noise floor, flat flag, 50 Hz ratio, spikes) | MVP (Oct 27) | — (core) |
| 2 | Live Event Marking | One-click/hotkey event buttons, precise timestamps, live mark list, editable afterwards | MVP (Oct 27) | — (core) |
| 3 | Synchronized Review | Operation timeline × band-power curves (δ/θ/α/β); click event → jump to ±30 s | MVP (Oct 27) | — (core) |
| 4 | Structured Export | Session log → CSV (event_id, timestamp, label, quality summary, source file) | MVP (Oct 27) | — (core) |
| 5 | Device Integration | Import real 16-ch device sessions; map channels to standard 10–20 montage | Beta (Dec 1) | public dataset |
| 6 | Live Mode | LSL stream (or file replay) with rolling α/θ indicators | Demo Day (Dec 8) | simulated-live mode |
| 7 | Session Management | Session history; re-open and re-annotate past sessions | Beta (Dec 1) | — |
| 8 | Polish | Consistent visuals, empty states, error messages, demo script | Demo Day (Dec 8) | partial polish acceptable |

Modules 1–4 are the **core product** and are never at risk. Modules 5–8 are independently droppable; dropping any one leaves the application complete in its core function.

## 3. User Stories

**US-1 — Trustworthy import.** *As a lab operator, I want to import an EEG recording and immediately see whether its quality is trustworthy, so I don't waste a session analyzing garbage data.*
Acceptance criteria: accepts EDF/BDF/CSV via file picker; quality panel shows per-channel noise floor (μV), flat-channel flag, line-noise ratio, spike count (computed by the `acceptance_check` core); failing channels highlighted; overall verdict (OK / CHECK / BAD) shown.

**US-2 — One-click marking.** *As an operator with both hands busy, I want to mark events by one click or hotkey during work, so logging never interrupts the procedure.*
Acceptance criteria: configurable buttons (label + color); timestamp error < 1 s vs. EEG clock; marks listed live; marks editable afterwards; ≥ 10 marks per session without performance loss.

**US-3 — Synchronized review.** *As an operator, I want my operation timeline and the EEG band-power curves on one synchronized chart, so I can jump from any event to the surrounding brain state.*
Acceptance criteria: event marks rendered as vertical lines on the EEG timeline; clicking a mark zooms to ±30 s; band power computed by Welch's method (MNE-Python), 4 s window, 50% overlap.

**US-4 — Structured export.** *As a researcher, I want to export a structured session log as CSV, so it feeds directly into later analysis.*
Acceptance criteria: CSV fields = event_id, timestamp (ISO + seconds-from-start), label, channel-quality summary, source file; sample export opens cleanly in Excel/pandas.

**US-5 — My own device.** *As a researcher, I want to import a session recorded on my own 16-channel device during real wet-lab work, so the tool serves my actual research.*
Acceptance criteria: device EDF/CSV imports without format errors; channel names mapped to 10–20 montage.

**US-6 — Live mode.** *As a researcher, I want the timeline to update continuously from a live stream, so I can watch state evolve while working.*
Acceptance criteria: LSL stream (or file replay when LSL unavailable) updates the chart continuously; α/θ indicators refresh every few seconds; runs 5 minutes without interruption.

**US-7 — Session management.** *As a researcher, I want to re-open a past session hours later to add or correct marks, so the log stays accurate.*
Acceptance criteria: session history list with time and file name; re-opening restores all marks; edits persist to the exported CSV.

**US-8 — Demo readiness.** *As a student presenting on Demo Day, I want the app to survive a live audience, so the demo does not fail.*
Acceptance criteria: one-click launcher starts the app on a clean machine state; empty states and error messages are shown instead of stack traces; end-to-end demo (import → mark → review → export) completes in < 3 minutes.

## 4. Technical Assumptions & Architecture

- **Language**: Python only (matches my concurrent programming course — one learning curve)
- **App framework**: Streamlit — local desktop web app, browser-based, demoable
- **EEG processing**: MNE-Python (filtering, Welch PSD, montages); NumPy/pandas
- **Reuse**: signal-quality module imported from `acceptance_check.py` (course objective: modularity & reuse); no copy-pasted third-party code
- **Streaming**: pylsl with the supplier-provided OpenBCI_LSL bridge; simulated-live replay as fallback
- **Hardware (modules 5–6 only)**: ExpandableBCI 16-channel (ADS1299), 250 Hz — never required for the core
- **Delivery form**: one-click `.bat` launcher; all data stored locally (privacy + offline use)
- **Version control**: Git from day one; meaningful commit messages per feature/fix
- **Layered architecture** (interface–implementation separation):
  1. `data/` — file parsing, montage mapping (file → MNE Raw object)
  2. `analysis/` — quality checks, band power (pure functions, unit-testable, no UI code)
  3. `session/` — event marking, timestamp alignment, persistence, export (state management)
  4. `ui/` — Streamlit pages calling the layers below; no signal math in UI code
- **Environment**: Windows 11 laptop; managed Python venv; no admin rights required

## 5. Test Plan (critical paths)

| # | Critical path | Test | Evidence |
|---|---|---|---|
| T1 | Import | Import every public-dataset file format used in the demo | Import log + screenshot |
| T2 | Quality flags | Known-bad recording (deliberately broken channel) must be flagged | Before/after panel screenshots |
| T3 | Timestamp alignment | Mark events at known times in a synthetic session; export must match within 1 s | Export CSV vs. ground truth |
| T4 | Export integrity | Exported CSV re-opens in pandas; all fields present, no NaN column | Test script output |
| T5 | Persistence | Re-open a session after 24 h; marks and edits intact | Screenshot + CSV diff |
| T6 | Live stability | Live mode runs 5 minutes without interruption or drift | Runtime log |
| T7 | Demo robustness | End-to-end demo on a clean start, timed | Timing log + recording |
| T8 | Regression | Re-run T1–T7 after each validation fix | Test log per iteration |

## 6. Out of Scope (explicit)

Automatic cognitive-state classification (research question, not course deliverable) · multi-user/accounts · cloud deployment · real-time feedback or intervention · mobile app.

## 7. Open Questions

- Solo-work confirmation from course team
- LMS proposal template may impose format changes (will adapt on receipt)
- If hardware acceptance fails, module 5 stays on public data and module 6 ships as simulated-live only (already planned)
