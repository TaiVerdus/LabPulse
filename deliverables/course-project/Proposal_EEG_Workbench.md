# Project Proposal — LabPulse: A Wet-Lab Operator State Logging & Visualization Desktop Web Application

**Course**: 44511105 Project-Based CST&AI Foundations (Fall 2026), AI-Assisted Real-World Projects
**Author**: Shixian Wang (Intelligent Medical Engineering · Brain-Computer Interface track)
**Date**: October 13, 2026 (draft v1.0, October 3)
**Team**: Individual project (solo plan submitted; pending course team confirmation)

---

## 1. Problem

Wet-lab research (e.g., pipetting, serial dilution, sampling) is made of long chains of **repetitive, precision** operations. Two problems show up again and again in this kind of work:

1. **Errors are discovered too late.** A mislabeled tube or a miscalculated dilution factor is usually caught downstream — hours later, or never. By then, tracing "when and why it went wrong" is almost impossible.
2. **The operator's state is invisible.** Human-factors research shows that cognitive overload (the brain cannot keep up) and attention decline are the main error sources in procedural work, yet in real labs the operator's cognitive state is **never objectively recorded**. Only two tools exist: self-report (unreliable, and it interrupts the work) and video review (accurate, but extremely time-consuming — nobody re-watches two hours of footage to catch that five-second mistake).

What is missing is a **low-friction, non-interrupting** logging tool: let the operator mark events with one click while working (which step is done, what error was noticed), then replay them afterwards **on the same timeline as the physiological state signals (EEG)**. This turns "I think I messed up somewhere after about an hour" into a searchable, replayable record.

This project comes directly from my research in the AI4S³ Laboratory (supervisor: Dr. Hang Dong): within an ongoing "50-tube materials separation" project, I am responsible for the Wednesday sampling & dilution module. The real research question behind it — the link between operator state and operational errors — is the subject of my first-year feasibility study. **The course project builds the tool; the research uses the tool.** This is a tool-building engineering project, not a human-subjects study.

## 2. Final Product Definition

**The final deliverable of this course is a complete desktop web application: LabPulse.**
It runs locally on a Windows laptop and is used through a browser — no cloud service, no account, no internet dependency; all data stays on the machine. A one-click launcher script (`.bat`) is provided, so even someone who cannot program can open it and use it.

The finished product contains **four core modules + four extended modules**:

**Core modules**

1. **Import & Trust** — load an EEG file (EDF/BDF/CSV) and instantly show a signal-quality panel (per-channel noise floor, flat-channel flag, line-noise ratio, spike count), reusing the analysis core I already wrote and validated during device acceptance.
2. **Live Event Marking** — one-click / hotkey event buttons ("step done", "error noticed", and custom labels); each mark carries a precise timestamp and never interrupts the work.
3. **Synchronized Review** — operation timeline × EEG band-power curves (δ/θ/α/β relative power) on one chart; click any event to jump to the brain state around it.
4. **Structured Export** — session log (events + timestamps + quality flags) exported as CSV, ready for analysis.

**Extended modules**
5\. **Device Integration** — import real sessions recorded by my own 16-channel device, with channel names mapped to the standard 10–20 montage.
6\. **Live Mode** — data arrives via LSL (or simulated-live from a file), the timeline keeps refreshing, with scrolling α/θ indicators.
7\. **Session Management** — history of past sessions; re-open any session to add or correct marks.
8\. **Polish** — consistent visuals, empty-state and error messages, and a demo script.

## 3. Target Users & Needs

**Primary users**: researchers who perform repetitive precision operations

| #  | Need                                                                        | Evidence                                                                                                  |
| -- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| N1 | **One-click event marking** during work, without breaking the flow           | My own dilution sessions: both hands are occupied; any logging that requires typing will simply not happen   |
| N2 | Review the "operation timeline" and the "EEG state curves" side by side afterwards | Group meeting (9/26): "record first, lock the research axis later" — recording infrastructure comes before analysis |
| N3 | Immediately know whether a recording's signal quality is trustworthy        | Device acceptance testing: signal-quality checking is the first thing any EEG recording needs                |
| N4 | Export structured session logs for later analysis                           | The research plan lists the "session-structure log" as one of five RQ-independent mandatory recording assets |
| N5 | Re-open a past session afterwards to add or correct marks                    | Real workflow: corrections happen after the session ends, not during it                                     |

**Secondary users** (validation only): classmates with no lab background

## 4. Success Metrics

