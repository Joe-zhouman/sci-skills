# Paper Types

When paper type matters for architecture and argument structure, load the relevant section.

## Research paper

The reader asks: why the phenomenon matters → what was done → what was found → what it means.

**Hourglass structure**: Introduction opens broadly then narrows to gap/question/hypothesis. Discussion/Conclusion widens again, connecting findings back to literature.

**Productive writing order**: Results → Introduction + Conclusion → Title → Discussion → Methods → Abstract.

## Methods paper

The reader asks: what capability does this enable → how does it work → how was it validated → what are its limits.

**Key difference from research**: the method is the contribution, not the means. The validation must demonstrate the method works, not just that it produced interesting data.

**Architecture**:
- Open with the capability gap: what can't researchers do now?
- Present the method as the solution to that gap
- Validate on known benchmarks or problems with ground truth
- Compare fairly to existing methods (same data, same metrics)
- State limitations explicitly: when does the method fail or degrade?

**Common failure**: presenting a methods paper as a research paper — the Introduction reads like a domain review instead of a capability-gap argument.

## Hypothesis paper

The reader asks: what is the proposed explanation → what would confirm or refute it → what evidence exists → what remains to be tested.

**Architecture**:
- State the hypothesis clearly and early
- Distinguish what is known from what is proposed
- Present evidence for and against — not just supporting evidence
- Define what would falsify the hypothesis
- Propose specific tests

**Common failure**: presenting a hypothesis as a conclusion. The language should signal "this is a proposal to be tested" not "this is established."

## Algorithmic paper

The reader asks: what problem does this solve → how does the algorithm work → how does it perform → what are the trade-offs.

**Architecture**:
- Define the computational problem precisely
- Present the algorithm with clear notation
- Analyze complexity (time, space, communication)
- Benchmark against baselines on standard datasets
- Discuss failure cases and edge conditions

**Common failure**: overclaiming generality from narrow benchmarks.

## Review paper

The reader asks: what is the state of the field → what are the major themes and debates → where is it going.

**Architecture**:
- Define the scope and organizing framework upfront
- Synthesize, don't serialize — group papers by theme, not by publication date
- Identify consensus, controversy, and gaps
- Propose future directions that emerge from the synthesis

**Common failure**: a literature dump that lists papers without synthesis. Each paragraph should have a point that multiple papers support or complicate.
