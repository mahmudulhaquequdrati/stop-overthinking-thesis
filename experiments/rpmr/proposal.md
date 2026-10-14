# A concrete invention candidate: Readout-Preserving Memory Repair

Date: 14 October 2026. Working name: RPMR.
Status: provisional method proposal, algebra checked; no model results or established novelty.
Research chain: GAP → QUESTION → HYPOTHESIS → METHOD DESIGN.

## 1. What we would invent

An internal repair operator for the temporary memory of a frozen Qwen3.5 model.
It shrinks selected loop-associated memory changes while preserving selected question-associated readouts.
A readout is the vector returned when a query reads the memory matrix.
Everyday example: remove repeated scribbles without changing selected readings of the task notes.
This analogy is a hypothesis. Numerical query directions are not certified semantic task facts.

The specific proposed contribution is:
**Online, query-constrained repair of recurrent DeltaNet memory during reasoning-loop recovery.**
Using a different model size or naming a score is insufficient novelty.
This proposal combines existing mathematics with a specific intervention surface and objective.
I found no exact match in the targeted search below. That does not establish priority.

## 2. Closest prior work and the actual differences

- [ReBalance](https://arxiv.org/html/2603.12372v1): confidence-controlled hidden-state steering.
  RPMR would edit a per-head cached memory matrix under selected query constraints.
- [SOPHIA](https://arxiv.org/html/2607.18100v1): detects self-loops and applies transition-conditioned
  residual-stream vectors. This rules out claiming online internal loop steering as new.
  RPMR would compute a local memory repair with an explicit immediate readout invariant.
- [AlphaEdit](https://arxiv.org/html/2410.02355v3): projects parameter edits to preserve associations.
  This is the preservation idea we borrow and must credit. RPMR would edit temporary
  inference memory, using current-prompt probes and online suspected-cycle drift.
- [SSM activation subspace bottlenecks](https://arxiv.org/html/2602.22719v1): scales selected
  Mamba activations at inference. RPMR proposes a constrained matrix edit, not general scalar scaling.
- [ACE](https://arxiv.org/html/2607.00588v1): subtracts a repetition-related feedback direction
  in continuous diffusion generation. RPMR instead uses autoregressive DeltaNet cache memory
  and a question-probe constraint. Removing a repetition direction alone is already prior work.
- [Dynamic Closed-Loop Steering](https://www.mdpi.com/2076-3417/16/13/6423): search-visible
  publisher text describes geometry-aware steering, PCA filtering, and anti-collapse perturbation.
  Its full page could not be opened; comparison is preliminary. It must be reviewed before submission.
- [Safin-1 / MARCH](https://arxiv.org/html/2609.00092v1): recurrent memory-history reading,
  including GDN backbones. This rules out claiming historical recurrent-memory recovery broadly.
- [Wait, Wait, Wait...](https://arxiv.org/html/2512.12895v1): studies learning errors and
  temporally correlated errors behind reasoning loops. It does not establish our models' cause.
- [Liquid AI Antidoom](https://www.liquid.ai/blog/antidoom): trains preferences at loop-trigger
  tokens. This rules out claiming targeted loop training as new.

Also found [MaLoRA](https://arxiv.org/abs/2607.19326), dynamic recurrent adapter scaling,
and [Efficient Reasoning on the Edge](https://arxiv.org/abs/2603.16867), adapter switching.
Abstracts checked. Dynamic LoRA control alone is not the recommended novelty claim.

Evidence depth: paper HTML inspected for the first five methods, MARCH, and the looping study;
publisher blog inspected for Antidoom. No cited method was reproduced in this session.
Search phrases included DeltaNet state editing, reasoning-loop null-space repair,
recurrent-memory loop projection, readout-preserving repetition, and Qwen3.5 memory repair.
The search was targeted, not exhaustive, and concentrated on publicly indexed papers.

## 3. The proposed mathematical operator

Use one head's key-by-value memory matrix S, matching Transformers' orientation.
The memory returns S^T q when queried with vector q.
Take U as an orthonormal basis for selected question-associated query directions.
Take C as candidate loop directions, estimated from already observed memory changes.
Define V = orth((I - UU^T)C), discarding zero or near-zero columns.
V contains the parts of suspected loop directions outside the protected query span.
S_ref is a stored checkpoint before the detected repeated span, not a correct-answer oracle.

The repair is:

    S_new = S - eta × VV^T(S - S_ref),       0 <= eta <= 1.

Plain meaning: move memory toward its earlier checkpoint only in eligible directions.
Leave all other directions alone. This is our candidate algorithm, not a new linear-algebra law.

## 4. What we can prove, and exactly where it stops

Because U^T V = 0:

    U^T S_new = U^T S.

Therefore selected query readouts are unchanged immediately by the repair.
Also:

    ||V^T(S_new - S_ref)||_F = (1 - eta) ||V^T(S - S_ref)||_F.

The targeted component of checkpoint drift shrinks by a known factor.
The Frobenius norm is the square root of the sum of squared matrix entries.
For eta = lambda/(1 + lambda), this is the unique minimizer of:

    min_X  1/2 ||X - S||_F^2 + lambda/2 ||V^T(X - S_ref)||_F^2
    subject to U^T X = U^T S,                    lambda >= 0.

The first term limits change; the second shrinks selected drift; the constraint protects readouts.
This is a standard quadratic optimization result. Do not claim the proof as new mathematics.

The result does NOT prove preservation of the question's meaning, final accuracy,
future readouts after more updates, or escape from a dynamical attractor.
It preserves current selected readouts, which might already contain errors.
Chosen prompt queries may fail to represent facts or requirements we care about.
Future updates, full attention, convolution, and nonlinear layers can change everything else.

## 5. Concrete online recipe to investigate

1. During prompt processing, collect query vectors at task-text tokens in one selected
   DeltaNet head. Use a low-rank basis U, chosen by a fixed development-data rule.
   A first prototype could keep at most eight principal directions; eight is a starting
   setting, not an optimized or justified research result.
2. During thinking, keep a small rolling buffer of selected memory snapshots.
3. Detect persistent repeated text using only the generated prefix. This is an existing
   detector, not the claimed contribution. Save its rules before confirmatory evaluation.
4. At detection, estimate C from the recent memory-update matrices using a low-rank
   left singular basis. A first prototype could keep at most four directions.
5. Construct V, and edit only that selected head's recurrent cache with the formula.
   Apply once per detected episode, then continue normal generation without forced closure.
6. Cap edit norm and intervention frequency; record skipped edits and all overhead.
   A scalar norm cap merely reduces effective eta and retains the immediate invariant.

If U spans the whole key space, no eligible edit exists: skip.
If cycle directions lie inside U, skip. Do not weaken protection silently.
If states are constant, the drift basis may be empty: skip.
Repeated text may reside in full-attention cache, so DeltaNet repair may fail completely.
Computing these directions is feasible in principle but GPU speed/memory are unmeasured.
Keep future diagnosis separate from claims that a singular vector is causally a loop circuit.

## 6. What would make this a defensible contribution?

Research question: does constrained recurrent-memory repair recover useful code answers
from loops better than existing output controls and unconstrained internal interventions?
Hypothesis: protecting selected query readouts reduces accuracy damage from loop repair.
What changes: no repair versus unconstrained repair versus query-constrained repair.
What is measured: first-answer code-test accuracy, loop rate, natural completion,
thinking/total tokens, wall time, and preservation residual on selected probes.
Data: separate development problems for tuning; fresh confirmation problems after freezing rules.
Comparisons: ON, OFF, fixed limits, repetition penalty, repeat stopping, forced closure,
whole-state rollback, unprotected projection, norm-matched random repair, ReBalance,
and SOPHIA or a clearly documented reproducible approximation.
Isolate detection effects using the SAME trigger across internal repair controls.
Use full 0.8B/2B/4B test distributions as well as a loop-enriched recovery diagnostic.
Evaluate base models first; add existing LoRA as an independent second factor afterward.
Support: real held-out improvement over simple controls, plus a benefit from protection
over unprotected edits. Compare the same problems across several seeds with uncertainty.
Contradiction: no better recovery, lost accuracy, no protection benefit, or equal random-edit gains.
Same total caps and decoding settings, same repeat handling, and benchmark test isolation apply.
All new-model pilot spending requires a resource estimate before execution.

## 7. Colab-only execution — 14 October 2026

Open 25_rpmr_colab_smoke.ipynb in Colab. Earlier local-only tools and duplicate
notes were archived and removed at the user's request. This proposal remains untested
on Qwen until the Colab notebook returns its saved report.
The smoke check is numerical and cache plumbing only, not online loop recovery.
Budget: 50 units remaining; preserve 20. Smoke session ceiling: at most five units.
The full pilot remains separate and disabled.
