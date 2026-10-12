# LabPulse — Detecting Operator State Anomalies in Wet-Lab Work

**Stage 1 Project Proposal**

| | |
|---|---|
| **Course** | 44511105 Project-Based CST&AI Foundations (Fall 2026) — Projects module |
| **Author** | Shixian Wang |
| **Stage** | Stage 1 — Milestone submission |
| **Date** | 2026-10-13 |
| **Team** | Individual project (solo) |
| **Repository** | `<Git URL>` |

---

## 1. The Problem

Quality control in wet-lab work is **entirely retrospective**. A miscalculated dilution
factor or a mislabelled tube is usually discovered downstream — hours later, or never.
By the time the failure surfaces, the cause is unrecoverable: nobody knows which step
went wrong, let alone why.

Three things are missing from the current workflow:

1. **Errors are found too late.** By the time a batch fails, the responsible step is
   buried in a two-hour timeline with no markers.
2. **The operator's state is never recorded.** Human-factors research treats cognitive
   overload and attention decline as the main error sources in procedural work, yet in a
   real lab the operator's state is captured by nothing. The only two existing tools are
   self-report (unreliable, and it interrupts the work) and video review (accurate, but
   nobody re-watches two hours of footage to find a five-second mistake).
3. **"Tired" has no measurement.** There is no instrument reading for fatigue. We cannot
   put a threshold on it, and we cannot ask an operator to report it without breaking
   their flow.

The practical consequence: an operator who is heading toward an error gets no signal
until the error has already happened.

## 2. Research Direction

**We do not attempt to define or measure "tiredness".** We treat the operator's own
baseline as the reference, and ask a narrower, answerable question:

> **Can a deviation from an operator's own physiological baseline — a *state anomaly* —
> be detected while they are still working?**

This reframing is deliberate. "Fatigue" has no ground truth and no scale; "deviation from
this person's own baseline" is a computable quantity. The purpose of detecting it is
practical, not diagnostic: give the operator a chance to notice that something has
shifted, and choose to pause, re-check, or restart the step — *before* the error lands in
the data.

**Primary objective**
Detect state anomalies, within subject, against each operator's own baseline.

**Secondary objective (exploratory only)**
Observe cases in which a detected anomaly was followed by a recorded operational error.
Because spontaneous errors are rare, this is **hypothesis-generating observation, not a
tested causal claim** — see §6.

**An operational definition of "state anomaly"** (fixed before data collection, so the
detector can be judged):

> A state anomaly is a period in which a derived physiological indicator departs from the
> operator's own quiet-operation baseline by more than **X standard deviations**, and
> stays there for at least **Y seconds**.
>
> *X and Y are fixed after the first two baseline sessions are analysed, then frozen for
> the rest of the study.* The sustained-duration rule exists so that a single blink or
> movement artefact does not raise an alarm.

## 3. What We Build: LabPulse

LabPulse is a desktop web application (Python + Streamlit, runs locally, no cloud, no
account) whose job is to make the study above possible. Five modules:

| # | Module | What it does |
|---|---|---|
| 1 | **Acquisition** | Receives live EEG/EMG from the laboratory's acquisition system and timestamps every sample against a single clock. |
| 2 | **SOP Timeline** | Records the procedure against the task's SOP step list. Step lists are **configuration files** — one file per task (weighing / dilution / sampling) — so the same code serves all three tasks. |
| 3 | **Event Marking** | One-click / hotkey marking during work ("step complete", "error noticed", free labels). Both hands are occupied during dilution; anything that requires typing will simply not happen. |
| 4 | **State Anomaly Detection** | Computes the indicator, compares it to the operator's baseline, and flags sustained deviations using the frozen X / Y rule. |
| 5 | **Synchronised Review & Export** | SOP step timeline × physiological curves on one chart; click any mark to jump to the signal around it; export a structured session log as CSV. |

The signal-quality check reuses the analysis core already written and validated during
equipment acceptance, rather than re-implementing it (modularity & reuse).

