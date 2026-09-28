# Size extension — Run all checklist

```text
1. Copy repo → Drive:  MyDrive/stop-overthinking/code/
2. Colab A100 (80GB best) → open 15b → Runtime → Run all
3. Wait for FAST PATH ON ✓ · smoke · Stage A/B/C
4. New Colab → open 15a → Run all
5. Laptop: make_size_summary + make_all_results
```

| GPU | 4B batch | 0.8B batch |
|---|---|---|
| A100 **80GB** | 64 | 128 |
| A100 **40GB** | 32 | 64 |

**Must see** `FAST PATH ON ✓` before Stage A. Without it, speed is ~40 tok/s — stop.

Details: [4b/RUN.md](4b/RUN.md) · [0.8b/RUN.md](0.8b/RUN.md)