| #  | Metric                                                                                    | Target                             | Verified at |
| -- | ----------------------------------------------------------------------------------------- | ---------------------------------- | ----------- |
| S1 | A user completes a full session (import → annotate → review → export) unassisted           | 100% of test users                 | Stage 3     |
| S2 | Low-quality channels (flat / too noisy / line-noise) flagged automatically on import        | Correctly flags known-bad channels | Stage 2     |
| S3 | Event timestamps align with the EEG timeline                                               | error < 1 s                        | Stage 2     |
| S4 | Task completion rate with 3+ users with no lab background                                  | ≥ 80%                              | Stage 3     |
| S5 | A session recorded on my own device during real wet-lab work is imported and visualized    | done before Demo Day               | Stage 5     |
| S6 | Live mode (LSL or simulated) runs 5 minutes continuously without interruption              | done before Demo Day               | Stage 5     |
| S7 | End-to-end live demo on Demo Day with no errors, under 3 minutes in total                  | pass                               | Stage 5     |

## 5. Stakeholder Communication (Evidence)

| Stakeholder | Role | What was communicated | Evidence |
|---|---|---|---|
| Dr. Hang Dong | Research supervisor **and** course instructor | Research framing (operator-state recording as infrastructure for a two-axis error study: cognitive overload / attention decline); approval to build the tool as the course project | Group meeting notes, Sep 26, 2026 |
| Materials separation project team | Context & workflow provider | Existing 50-tube pipeline: bench workflow, video setup, SOP; my assigned Wednesday sampling/dilution module | Group meeting notes; project onboarding |
| Equipment supplier's lab (independent third party) | Hardware & technical support | 16-channel device selection rationale, driver/software bundle, acceptance-testing guidance | Supplier communication records; delivered software bundle |
| Course teaching team | Scope approval | Solo-work plan (pending confirmation) | Email/LMS record (to be added) |

### 6. Product Scope & PRD Summary

Full PRD attached (`MVP_PRD.md`). In one paragraph:

LabPulse is a Streamlit desktop web application (pure Python) that imports EEG recordings, checks quality automatically, supports one-click event marking while working, replays the operation timeline against EEG band-power curves, exports structured session logs, manages past sessions, and — in its final form — receives live data from my own 16-channel device via LSL. Its signal-quality module **reuses `acceptance_check.py`** — the analysis core I wrote and validated during device acceptance (course objective: "modularity & reuse"). Public EEG datasets (PhysioNet EEG Motor Movement/Imagery Dataset) serve as the demo baseline, so **the core product never depends on whether the hardware arrives or works**; device integration and live mode are extended modules, each with a defined fallback path.

## 7. Delivery Timeline & Risk Control

**Scope statement**: This is a solo project by a first-year student alongside a full course load (4–6 h/week). Ambition is bounded by design: four core modules, one language, one reusable analysis core. **Explicitly out of scope**: automatic cognitive-state classification (that is the research question, not a course deliverable), multi-user accounts, cloud deployment, mobile app.

**Path to the complete product**:

| Course milestone | Date | Product state | Fallback if blocked |
|---|---|---|---|
| Stage 2: MVP | Oct 27 | Core modules 1–4 working on public datasets | Public dataset *is* the baseline |
| Stage 3: Validation | Nov 10 | 3-layer users: myself (real Wednesday sessions) → labmates → 3 naive classmates; revision plan | Simulated-session protocol |
| Stage 4: Beta | Dec 1 | + module 5 (device integration) + module 7 (session management) | Simulated-live mode stands in |
| Stage 5: Demo Day | Dec 8 | **Complete application**: modules 1–8, polished UI, live demo | Pre-recorded video + public-data live run |

**Risk control for the extended modules** (the core four are never at risk):
- LSL unstable → simulated-live mode substitutes; user-visible behavior is identical
- Device data unavailable → public dataset + any available device recording
- Bad-channel interpolation suggestion → droppable without affecting other modules
- Time overrun → module 8 (polish) is scheduled last; modules 5–7 are independently droppable

## 8. Ethics, Data & AI Compliance

- **Human data**: v1 records only myself as the operator (within-subject feasibility design); ethics clearance for this recording confirmed with my supervisor (no obstacle). No other person's physiological data is collected in the course project.
- **Privacy**: any wet-lab video used for cross-checking will avoid capturing faces or be desensitized before use. All application data stays on the local machine.
- **Public dataset**: PhysioNet EEG Motor Movement/Imagery Database (Schalk et al.), used under its open license with attribution.
- **AI use**: AI tools are used as implementation assistants under course AI-compliance rules; all AI interactions are logged, AI-generated code is flagged in comments, and design decisions (problem definition, product scope, metrics) are my own. No sensitive data (unpublished research data, credentials) is shared with external AI tools.

---

*Draft v1.0 — pending: LMS template check, solo-work confirmation, stakeholder review by Dr. Dong.*
