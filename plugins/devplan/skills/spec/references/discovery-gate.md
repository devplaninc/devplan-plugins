# Discovery gate

Use this as a conversational readiness check, not a questionnaire. The goal is to understand the problem and intended value well enough to write a spec - not to collect every possible requirement.

## Establish readiness

Answer these areas from available evidence before asking the user:

1. **Problem** - What is broken, missing, costly, or newly possible? What happens if nothing changes?
2. **Users** - Who experiences it, how often, where in their workflow, and how do they handle it today?
3. **Why now** - Which customer, market, operational, technical, or strategic signals make this timely?
4. **Hypothesis and outcome** - What should change for the user or business, and why might this work cause it?
5. **Success and failure** - What observable result should move? What early signal would show the hypothesis is wrong?
6. **Uncertainty** - Which assumption must be true? Which uncertain journey point or qualitative feedback could change direction?
7. **Boundaries** - What is already decided, constrained, explored, or out of scope? What is the smallest valuable version?

## How to run the conversation

- Open with a short, evidence-informed reflection rather than a blank “tell me more.”
- Ask one focused question at a time.
- Prefer questions about the problem, user motivation, value, and uncertainty before feature requirements.
- Use brief multiple-choice options when they expose a meaningful tradeoff or make an abstract question easier to answer.
- Explain in one sentence why a question matters when that is not obvious.
- Do not be reflexively agreeable. Point out when existing evidence weakens the premise, suggests a different user problem, or conflicts with the proposed solution.
- Keep the conversation bounded. Usually ask two to five questions and stop as soon as another answer would add detail without changing the spec.
- Allow the user to redirect, skip discovery, or request a provisional spec at any point.

Useful question patterns include:

- “The strongest evidence points to **X**, but the request assumes **Y**. Which problem should this spec optimize for?”
- “Which outcome matters most: **A**, **B**, or **C**?”
- “What would we observe in the first two weeks if this hypothesis were wrong?”
- “What is the smallest version that changes the user’s experience rather than only adding functionality?”

## Use evidence before questions

Use this order:

1. Current product and customer context: Devplan in graph mode, connected tools in connector mode.
2. The local artifact or codebase.
3. The user's answer, only for consequential gaps.

Never turn weak or absent evidence into invented customer demand. Preserve disagreement between sources until it can be resolved. Keep tool names, internal terminology, and retrieval mechanics out of the conversation.

## Decide whether to proceed

Proceed when the problem, users, intended outcome, boundaries, success signal, and largest unknowns are clear enough for the requested depth.

If readiness is incomplete:

- ask the single question most likely to change the spec;
- create a provisional spec when assumptions can be explicit and safely reversed;
- pause when different answers imply different problems, commitments, or strategic directions.

When the user explicitly requests a spec, prefer the provisional-spec path whenever the evidence supports a useful objective, scope, success criteria, and risk statement. Treat a sequencing choice or unresolved dependency as an open decision inside the spec unless choosing incorrectly would create a materially different commitment.

Before presenting the spec, briefly synthesize the agreed problem, user, outcome, and important constraint so the transition from discovery to the spec feels continuous.
