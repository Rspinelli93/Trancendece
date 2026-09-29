# Option 3 — C Learning Platform

We build a place to practise C, one topic at a time. Students create an account, solve exercises, get a clear result, and build their topic levels. Recommendations help them choose what to practise next. This recommendations are based on previous results.

We prepare exercises ourselves and generate others with an LLM. Every exercise goes through our compiler and tests before a student receives it. Students never need to talk to the AI. Succesfuly tested exercises will be stored in the Data base and RAG.

Votation system after succesfully finishing an excersise or after failure will let us add a qualification system over our excersises. Excersise with bad qualifications will appear less. After certain percentage of bad qualification, those excersises will get "disqualified". This way we let our users to be the last part of the testing.

## Roles Documents

Read [Understanding the platform](Diagrams/Understanding_the_platform.md) for the whole idea, the tools, and how the parts connect.

Then read the part you are working on, or all of them if you feel exited :)
(The first name is the main person in charge, the other/s collaborate/review)

| System | Main person |
| --- | --- |
| [Accounts and progress](Diagrams/Accounts_and_progress.md) | William + Eliott |
| [Exercises and admin](Diagrams/Admin_and_exercises.md) | Julien + William, with Eliott on the page |
| [LLM and RAG](Diagrams/LLM_and_RAG.md) | Rick + Julien |
| [Compiler integration, correction system and exercises](Diagrams/Compiler_and_correction.md) | Julien + Garance |
| [Recommendations and rewards](Diagrams/Recommendations_and_rewards.md) | Eliott + William, with Rick on ML |
| [DevOps and containers](Diagrams/DevOps_and_containers.md) | Garance + Julien |

## Architecture Documents

- [Exercise lifecycle](Diagrams/Exercise_lifecycle.md): uploads, generated exercises, versions, votes, and removal.
- [Exercise format](Diagrams/Exercise_format.md): what goes inside the JSON and error downloads.
- [Routes](Diagrams/Routes_explained.md): page addresses and backend actions.
- [Database](Diagrams/Database_explained.md): what we save and how records connect.
- [Team tasks](Diagrams/Team_tasks.md): ownership, pairs, and build order.
- [Subject and points](Diagrams/Subject_and_points.md): mandatory work and our proposed 15 points.
- [Team decisions](Diagrams/Team_decisions.md): choices we still need to make.
- [Diagrams](Diagrams/How_to_open_the_diagrams.md): one picture per system, plus the main flows.

This is a proposal that will get us the points idealy, justifiying custom modules with the AI + RAG + Machine learning.

Every time you see a number on the side is the number of the page in the subject that talks about that.

Link to subject: [subject v21.2](../en.subject.pdf)