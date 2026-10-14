# Appendices: the completed study

<!-- CURRENT-STUDY:START -->

**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

[Every method, benchmark, difficulty, token count and interval](../results/CURRENT-RESULTS.md) · [Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal Markdown thesis](THESIS.md).

<!-- CURRENT-STUDY:END -->

## Every test problem

All 464 frozen test IDs appear below. Training and pilot problems are excluded.
The 234/40/190 collection history is documented in the method, not treated as separate headline studies.

| Test ID | Benchmark | Difficulty |
|---|---|---|
| HumanEval/0 | HumanEval+ | easy |
| HumanEval/1 | HumanEval+ | easy |
| HumanEval/10 | HumanEval+ | easy |
| HumanEval/100 | HumanEval+ | easy |
| HumanEval/101 | HumanEval+ | easy |
| HumanEval/102 | HumanEval+ | easy |
| HumanEval/103 | HumanEval+ | easy |
| HumanEval/104 | HumanEval+ | easy |
| HumanEval/105 | HumanEval+ | easy |
| HumanEval/106 | HumanEval+ | easy |
| HumanEval/107 | HumanEval+ | easy |
| HumanEval/108 | HumanEval+ | easy |
| HumanEval/109 | HumanEval+ | easy |
| HumanEval/11 | HumanEval+ | easy |
| HumanEval/110 | HumanEval+ | easy |
| HumanEval/111 | HumanEval+ | easy |
| HumanEval/112 | HumanEval+ | easy |
| HumanEval/113 | HumanEval+ | easy |
| HumanEval/114 | HumanEval+ | easy |
| HumanEval/115 | HumanEval+ | easy |
| HumanEval/116 | HumanEval+ | easy |
| HumanEval/117 | HumanEval+ | easy |
| HumanEval/118 | HumanEval+ | easy |
| HumanEval/119 | HumanEval+ | easy |
| HumanEval/12 | HumanEval+ | easy |
| HumanEval/120 | HumanEval+ | easy |
| HumanEval/121 | HumanEval+ | easy |
| HumanEval/122 | HumanEval+ | easy |
| HumanEval/123 | HumanEval+ | easy |
| HumanEval/124 | HumanEval+ | easy |
| HumanEval/125 | HumanEval+ | easy |
| HumanEval/126 | HumanEval+ | easy |
| HumanEval/127 | HumanEval+ | easy |
| HumanEval/128 | HumanEval+ | easy |
| HumanEval/129 | HumanEval+ | easy |
| HumanEval/13 | HumanEval+ | easy |
| HumanEval/130 | HumanEval+ | easy |
| HumanEval/131 | HumanEval+ | easy |
| HumanEval/132 | HumanEval+ | easy |
| HumanEval/133 | HumanEval+ | easy |
| HumanEval/134 | HumanEval+ | easy |
| HumanEval/135 | HumanEval+ | easy |
| HumanEval/136 | HumanEval+ | easy |
| HumanEval/137 | HumanEval+ | easy |
| HumanEval/138 | HumanEval+ | easy |
| HumanEval/139 | HumanEval+ | easy |
| HumanEval/14 | HumanEval+ | easy |
| HumanEval/140 | HumanEval+ | easy |
| HumanEval/141 | HumanEval+ | easy |
| HumanEval/142 | HumanEval+ | easy |
| HumanEval/143 | HumanEval+ | easy |
| HumanEval/144 | HumanEval+ | easy |
| HumanEval/145 | HumanEval+ | easy |
| HumanEval/146 | HumanEval+ | easy |
| HumanEval/147 | HumanEval+ | easy |
| HumanEval/148 | HumanEval+ | easy |
| HumanEval/149 | HumanEval+ | easy |
| HumanEval/15 | HumanEval+ | easy |
| HumanEval/150 | HumanEval+ | easy |
| HumanEval/151 | HumanEval+ | easy |
| HumanEval/152 | HumanEval+ | easy |
| HumanEval/153 | HumanEval+ | easy |
| HumanEval/154 | HumanEval+ | easy |
| HumanEval/155 | HumanEval+ | easy |
| HumanEval/156 | HumanEval+ | easy |
| HumanEval/157 | HumanEval+ | easy |
| HumanEval/158 | HumanEval+ | easy |
| HumanEval/159 | HumanEval+ | easy |
| HumanEval/16 | HumanEval+ | easy |
| HumanEval/160 | HumanEval+ | easy |
| HumanEval/161 | HumanEval+ | easy |
| HumanEval/162 | HumanEval+ | easy |
| HumanEval/163 | HumanEval+ | easy |
| HumanEval/17 | HumanEval+ | easy |
| HumanEval/18 | HumanEval+ | easy |
| HumanEval/19 | HumanEval+ | easy |
| HumanEval/2 | HumanEval+ | easy |
| HumanEval/20 | HumanEval+ | easy |
| HumanEval/21 | HumanEval+ | easy |
| HumanEval/22 | HumanEval+ | easy |
| HumanEval/23 | HumanEval+ | easy |
| HumanEval/24 | HumanEval+ | easy |
| HumanEval/25 | HumanEval+ | easy |
| HumanEval/26 | HumanEval+ | easy |
| HumanEval/27 | HumanEval+ | easy |
| HumanEval/28 | HumanEval+ | easy |
| HumanEval/29 | HumanEval+ | easy |
| HumanEval/3 | HumanEval+ | easy |
| HumanEval/30 | HumanEval+ | easy |
| HumanEval/31 | HumanEval+ | easy |
| HumanEval/32 | HumanEval+ | easy |
| HumanEval/33 | HumanEval+ | easy |
| HumanEval/34 | HumanEval+ | easy |
| HumanEval/35 | HumanEval+ | easy |
| HumanEval/36 | HumanEval+ | easy |
| HumanEval/37 | HumanEval+ | easy |
| HumanEval/38 | HumanEval+ | easy |
| HumanEval/39 | HumanEval+ | easy |
| HumanEval/4 | HumanEval+ | easy |
| HumanEval/40 | HumanEval+ | easy |
| HumanEval/41 | HumanEval+ | easy |
| HumanEval/42 | HumanEval+ | easy |
| HumanEval/43 | HumanEval+ | easy |
| HumanEval/44 | HumanEval+ | easy |
| HumanEval/45 | HumanEval+ | easy |
| HumanEval/46 | HumanEval+ | easy |
| HumanEval/47 | HumanEval+ | easy |
| HumanEval/48 | HumanEval+ | easy |
| HumanEval/49 | HumanEval+ | easy |
| HumanEval/5 | HumanEval+ | easy |
| HumanEval/50 | HumanEval+ | easy |
| HumanEval/51 | HumanEval+ | easy |
| HumanEval/52 | HumanEval+ | easy |
| HumanEval/53 | HumanEval+ | easy |
| HumanEval/54 | HumanEval+ | easy |
| HumanEval/55 | HumanEval+ | easy |
| HumanEval/56 | HumanEval+ | easy |
| HumanEval/57 | HumanEval+ | easy |
| HumanEval/58 | HumanEval+ | easy |
| HumanEval/59 | HumanEval+ | easy |
| HumanEval/6 | HumanEval+ | easy |
| HumanEval/60 | HumanEval+ | easy |
| HumanEval/61 | HumanEval+ | easy |
| HumanEval/62 | HumanEval+ | easy |
| HumanEval/63 | HumanEval+ | easy |
| HumanEval/64 | HumanEval+ | easy |
| HumanEval/65 | HumanEval+ | easy |
| HumanEval/66 | HumanEval+ | easy |
| HumanEval/67 | HumanEval+ | easy |
| HumanEval/68 | HumanEval+ | easy |
| HumanEval/69 | HumanEval+ | easy |
| HumanEval/7 | HumanEval+ | easy |
| HumanEval/70 | HumanEval+ | easy |
| HumanEval/71 | HumanEval+ | easy |
| HumanEval/72 | HumanEval+ | easy |
| HumanEval/73 | HumanEval+ | easy |
| HumanEval/74 | HumanEval+ | easy |
| HumanEval/75 | HumanEval+ | easy |
| HumanEval/76 | HumanEval+ | easy |
| HumanEval/77 | HumanEval+ | easy |
| HumanEval/78 | HumanEval+ | easy |
| HumanEval/79 | HumanEval+ | easy |
| HumanEval/8 | HumanEval+ | easy |
| HumanEval/80 | HumanEval+ | easy |
| HumanEval/81 | HumanEval+ | easy |
| HumanEval/82 | HumanEval+ | easy |
| HumanEval/83 | HumanEval+ | easy |
| HumanEval/84 | HumanEval+ | easy |
| HumanEval/85 | HumanEval+ | easy |
| HumanEval/86 | HumanEval+ | easy |
| HumanEval/87 | HumanEval+ | easy |
| HumanEval/88 | HumanEval+ | easy |
| HumanEval/89 | HumanEval+ | easy |
| HumanEval/9 | HumanEval+ | easy |
| HumanEval/90 | HumanEval+ | easy |
| HumanEval/91 | HumanEval+ | easy |
| HumanEval/92 | HumanEval+ | easy |
| HumanEval/93 | HumanEval+ | easy |
| HumanEval/94 | HumanEval+ | easy |
| HumanEval/95 | HumanEval+ | easy |
| HumanEval/96 | HumanEval+ | easy |
| HumanEval/97 | HumanEval+ | easy |
| HumanEval/98 | HumanEval+ | easy |
| HumanEval/99 | HumanEval+ | easy |
| lcb/3026 | LiveCodeBench | medium |
| lcb/3328 | LiveCodeBench | medium |
| lcb/3334 | LiveCodeBench | easy |
| lcb/3337 | LiveCodeBench | medium |
| lcb/3346 | LiveCodeBench | medium |
| lcb/3349 | LiveCodeBench | easy |
| lcb/3353 | LiveCodeBench | easy |
| lcb/3354 | LiveCodeBench | medium |
| lcb/3355 | LiveCodeBench | medium |
| lcb/3356 | LiveCodeBench | medium |
| lcb/3360 | LiveCodeBench | medium |
| lcb/3361 | LiveCodeBench | easy |
| lcb/3367 | LiveCodeBench | easy |
| lcb/3371 | LiveCodeBench | easy |
| lcb/3372 | LiveCodeBench | easy |
| lcb/3374 | LiveCodeBench | medium |
| lcb/3379 | LiveCodeBench | easy |
| lcb/3381 | LiveCodeBench | easy |
| lcb/3384 | LiveCodeBench | medium |
| lcb/3394 | LiveCodeBench | medium |
| lcb/3395 | LiveCodeBench | medium |
| lcb/3396 | LiveCodeBench | easy |
| lcb/3397 | LiveCodeBench | easy |
| lcb/3398 | LiveCodeBench | easy |
| lcb/3403 | LiveCodeBench | medium |
| lcb/3406 | LiveCodeBench | medium |
| lcb/3408 | LiveCodeBench | easy |
| lcb/3412 | LiveCodeBench | easy |
| lcb/3421 | LiveCodeBench | easy |
| lcb/3422 | LiveCodeBench | medium |
| lcb/3426 | LiveCodeBench | easy |
| lcb/3428 | LiveCodeBench | easy |
| lcb/3429 | LiveCodeBench | easy |
| lcb/3442 | LiveCodeBench | medium |
| lcb/3446 | LiveCodeBench | easy |
| lcb/3447 | LiveCodeBench | easy |
| lcb/3450 | LiveCodeBench | easy |
| lcb/3451 | LiveCodeBench | medium |
| lcb/3453 | LiveCodeBench | medium |
| lcb/3455 | LiveCodeBench | medium |
| lcb/3456 | LiveCodeBench | medium |
| lcb/3462 | LiveCodeBench | medium |
| lcb/3463 | LiveCodeBench | easy |
| lcb/3464 | LiveCodeBench | medium |
| lcb/3468 | LiveCodeBench | easy |
| lcb/3469 | LiveCodeBench | easy |
| lcb/3471 | LiveCodeBench | easy |
| lcb/3475 | LiveCodeBench | medium |
| lcb/3476 | LiveCodeBench | easy |
| lcb/3479 | LiveCodeBench | medium |
| lcb/3484 | LiveCodeBench | easy |
| lcb/3487 | LiveCodeBench | medium |
| lcb/3493 | LiveCodeBench | medium |
| lcb/3494 | LiveCodeBench | medium |
| lcb/3496 | LiveCodeBench | medium |
| lcb/3498 | LiveCodeBench | medium |
| lcb/3502 | LiveCodeBench | medium |
| lcb/3507 | LiveCodeBench | medium |
| lcb/3508 | LiveCodeBench | easy |
| lcb/3511 | LiveCodeBench | easy |
| lcb/3515 | LiveCodeBench | easy |
| lcb/3517 | LiveCodeBench | medium |
| lcb/3518 | LiveCodeBench | medium |
| lcb/3519 | LiveCodeBench | easy |
| lcb/3522 | LiveCodeBench | medium |
| lcb/3526 | LiveCodeBench | medium |
| lcb/3528 | LiveCodeBench | medium |
| lcb/3533 | LiveCodeBench | easy |
| lcb/3534 | LiveCodeBench | medium |
| lcb/3540 | LiveCodeBench | medium |
| lcb/3543 | LiveCodeBench | easy |
| lcb/3553 | LiveCodeBench | easy |
| lcb/3555 | LiveCodeBench | easy |
| lcb/3558 | LiveCodeBench | medium |
| lcb/3559 | LiveCodeBench | medium |
| lcb/3567 | LiveCodeBench | easy |
| lcb/3568 | LiveCodeBench | easy |
| lcb/3570 | LiveCodeBench | medium |
| lcb/3573 | LiveCodeBench | medium |
| lcb/3579 | LiveCodeBench | medium |
| lcb/3587 | LiveCodeBench | medium |
| lcb/3591 | LiveCodeBench | medium |
| lcb/3593 | LiveCodeBench | medium |
| lcb/3600 | LiveCodeBench | easy |
| lcb/3605 | LiveCodeBench | easy |
| lcb/3606 | LiveCodeBench | easy |
| lcb/3607 | LiveCodeBench | medium |
| lcb/3610 | LiveCodeBench | easy |
| lcb/3612 | LiveCodeBench | easy |
| lcb/3613 | LiveCodeBench | medium |
| lcb/3616 | LiveCodeBench | easy |
| lcb/3617 | LiveCodeBench | easy |
| lcb/3620 | LiveCodeBench | medium |
| lcb/3621 | LiveCodeBench | easy |
| lcb/3622 | LiveCodeBench | medium |
| lcb/3625 | LiveCodeBench | easy |
| lcb/3626 | LiveCodeBench | easy |
| lcb/3627 | LiveCodeBench | medium |
| lcb/3629 | LiveCodeBench | medium |
| lcb/3632 | LiveCodeBench | easy |
| lcb/3634 | LiveCodeBench | medium |
| lcb/3636 | LiveCodeBench | easy |
| lcb/3639 | LiveCodeBench | medium |
| lcb/3644 | LiveCodeBench | easy |
| lcb/3649 | LiveCodeBench | medium |
| lcb/3651 | LiveCodeBench | easy |
| lcb/3653 | LiveCodeBench | medium |
| lcb/3654 | LiveCodeBench | medium |
| lcb/3655 | LiveCodeBench | medium |
| lcb/3656 | LiveCodeBench | easy |
| lcb/3657 | LiveCodeBench | medium |
| lcb/3659 | LiveCodeBench | medium |
| lcb/3676 | LiveCodeBench | easy |
| lcb/3681 | LiveCodeBench | medium |
| lcb/3683 | LiveCodeBench | medium |
| lcb/3684 | LiveCodeBench | easy |
| lcb/3685 | LiveCodeBench | easy |
| lcb/3686 | LiveCodeBench | medium |
| lcb/3699 | LiveCodeBench | medium |
| lcb/3702 | LiveCodeBench | easy |
| lcb/3705 | LiveCodeBench | easy |
| lcb/3709 | LiveCodeBench | easy |
| lcb/3715 | LiveCodeBench | medium |
| lcb/3716 | LiveCodeBench | medium |
| lcb/3722 | LiveCodeBench | medium |
| lcb/3723 | LiveCodeBench | easy |
| lcb/3736 | LiveCodeBench | easy |
| lcb/3743 | LiveCodeBench | medium |
| lcb/3748 | LiveCodeBench | medium |
| lcb/3750 | LiveCodeBench | medium |
| lcb/3753 | LiveCodeBench | easy |
| lcb/3754 | LiveCodeBench | medium |
| lcb/3759 | LiveCodeBench | medium |
| lcb/3760 | LiveCodeBench | medium |
| lcb/3763 | LiveCodeBench | medium |
| lcb/3764 | LiveCodeBench | medium |
| lcb/3768 | LiveCodeBench | easy |
| lcb/3771 | LiveCodeBench | medium |
| lcb/3773 | LiveCodeBench | easy |
| lcb/3776 | LiveCodeBench | medium |
| lcb/3778 | LiveCodeBench | easy |
| lcb/3779 | LiveCodeBench | medium |
| lcb/3785 | LiveCodeBench | medium |
| lcb/3786 | LiveCodeBench | medium |
| lcb/3788 | LiveCodeBench | easy |
| lcb/3791 | LiveCodeBench | medium |
| lcb/3793 | LiveCodeBench | medium |
| lcb/3794 | LiveCodeBench | medium |
| lcb/3795 | LiveCodeBench | medium |
| lcb/3799 | LiveCodeBench | easy |
| lcb/3805 | LiveCodeBench | medium |
| lcb/3809 | LiveCodeBench | medium |
| lcb/3811 | LiveCodeBench | easy |
| lcb/3817 | LiveCodeBench | easy |
| lcb/3832 | LiveCodeBench | easy |
| lcb/abc344_a | LiveCodeBench | easy |
| lcb/abc344_b | LiveCodeBench | easy |
| lcb/abc345_b | LiveCodeBench | easy |
| lcb/abc346_a | LiveCodeBench | easy |
| lcb/abc346_b | LiveCodeBench | easy |
| lcb/abc347_a | LiveCodeBench | easy |
| lcb/abc347_b | LiveCodeBench | easy |
| lcb/abc348_a | LiveCodeBench | easy |
| lcb/abc348_b | LiveCodeBench | easy |
| lcb/abc349_a | LiveCodeBench | easy |
| lcb/abc349_b | LiveCodeBench | easy |
| lcb/abc349_c | LiveCodeBench | medium |
| lcb/abc350_a | LiveCodeBench | easy |
| lcb/abc350_b | LiveCodeBench | easy |
| lcb/abc351_a | LiveCodeBench | easy |
| lcb/abc351_b | LiveCodeBench | easy |
| lcb/abc352_a | LiveCodeBench | easy |
| lcb/abc353_a | LiveCodeBench | easy |
| lcb/abc353_b | LiveCodeBench | easy |
| lcb/abc354_a | LiveCodeBench | easy |
| lcb/abc354_b | LiveCodeBench | easy |
| lcb/abc355_a | LiveCodeBench | easy |
| lcb/abc355_b | LiveCodeBench | easy |
| lcb/abc356_a | LiveCodeBench | easy |
| lcb/abc356_b | LiveCodeBench | easy |
| lcb/abc356_c | LiveCodeBench | medium |
| lcb/abc356_d | LiveCodeBench | medium |
| lcb/abc357_a | LiveCodeBench | easy |
| lcb/abc357_b | LiveCodeBench | easy |
| lcb/abc357_c | LiveCodeBench | medium |
| lcb/abc357_d | LiveCodeBench | medium |
| lcb/abc358_a | LiveCodeBench | easy |
| lcb/abc358_b | LiveCodeBench | easy |
| lcb/abc358_c | LiveCodeBench | medium |
| lcb/abc359_a | LiveCodeBench | easy |
| lcb/abc359_b | LiveCodeBench | easy |
| lcb/abc359_c | LiveCodeBench | medium |
| lcb/abc360_a | LiveCodeBench | easy |
| lcb/abc360_b | LiveCodeBench | easy |
| lcb/abc361_a | LiveCodeBench | easy |
| lcb/abc361_b | LiveCodeBench | medium |
| lcb/abc362_a | LiveCodeBench | easy |
| lcb/abc362_b | LiveCodeBench | easy |
| lcb/abc363_a | LiveCodeBench | easy |
| lcb/abc363_b | LiveCodeBench | easy |
| lcb/abc363_c | LiveCodeBench | medium |
| lcb/abc363_d | LiveCodeBench | medium |
| lcb/abc364_a | LiveCodeBench | easy |
| lcb/abc364_b | LiveCodeBench | easy |
| lcb/abc365_a | LiveCodeBench | easy |
| lcb/abc365_b | LiveCodeBench | easy |
| lcb/abc366_a | LiveCodeBench | easy |
| lcb/abc366_b | LiveCodeBench | easy |
| lcb/abc367_a | LiveCodeBench | easy |
| lcb/abc367_b | LiveCodeBench | easy |
| lcb/abc368_a | LiveCodeBench | easy |
| lcb/abc368_b | LiveCodeBench | easy |
| lcb/abc369_a | LiveCodeBench | easy |
| lcb/abc369_b | LiveCodeBench | easy |
| lcb/abc370_a | LiveCodeBench | easy |
| lcb/abc370_b | LiveCodeBench | easy |
| lcb/abc370_c | LiveCodeBench | medium |
| lcb/abc371_a | LiveCodeBench | easy |
| lcb/abc371_b | LiveCodeBench | easy |
| lcb/abc371_c | LiveCodeBench | medium |
| lcb/abc372_a | LiveCodeBench | easy |
| lcb/abc373_a | LiveCodeBench | easy |
| lcb/abc373_b | LiveCodeBench | easy |
| lcb/abc374_a | LiveCodeBench | easy |
| lcb/abc374_b | LiveCodeBench | easy |
| lcb/abc374_c | LiveCodeBench | medium |
| lcb/abc374_d | LiveCodeBench | medium |
| lcb/abc375_a | LiveCodeBench | easy |
| lcb/abc375_d | LiveCodeBench | medium |
| lcb/abc376_a | LiveCodeBench | easy |
| lcb/abc376_b | LiveCodeBench | medium |
| lcb/abc377_a | LiveCodeBench | easy |
| lcb/abc377_b | LiveCodeBench | easy |
| lcb/abc378_a | LiveCodeBench | easy |
| lcb/abc378_b | LiveCodeBench | easy |
| lcb/abc379_a | LiveCodeBench | easy |
| lcb/abc379_b | LiveCodeBench | easy |
| lcb/abc379_d | LiveCodeBench | medium |
| lcb/abc380_a | LiveCodeBench | easy |
| lcb/abc380_b | LiveCodeBench | easy |
| lcb/abc380_c | LiveCodeBench | medium |
| lcb/abc380_d | LiveCodeBench | medium |
| lcb/abc381_a | LiveCodeBench | easy |
| lcb/abc381_b | LiveCodeBench | easy |
| lcb/abc381_c | LiveCodeBench | medium |
| lcb/abc382_a | LiveCodeBench | easy |
| lcb/abc382_b | LiveCodeBench | easy |
| lcb/abc382_c | LiveCodeBench | medium |
| lcb/abc383_a | LiveCodeBench | easy |
| lcb/abc383_b | LiveCodeBench | medium |
| lcb/abc383_c | LiveCodeBench | medium |
| lcb/abc383_d | LiveCodeBench | medium |
| lcb/abc384_a | LiveCodeBench | easy |
| lcb/abc384_b | LiveCodeBench | easy |
| lcb/abc384_c | LiveCodeBench | medium |
| lcb/abc384_d | LiveCodeBench | medium |
| lcb/abc385_a | LiveCodeBench | easy |
| lcb/abc385_b | LiveCodeBench | easy |
| lcb/abc385_c | LiveCodeBench | medium |
| lcb/abc386_a | LiveCodeBench | easy |
| lcb/abc386_b | LiveCodeBench | easy |
| lcb/abc386_c | LiveCodeBench | medium |
| lcb/abc391_a | LiveCodeBench | easy |
| lcb/abc391_b | LiveCodeBench | easy |
| lcb/abc391_d | LiveCodeBench | medium |
| lcb/abc392_a | LiveCodeBench | easy |
| lcb/abc392_b | LiveCodeBench | easy |
| lcb/abc392_c | LiveCodeBench | medium |
| lcb/abc392_d | LiveCodeBench | medium |
| lcb/abc393_a | LiveCodeBench | easy |
| lcb/abc393_b | LiveCodeBench | easy |
| lcb/abc394_a | LiveCodeBench | easy |
| lcb/abc394_b | LiveCodeBench | easy |
| lcb/abc394_c | LiveCodeBench | medium |
| lcb/abc394_d | LiveCodeBench | medium |
| lcb/abc395_a | LiveCodeBench | easy |
| lcb/abc395_b | LiveCodeBench | easy |
| lcb/abc395_c | LiveCodeBench | medium |
| lcb/abc396_a | LiveCodeBench | easy |
| lcb/abc396_b | LiveCodeBench | easy |
| lcb/abc396_c | LiveCodeBench | medium |
| lcb/abc396_d | LiveCodeBench | medium |
| lcb/abc397_a | LiveCodeBench | easy |
| lcb/abc397_b | LiveCodeBench | medium |
| lcb/abc397_c | LiveCodeBench | medium |
| lcb/abc398_a | LiveCodeBench | easy |
| lcb/abc398_b | LiveCodeBench | medium |
| lcb/abc398_c | LiveCodeBench | medium |
| lcb/abc399_a | LiveCodeBench | easy |
| lcb/abc399_b | LiveCodeBench | easy |
| lcb/abc399_c | LiveCodeBench | medium |
| lcb/abc399_d | LiveCodeBench | medium |
| lcb/abc400_a | LiveCodeBench | easy |
| lcb/abc400_b | LiveCodeBench | easy |
| lcb/abc400_c | LiveCodeBench | medium |
| lcb/abc400_d | LiveCodeBench | medium |
| lcb/arc189_a | LiveCodeBench | medium |
| lcb/arc192_a | LiveCodeBench | medium |
| lcb/arc194_a | LiveCodeBench | medium |
| lcb/arc195_a | LiveCodeBench | medium |