**Alignment requirement.** The SOP timeline is human-marked (minutes) while the
physiological signal is continuous (milliseconds). Both must be stamped against the same
clock; mark-to-signal alignment error must stay **under 1 second**, or the two streams
cannot be correlated afterwards.

## 4. Study Design

**Participants and tasks — fixed assignment.**

| Operator | Task | Time slot |
|---|---|---|
| Operator A | Weighing | separate |
| Operator B (author) | Dilution | separate |
| Operator C | Sampling | separate |

Each operator performs **only their own task**; there is no crossover. This means person
and task are not separable, so **no comparison between operators or between tasks will be
claimed** (see §6). Each operator is analysed as an independent within-subject case:
three separate small experiments, each with its own baseline.

**Positive control 1 — auditory load (white noise).**
Because "state anomaly" has no external ground truth, we need a period in which an anomaly
*should* occur. White noise is switched on for a fixed block: it adds exogenous load,
requires no change to the task, and is reproducible. **This is the validation condition
for the primary objective** — without it, the detector's output cannot be judged right or
wrong. Fixed playlist/noise, fixed volume, same hardware for every session.

**Positive control 2 — within-session time-on-task (free).**
Sessions are a fixed 90 minutes. The first 30 minutes and the last 30 minutes are compared
within the same session: state anomalies should be more frequent later. This costs no
extra session and provides an ecologically valid contrast.

**Protocol and data volume.**

| Phase | Sessions per operator | Total | Calendar |
|---|---|---|---|
| Quiet baseline | 2 | 6 | 2 weeks |
| White-noise block | 2 | 6 | 2 weeks |
| **Total** | **4** | **12 sessions** | **4 weeks** |

Each session is 1–2 hours and is part of the operators' existing weekly laboratory
schedule — no additional sessions have to be created for this study.
Estimated yield: ~18 hours of recording ≈ **~2000 non-overlapping 30-second windows**,
with each operator carrying their own baseline. Adjacent windows are strongly correlated,
so the effective independent sample is much smaller; the binding constraint is the number
of **sessions**, not windows.

**Secondary (exploratory) analysis.** Operational errors are recorded as they are noticed
during work, or back-filled afterwards from a downstream result. With spontaneous error
rates around 1–2 per session, the study yields a few dozen events at most. This is far
below what a state↔error association test requires, so the secondary analysis is reported
as a set of documented cases, never as a correlation or a causal result.

## 5. Success Criteria

| # | Criterion | Target | Verified at |
|---|---|---|---|
| S1 | Two baseline sessions per operator completed and analysed | 3/3 operators | Week 2 |
| S2 | X / Y thresholds fixed and documented before the noise block | frozen, written down | Week 2 |
| S3 | White-noise blocks show a detectable shift versus that operator's own baseline | 3/3 operators | Week 4 |
| S4 | Within-session first-vs-last-30-min contrast computed | 12/12 sessions | Week 4 |
| S5 | SOP mark aligns to the signal timeline | error < 1 s | Week 1 |
| S6 | A full session (acquire → mark → review → export) runs unassisted | 1 operator, no help | Week 4 |
| S7 | End-to-end live demonstration completes in under 3 minutes | pass | Demo Day |

**Interpretation rule.** S3 is a *feasibility* result, not a universal claim. Three
operators showing the effect supports "detection is feasible in this setting"; it does not
establish that it generalises, and it will not be written as if it did.

## 6. Scope — What We Explicitly Do Not Do

- **No causal claim that anomaly detection reduces errors.** That requires a controlled
  feedback-vs-no-feedback comparison and is out of scope for this study.
- **No induced errors.** Errors will not be manufactured in real laboratory procedures;
  the real materials belong to an ongoing project.
- **No cross-operator or cross-task comparison.** Person and task are perfectly
  confounded by design (§4).
- **No automatic state *classification* into named states** (e.g. "fatigued",
  "overloaded"). The output is an anomaly flag relative to a personal baseline, nothing
  more.
