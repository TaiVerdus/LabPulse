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
3. **The state that matters has no single measurement.** Cognitive load and attention
   decline have no threshold and no gold standard — and asking an operator to report them
   breaks their flow. (Muscle fatigue is the exception: it *does* admit a measurable
   marker, which is exactly why this project anchors on it — see §2.)

The practical consequence: an operator who is heading toward an error gets no signal
until the error has already happened.

## 2. Research Direction

**LabPulse is a mirror, not a judge.** The system does not decide for the operator whether
they are fit to continue. It shows the operator their own signal against their own
baseline, and the operator decides. The premise of the whole project is this line:
*we can hardly define "tired", but we can help someone notice that they are tired.*

We therefore do not attempt to define or measure "tiredness" as a single construct. We
treat the operator's own baseline as the reference and ask a narrower, answerable question:

> **Can a deviation from an operator's own physiological baseline — a *state anomaly* —
> be detected while they are still working, and located on the SOP timeline?**

**Two complementary channels, deliberately asymmetric.** Each is validated against a
different control (§4), so neither is left to be judged against nothing:

| Channel | Target | Strength | Role |
|---|---|---|---|
| **EMG** (surface) | Action execution + **muscle fatigue** | Muscle fatigue has a textbook marker: surface-EMG **median frequency (MDF) declines** with sustained contraction. Measurable, repeatable, and visible as a trend **within a single subject** — no gold-standard-free guessing. | **Primary** |
| **EEG** | Cognitive load / attention | Strong at "something changed", weak at naming it: heavy artefact load, no gold standard for "cognitive load", and single-subject cognitive-state inference has no established solution. | **Complementary** |

This split is the single biggest design upgrade. Cognitive state is the target we care
about, but it is not the target we can *validate*; muscle fatigue is narrower, yet it is
measurable. We therefore anchor the primary objective on the channel that admits a
literature-backed marker, and carry EEG as a complementary channel reported honestly as
exploratory.

**SOP as the skeleton.** Rather than inferring the timeline from the signal, the SOP step
list supplies it: every signal window is attached to a known step ("dilution, step 3"). The
detector's output is therefore not an abstract "abnormal segment" but a **named,
interpretable statement — "dilution SOP step 3 deviated"** — which is what makes the
problem tractable and the result explainable to the operator.

**Primary objective**
Detect state anomalies within subject, against each operator's own baseline, and locate
them on the SOP timeline.

**Secondary objective (exploratory only)**
Observe cases in which a detected anomaly was followed by a recorded operational error.
Because spontaneous errors are rare, this is **hypothesis-generating observation, not a
tested causal claim** — see §6.

**An operational definition of "state anomaly"** (fixed before data collection, so the
detector can be judged):

> A state anomaly is a period in which a channel's indicator departs from the operator's
> own quiet-operation baseline by more than **X standard deviations**, and stays there for
> at least **Y seconds**.
>
> - **EMG indicator** (primary): median frequency (MDF) and amplitude (RMS) of the muscle
>   group active in the task.
> - **EEG indicator** (complementary): band-power ratios against that operator's own
>   baseline. Reported separately — **never merged into one score with EMG**, because the
>   two have different time constants and different evidence strength.
>
> *X and Y are fixed per channel after the first two baseline sessions are analysed, then
> frozen for the rest of the study. The sustained-duration rule keeps a single blink or
> movement artefact from raising an alarm.*

## 3. What We Build: LabPulse

LabPulse is a desktop web application (Python + Streamlit, runs locally, no cloud, no
account) whose job is to make the study above possible. Five modules:

| # | Module | What it does |
|---|---|---|
| 1 | **Acquisition** | Receives live EEG and surface EMG from the laboratory's acquisition system and timestamps every sample against a single clock. |
| 2 | **SOP Timeline** | Records the procedure against the task's SOP step list. This step list is the **skeleton of the whole system** — it is what turns a signal into a *located* result. Step lists are **configuration files**, one per task (weighing / dilution / sampling), so the same code serves all three tasks. |
| 3 | **Event Marking** | One-click / hotkey marking during work ("step complete", "error noticed", free labels). Both hands are occupied during dilution; anything that requires typing will simply not happen. |
| 4 | **State Anomaly Detection** | Computes both channels' indicators (EMG MDF/RMS primary, EEG band ratios complementary), compares each against the operator's own baseline, and flags sustained deviations using the frozen X / Y rule — **attributed to a named SOP step**. |
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

**Each channel gets its own positive control.**

