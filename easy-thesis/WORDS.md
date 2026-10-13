# Words used in this folder

Each word is used in the easy thesis.
The longer list is [../GLOSSARY.md](../GLOSSARY.md).

| Word | Meaning |
|---|---|
| Token | A small piece of text, about three quarters of a word. The model writes one token at a time. |
| Thinking | Notes the model writes to itself before the code. Thinking uses tokens and time. |
| Thinking ON | The normal way. The model may think as long as the token room allows. |
| Thinking OFF | The switch is off. The model writes the answer with no thinking notes. |
| Thinking limit | We stop the thinking notes at a fixed length, then the model must answer. |
| Think briefly | We add one sentence that asks for short thinking. |
| LoRA | A small trained add-on. The big model stays frozen. |
| LoRA-1 | The add-on from the small early test (easy problems only). |
| LoRA-2 | The add-on from the main 2B run. This was the main trained way, chosen before we saw scores. |
| Accuracy | Average of each problem’s share of passing attempts. |
| Pass | The code passes every test for that problem. One failed test means fail. |
| Points | The gap between two accuracies. 40% minus 30% is +10 points. |
| Error bar | An uncertainty interval from resampling problems; it does not prove a universal result. |
| Cut off | The saved output reached its cap. The grader still determines whether extracted code passes. |
| Loop | The model repeats the same lines until the room runs out. |
| Dataset | A fixed list of problems, with tests. |
| Overlap | A training problem that is too close to a test problem. We remove those. |
| Median | The middle value after you sort the numbers. A few huge answers do not pull it up. |
| GPU | The chip that runs the model. We used a Google Colab A100. |
| 0.8B / 2B / 4B | About 0.8, 2, or 4 billion numbers inside the model. Bigger usually means stronger and heavier. |
| Coverage | How many unique problems have results for one method. |
| Retrospective | Chosen after the results were available. |
| Equal problem weight | Each problem contributes equally, even when attempt counts differ. |
| Paired comparison | Compare two methods on exactly the same problems. |
| Bootstrap | Repeat the calculation on resampled problems to estimate uncertainty. |
