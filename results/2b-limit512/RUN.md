# 2B · limit 512 fill-in — what happened

**Checked** from Drive zip `2b-limit512-20260929T161939Z-1-001.zip` (2026-09-29).  
Same **234** problems · **2 tries** · **limit512 only** (DECISIONS #81–#82).

## Main number

| Way | Accuracy | Thinking | All tokens | Cut off |
|---|---|---|---|---|
| **limit512** | **45.1%** | 492 | 2684 | 28% |

## How it sits next to other 2B ways

| Way | Accuracy |
|---|---|
| Thinking OFF | 40.8% |
| Thinking ON | 42.1% |
| **limit512** | **45.1%** ← this fill-in |
| LoRA-1 | 45.5% |
| **limit1024** | **49.8%** ← still best on 2B |

```text
limit512 helps vs ON (+3.0 points)
but limit1024 is still clearly better (+4.7 vs limit512)
```

So the empty chart cell is filled, and the main 2B story does **not** change: best free way stays **limit 1024**.

Raw: `results/2b-limit512/raw/` · Notebook: `16_qwen35_2b_limit512.ipynb`
