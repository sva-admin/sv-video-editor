# Learning and handoff

## Keep learning close to evidence

Use the project's existing handoff and issue log. Record:

- The requested outcome and the observed failure, with source or output range.
- The suspected cause, clearly separated from a confirmed cause.
- The smallest correction, inputs changed and sections preserved.
- The exact command, versions, new output hash and confirming check.
- Any remaining visual, listening or owner review.

Before turning a production observation into a reusable rule, classify it as supported, conditional, unverified or contradicted. Decide to adopt, adapt, keep as a hypothesis or reject it. State the conditions and a recheck trigger, such as a tool upgrade or change of output format. One incident is not proof of a universal software bug.

Keep different kinds of information separate:

| Record | Destination |
| --- | --- |
| Client facts, current edit, unresolved decisions | Private project files |
| User preferences | The authorized preference system, only when permitted |
| Tool behavior and repeatable correction | Project evidence, then a de-identified reference if authorized |
| General workflow method | Shared skill after review and suitable authorization |
| Reviewer's opinion | A dated finding attached to the particular output |

This loop improves written instructions and tests. It does not train a model, guarantee aesthetic quality or justify modifying persistent memory without permission.

## Turn a failure into an evaluation

Write a fictional case that exercises the underlying behavior without retaining the real client's names, lines, counts, timeline or identifying combination. Include the user request, available evidence and expected decisions. See [evaluation cases](../evals/cases.json).

Test whether a new agent using only the skill can select the right workflow, preserve authorization, distinguish facts from assumptions and report unfinished checks. For helper code, add a minimal fixture that reproduces the fault and checks its correction. Do not create tests that merely echo implementation details.

## Handoff that another editor can use

Keep the current summary at the top and retain meaningful history below it:

```text
Project and requested deliverables:
Current revision and exact output paths:
Completed work and evidence:
Approved decisions and the revision they apply to:
Source locations and missing material:
Source-to-edit map, cue file and editable project:
Build command, tool versions and dependencies:
Preview restart command and known limitations:
Active jobs, owner, lock and cache state:
Next action, responsible person and dependency:
Technical checks not run:
Visual or listening review still needed:
Owner approvals still needed:
Sent or published status:
```

Use one maintained home for each output. Verify that the receiving editor can resolve sources and open the project before describing a handover as complete. A portable zip must contain the necessary records and permitted assets or clear source-relink instructions. Avoid duplicating large media when the recipient already has verified copies.
