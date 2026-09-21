# Q&A 24: The free "go / no-go" test, before any money is spent

⬅️ [All Q&A](README.md) · Hard word? See [GLOSSARY.md](../GLOSSARY.md) · Decision: [DECISIONS #59](../DECISIONS.md)

---

## 1. The step in 2 sentences

Before paying for a faster GPU, we test the whole plan on the free Colab T4. Notebook 12 now
checks 4 things for free: whether the T4's number format breaks the model, whether the model is
good enough on easy **and** medium problems, whether there is room to shorten, and how fast it is.

```text
FREE T4 test ──► all pass? ──► yes ──► fast enough? ──► yes ──► stay free
     │                                     └──► no ──► NOW pay $10 (L4)
     └──► fails ──► try the 4B model (free) ──► fails ──► stop and rethink, $0 lost
```

---

## 2. Questions a teacher may ask

**Q: Why not just buy the faster GPU from the start? It is only $10.**
The money is not the problem. The problem is paying and **then** finding out the plan does not
work. Imagine the model is too weak on medium problems: a faster GPU would only get us that bad
news faster. Testing for free first means a failure costs nothing.

**Q: What is the "float16 garbage" risk?**
Numbers inside a model are stored in a format. Qwen was trained in **bfloat16**. The free T4 is
an older GPU from 2018 and cannot use it, so it uses **float16** instead. float16 cannot hold
very big numbers. If one gets too big ("overflows"), the model can write garbage. It usually works,
but "usually" is not good enough when every result depends on it.

**Q: How do you check it?**
We ask 10 easy problems twice: once in float16, once in **float32**. float32 is bigger and
cannot overflow, so it is the honest reference. If float16 passes at most 1 problem fewer, and
has no more garbage answers, float16 is safe. Otherwise every run uses float32. It is slower,
but still free. The rule was written **before** the run.

**Q: Why did you add medium problems to the test?**
The old test used only 30 easy HumanEval problems. A 2B model will probably do well on those.
The real risk is **medium** problems. A test that skips the risky part cannot tell us anything
we need. So we added 20 medium LiveCodeBench problems, and check the gates **separately** for
easy and medium.

**Q: What is vLLM, and why test it now?**
vLLM is free software built only for writing answers fast. We don't use it for the thesis yet,
because it has a known bug with LoRA add-ons (DECISIONS #57). But if the free T4 is too slow, we
need to know whether vLLM would even run **before** paying for a GPU because of it. So the last
step of the notebook just tries it and prints its speed.

---

## 3. Hard questions

**Q: Does a result from the free T4 still count if you later move to a paid GPU?**
The **accuracy** gates are about the model, not the machine, as long as the number format is
not breaking it. That is exactly what the float16 check makes sure of. The **speed** number is
only about the T4, and we use it only to decide whether to pay.

**Q: You found two bugs while making this. What were they?**
First: asking for "20 LiveCodeBench problems" would have given 20 **easy** ones, because the
problems are sorted easy first. So we added a `--difficulty` option. Second: the notebook kept its
own copy of the model in GPU memory (~5 GB) while the scripts load another. With float32 (~9 GB)
that would not fit in 15 GB. The notebook now frees its copy first. Neither bug would have
crashed on the easy path, which is why they were easy to miss.

**Q: What if the model passes on easy but fails on medium?**
Then it is too weak for our scope, which is easy **and** medium code. The table says: try the
4B model, still free. If the 4B also fails on medium, we stop and rethink the scope, for example
easy problems only. That would be a real change to the thesis, so we would decide it together.

---

## 4. What we checked, and what we only assume

| ✅ We checked this | ❌ We only assume this |
|---|---|
| The T4 has no bfloat16 (its specs; the notebook prints it) | That float16 is safe for Qwen3.5-2B |
| The old test used only easy problems | That the pilot takes 1–3 hours |
| `check_gates.py` reads the LiveCodeBench grades too (same columns) | That vLLM installs and runs on a T4 |
| The notebook file is valid (28 cells) | Any speed number: none is measured on Colab yet |

---

## 5. Where this is written down

- **Decision:** [DECISIONS.md](../DECISIONS.md) row #59
- **Roadmap:** [ROADMAP.md](../ROADMAP.md) "You are here" and "What to do next"
- **Code:** `notebooks/12_qwen_colab.ipynb` (steps 6b, 7–9, 10, 11),
  `scripts/gen_colab.py` (`--dtype`, `--difficulty`), `scripts/try_vllm.py`
- **Words:** [GLOSSARY.md](../GLOSSARY.md): bf16/float16/float32, go / no-go test, vLLM
