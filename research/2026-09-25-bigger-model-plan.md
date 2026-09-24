# A bigger model? The "surety gate" plan (idea, not decided) — 2026-09-25

The user asked: can we try a different, bigger model (A100 or H100), and how can we be **sure** that LoRA
training will work before we spend money? Nothing here is decided yet. Nothing is checked unless it says so.

## 1. What our results say about when training can work

Shortest-correct training can only shorten thinking that **finishes** and is **correct**.
It cannot fix **loops** (thinking that never finishes). Our Qwen3.5-2B mostly loops
(69.5% of thinking ON's cut-offs, results/full-results/FULL-RESULTS.md §9). So before training a new model,
first measure which kind of waste it has.

## 2. The surety gate (cheap, before any training)

40 problems (MBPP+, HumanEval+, LiveCodeBench easy + medium), thinking ON, 4 tries, a big limit (16k), and
stop generation when the text repeats (so loops end fast and are recorded).

| Measure | Our 2B model | Suggested GO rule (to be fixed in DECISIONS before running) |
|---|---|---|
| Share of answers that loop | about 30% of all ON answers (132 loops / 468) | ≤ 10% |
| TARGET (kept ÷ average correct length) | 0.829 MBPP+ · 0.987 LCB | ≤ 0.75 |
| Problems with ≥ 2 correct of 4 | 111/200 MBPP+ · 12/80 LCB | ≥ 50% on every set |

A NO-GO result is still useful: it tests the "loops" explanation on a second model.

## 3. Testing "without a limit"

Not possible (loops never end, and one looping answer holds up a whole batch). Use a big limit (16k/32k)
**plus** a repetition stop, and test ON-big-limit and the 1,024 limit side by side.

## 4. Model choice

A bigger model of the **same family** (Qwen3.5, ~7–9B if it exists), with the thinking switch, so only the
size changes.

## 5. Not checked

- Which Qwen3.5 sizes exist and their Hugging Face names.
- Whether the Colab A100 is 40 GB or 80 GB (notebook 14 step 2 prints it).
- H100 price in Colab units and its real speed-up.
- Cost of the gate (guess: 5–10 units) and of a full run (guess: several times our 38 units).
- Whether a repetition stop works with our answering script (`scripts/gen_colab.py`) — it does not have one today.

## 6. Constraints

- Deadline: about 2026-09-27 (one week from 2026-09-20, DECISIONS #48).
- Units: about 30 left; the 20-unit floor (DECISIONS #65) leaves about 10.
- Recommendation given: finish writing the thesis first; run the gate only if time and units allow.