- **No medical or diagnostic claim.** This is not a health device and will not be
  described as one.
- Multi-user accounts, cloud deployment, and mobile clients are out of scope.

## 7. Stakeholders, Ethics, and Data Compliance

| Stakeholder | Role | Status |
|---|---|---|
| Research supervisor | Scientific guidance and approval of the recording protocol | Approved |
| Operators B and C | Participants | Written informed consent obtained; data handling agreed |
| Course teaching team | Scope and milestone approval | Solo plan pending confirmation |
| Laboratory project team | Provides the real workflow and SOP | In place |

- **Human data.** Three operators, each consenting, each recorded only during their own
  task. Raw physiological data stays on the local machine and is not uploaded to any
  cloud service or external tool.
- **Privacy.** No video processing is part of this stage. Personal identifiers are kept
  out of exported datasets; operators are referred to as A / B / C in all analysis and
  write-ups.
- **Withdrawal.** Any operator may withdraw and have their recordings deleted at any
  point without giving a reason.
- **Open pre-condition (to be resolved before data collection).** Whether EEG and EMG can
  be recorded in the *same* session depends on the electrode configuration: surface EMG
  uses a bipolar pair, while the EEG montage uses a single-ended (referenced) arrangement.
  This must be confirmed against the manufacturer's manual before the protocol is frozen.
  If they cannot be recorded together, the study proceeds on EEG alone and the state
  indicator is derived from EEG only.
- **Standing rule.** No sensitive laboratory data, unpublished results, credentials, or
  participant information are shared with AI tools.

## 8. Timeline and Risk Control

| Milestone | Date | Target state |
|---|---|---|
| Stage 1 | Oct 13 | This proposal + repository link |
| Baseline sessions | Weeks of Oct 13–26 | 6 sessions, thresholds X / Y frozen |
| Stage 2 (MVP) | Oct 27 | Modules 1–5 working end-to-end on recorded sessions |
| Noise block | Weeks of Oct 27–Nov 9 | 6 sessions |
| Stage 3 (Validation) | Nov 10 | Detection results for 3/3 operators; revision plan |
| Stage 4 (Beta) | Dec 1 | Polished UI, real-session review, reliability pass |
| Stage 5 (Demo Day) | Dec 8 | Live end-to-end demonstration, < 3 minutes |

**Risks and fallbacks.**

| Risk | Fallback |
|---|---|
| EEG and EMG cannot be recorded together | Proceed on EEG only (see §7); the anomaly rule is unchanged |
| Recording cannot be attached to real sessions in some week | Use a surrogate practice task with the same motor actions; mark the session as surrogate in the log |
| Very few errors observed | Expected; the secondary analysis is already scoped as exploratory and does not gate any deliverable |
| Detection performs poorly | A negative result is a valid Stage 3 outcome, reported as such; it does not block the software deliverable |
| Session overruns available time | Sessions are already part of the weekly schedule; the protocol is capped at 90 minutes |

## 9. Process Evidence and AI Use

- **Repository history is short.** The LabPulse repository was first created on
  **2026-10-04**. Work before that date (initial problem framing, earlier draft documents)
  took place outside version control and therefore has **no reproducible commit
  timestamps**. This gap is stated here rather than papered over; it is also recorded in
  the AI usage log.
- **AI-assisted work is logged.** Every AI interaction that produced a change is recorded
  with a timestamp taken from the git commit, in `AI使用日志.md`. AI is used for
  drafting, implementation and verification; research questions, scope decisions and
  interpretation are the author's own.
- **Direction revision.** The project direction was revised on **2026-10-12** after a
  design review of the original tool-only framing. The revision (state-anomaly detection
  as the primary objective; three-operator within-subject design; white-noise positive
  control; no induced errors) supersedes the earlier proposal. Both the original framing
  and the reason for the change are recorded, as required by the course rule that every
  review submits *current version + process evidence + next-round decision*.

---

*Stage 1 submission — 2026-10-13. Pending: repository URL, LMS template check,
solo-work confirmation.*
