# Extra scores (written by the run)

<!-- CURRENT-STUDY:START -->

**Historical record below.** Its earlier scores, model choices and plans describe that stage only.
Use the current results linked here for the completed study.

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../CURRENT-RESULTS.md) · [Full easy thesis](../../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](../../thesis/THESIS.md).

<!-- CURRENT-STUDY:END -->

The old exam files were not changed.
This file is rewritten after every graded way, so a stopped run still has its scores.

- Old exam ids: 234
- Extra ids: 40
- Overlap: 0
- Total if added: 274

### 0.8b — old exam (frozen)

| Way | Accuracy | Passed |
|---|---|---|
| limit1024 | 13.2% | 31/234 |
| limit512 | 17.5% | 41/234 |
| lora1 | 17.9% | 42/234 |
| off | 20.5% | 48/234 |
| on | 7.3% | 17/234 |

### 0.8b — extra problems only

| Way | Accuracy | Passed |
|---|---|---|
| limit1024 | 0.0% | 0/40 |
| limit512 | 0.0% | 0/40 |
| lora1 | 0.0% | 0/40 |
| off | 5.0% | 2/40 |
| on | 0.0% | 0/40 |

### 0.8b — old plus extra

| Way | Accuracy | Passed |
|---|---|---|
| limit1024 | 11.3% | 31/274 |
| limit512 | 15.0% | 41/274 |
| lora1 | 15.3% | 42/274 |
| off | 18.2% | 50/274 |
| on | 6.2% | 17/274 |

### 2b — old exam (frozen)

| Way | Accuracy | Passed |
|---|---|---|
| brief | 6.6% | 31/468 |
| limit1024 | 49.8% | 233/468 |
| limit2048 | 46.6% | 109/234 |
| limit512 | 45.1% | 211/468 |
| lora1 | 45.5% | 213/468 |
| lora2 | 45.1% | 211/468 |
| off | 40.8% | 191/468 |
| on | 42.1% | 197/468 |

### 2b — extra problems only

| Way | Accuracy | Passed |
|---|---|---|
| brief | 5.0% | 4/80 |
| limit1024 | 8.8% | 7/80 |
| limit2048 | 7.5% | 3/40 |
| limit512 | 6.2% | 5/80 |
| off | 12.5% | 10/80 |
| on | 0.0% | 0/80 |

### 2b — old plus extra

| Way | Accuracy | Passed |
|---|---|---|
| brief | 6.4% | 35/548 |
| limit1024 | 43.8% | 240/548 |
| limit2048 | 40.9% | 112/274 |
| limit512 | 39.4% | 216/548 |
| off | 36.7% | 201/548 |
| on | 35.9% | 197/548 |

### 4b — old exam (frozen)

| Way | Accuracy | Passed |
|---|---|---|
| limit1024 | 76.5% | 358/468 |
| limit2048 | 78.2% | 366/468 |
| limit4096 | 76.7% | 359/468 |
| limit512 | 75.4% | 353/468 |
| lora1 | 69.9% | 327/468 |
| off | 69.7% | 326/468 |
| on | 64.3% | 301/468 |

### 4b — extra problems only

| Way | Accuracy | Passed |
|---|---|---|
| limit2048 | 46.2% | 37/80 |
| off | 46.2% | 37/80 |
| on | 18.8% | 15/80 |

### 4b — old plus extra

| Way | Accuracy | Passed |
|---|---|---|
| limit2048 | 73.5% | 403/548 |
| off | 66.2% | 363/548 |
| on | 57.7% | 316/548 |
