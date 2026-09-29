# Decisions before implementation

We are building a C learning platform with free accounts, no sockets, no student AI assistant, simple code results, and at most five topics. Admins paste or upload JSON, including batches. Every exercise must pass the compiler check before publication.

Admin-confirmed exercises can enter RAG immediately after successful checks. Platform-generated exercises enter only after a student passes. Badges use ordinary rules; ML recommends practice. Voting uses a percentage, and reports can be sent before a student finishes.

## Still to settle

1. **Topics:** choose at most five from the list below.
2. **Exercise shape:** function exercises use `compiler_code` with a `{{SOLUTION}}` placeholder. Confirm whether whole C programs are also needed.
3. **Generation:** the proposed trigger is an assignment with no suitable saved exercise. Choose request limits, retry limit, provider, budget, and embedding model.
4. **Rewards:** define points, badge milestones, topic levels, and leaderboard ties.
5. **Feedback limits:** choose the minimum vote count and negative percentage. Five distinct reports remains a provisional threshold.
6. **Trial policy:** a generated exercise enters RAG automatically after the first passing student solution. Set how many students may receive a trial at once.
7. **Memory checks:** confirm the supported checker setup and resource limits with a real run.
8. **Module claim:** prepare the custom-module argument or choose a replacement before relying on 15 points.
9. **Coordination:** assign PO, PM, and Tech Lead responsibilities.

## Topic candidates

Variables and conditions; loops; functions; arrays; string manipulation; pointers; memory management; structures; linked lists; recursion; file handling; bitwise operations; recreating simple C functions; debugging broken code; reading program output; searching and sorting.

A possible group of five is strings, arrays/pointers, memory management, recreating functions, and structures/linked lists. We have not selected it. Introductory material must also fit the agreed five-topic limit; we should not quietly add extra topics later.

## Working choices for the diagrams

The diagrams use React, Express, Prisma/PostgreSQL with pgvector, a shared background worker, Judge0, and Python recommendation scripts. They show `reference_solution`, `compiler_code`, `expected_output`, and automatic RAG inclusion after a student pass. If we change those choices, update the routes, lifecycle, and matching diagrams together.