## Every available problem-level score and source

- [Per-problem scores and token means](../results/combined/per-problem.csv).
- [Every graded source file and original pass count](../results/combined/sources.csv).
- [Combined scores, intervals and training-ID audit](../results/combined/results.json).
- [All benchmark and difficulty tables](../results/CURRENT-RESULTS.md).
- [Checked new run configurations and first-attempt comparisons](../results/lora-controls/checked-results.json).
- [Saved raw answers and run notes](../results/lora-controls/README.md).
- [Original LoRA-2 training-problem table](../results/full-results/tables/training-problems.csv).

The last table describes the original 280-problem training pool, not extra test problems.
Training/test exact-ID overlap is zero. This does not prove no text or pretraining exposure.
LoRA-2 and historical loop findings were not extended to 464 problems.
No missing result is counted as a failure. Partial-method denominators remain visible.

## Reproduce all current Markdown, without GPU work

```sh
.venv/bin/python scripts/audit_lora_controls.py
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
python3 scripts/sync_thesis_markdown.py
python3 scripts/sync_thesis_markdown.py --check
```

Do not rerun completed notebooks merely to rebuild the text.
Notebook 23 is superseded by Notebook 24. No completed configuration needs repeating.

## Historical versions and export status

[Original Markdown snapshot](../archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz)
contains every pre-update Markdown document, including the original formal thesis.
Raw CSV/JSONL and downloaded reports retain their original contents.
Existing PDF and HTML exports are historical; this update refreshes Markdown only.