**Control 1 — white noise → validates the EEG (cognitive-load) channel.**
White noise is switched on for a fixed block: it adds exogenous load, requires no change to
the task, and is reproducible. If the EEG channel cannot separate quiet from noise-loaded
blocks *within the same operator*, it is not measuring anything usable. Fixed noise source,
fixed volume, same hardware every session. (Music was rejected: its rhythm enters the EEG
spectrum and contaminates the very band being measured.)

**Control 2 — within-session time-on-task → validates the EMG (muscle-fatigue) channel.**
Sessions are a fixed 90 minutes; the first 30 minutes and the last 30 minutes are compared
within the same session, and sustained work should lower MDF. This is the **validation
condition for the primary channel**, and it costs no extra session — the load is produced
by the real work itself.

**Calibration (optional, ~1 minute per session).** A brief sustained isometric hold
(20–30 s at a self-chosen level, held as steadily as possible) recorded at the start and
the end of each session gives a same-session, task-independent reference for MDF decline.
It is a *relative* before/after contrast, not an absolute force measurement. Whether it is
needed is decided after the baseline sessions — see the risk table in §8.

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
| S2 | X / Y thresholds fixed **per channel** and documented before the noise block | frozen, written down | Week 2 |
| S3 | **EEG channel**: white-noise blocks show a detectable shift versus that operator's own quiet baseline | 3/3 operators | Week 4 |
| S4 | **EMG channel (primary)**: within-session MDF trend, first 30 min vs last 30 min | computed for 12/12 sessions; decline visible in ≥2/3 operators — otherwise the §4 calibration fallback is activated, and a null result is reported as a null result | Week 4 |
| S5 | SOP mark aligns to the signal timeline | error < 1 s | Week 1 |
| S6 | A full session (acquire → mark → review → export) runs unassisted | 1 operator, no help | Week 4 |
| S7 | End-to-end live demonstration completes in under 3 minutes | pass | Demo Day |

**Interpretation rule.** S3 and S4 are *feasibility* results, not universal claims. Three
operators showing an effect supports "detection is feasible in this setting"; it does not
establish that it generalises, and it will not be written as if it did.

## 6. Scope — What We Explicitly Do Not Do

- **No automatic decision.** The system never gates the operator's work and never says
  "stop". It is a mirror, not a judge (§2).
- **No causal claim that anomaly detection reduces errors.** That requires a controlled
  feedback-vs-no-feedback comparison and is out of scope for this study.
- **No induced errors.** Errors will not be manufactured in real laboratory procedures;
  the real materials belong to an ongoing project.
- **No cross-operator or cross-task comparison.** Person and task are perfectly
  confounded by design (§4).
- **No automatic state *classification* into named states** (e.g. "fatigued",
  "overloaded"). The output is an anomaly flag located on a step, nothing more.
- **No single fused "state score"** merging EMG and EEG (see §2).
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
- **Blocking pre-condition (must be resolved before data collection).** Surface EMG uses a
  bipolar electrode pair, whereas the EEG montage is single-ended (referenced). Whether the
  two can be recorded **in the same session on the same amplifier** must be confirmed
  against the manufacturer's manual *before the protocol is frozen*. This is a **blocking**
  item, because EMG now carries the primary objective (§2). Options, in order of
  preference:
  (a) both channels on the same system;
  (b) EMG on a separate channel group or device, synchronised to the same clock;
  (c) EMG only, with the primary objective rescoped to muscle fatigue and EEG moved to a
  later stage. **Option (c) is a real downgrade and would be declared as one** — not
  presented as the same study.
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
| EMG and EEG cannot be recorded together (**blocking**) | §7 options (a) → (b) → (c); option (c) rescopes the primary objective and is declared as a downgrade |
| MDF decline in intermittent lab tasks too small to see within 90 minutes | Activate the §4 sustained-hold calibration; if still null, lengthen the session or raise task load — and report the null result as a null result |
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
  design review of the original tool-only framing. Two upgrades were adopted in that
  review: (i) **surface EMG was promoted to the primary channel** (muscle fatigue has a
  measurable marker, cognitive state does not) with EEG kept as a complementary channel;
  and (ii) **the SOP step list became the skeleton** of the result, so the output is
  "which step deviated" rather than a timeline inferred from signal. The same review fixed
  three other decisions: state-anomaly detection as the primary objective, a three-operator
  within-subject design, a white-noise positive control, and no induced errors. This
  supersedes the earlier proposal. Both the original framing and the reason for the change
  are retained, as required by the course rule that every review submits *current version +
  process evidence + next-round decision*.

---

*Stage 1 submission — 2026-10-13. Pending: repository URL, LMS template check,
solo-work confirmation.*
