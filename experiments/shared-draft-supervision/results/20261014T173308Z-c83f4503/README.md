# Incomplete first 4B token audit

The original report and per-example audit are preserved byte-for-byte.
Source hashes, 73-example count, exact ID checks, EOS, and label checks passed.
No GPU used. Reported wall time: 27.125 seconds after Drive setup.

The reported 1.5855% redundant thinking share is incomplete.
The parser accepted at most three spaces before a fenced code block.
It therefore skipped deeper-indented draft blocks in the saved thinking text.
Do not use its 12-trace count or failed 5% screen to accept/reject the candidate.
The saved report's next-step instruction to park the candidate is superseded.

Indent-aware parser v2 requires matching opening/closing indentation.
It includes four/eight spaces and tabs, while retaining language filtering and AST checks.
Read-only character-offset checks find 238 nonempty parseable blocks and 27 duplicate traces.
These match the initial broad audit on all 73 traces, excluding empty trees.
Character fixtures do not give a corrected tokenizer percentage.
The corrected Colab CPU token audit remains pending. No GPU training authorized.
