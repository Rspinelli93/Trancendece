# Reading the diagrams

Open a `.mmd` file in an editor that supports Mermaid preview. The source is plain text, so the team can change it alongside the Markdown.

Each system has a short written guide and a diagram. Read the guide first if a tool or arrow is unfamiliar.

| Diagram | What it shows |
| --- | --- |
| [00 — Overview](00-system-overview.mmd) | Pages, backend, worker, data, and outside tools |
| [01 — Accounts and progress](01-accounts-and-progress.mmd) | Login and saved learning activity |
| [02 — Admin and exercises](02-admin-and-exercises.mmd) | Batch upload, checks, confirmation, editing, disabling |
| [03 — LLM and RAG](03-llm-and-rag.mmd) | Find examples, generate, validate, and reuse |
| [04 — Compiler and correction](04-compiler-and-correction.mmd) | Code submission and result handling |
| [05 — Recommendations and rewards](05-recommendations-and-rewards.mmd) | Model suggestions and ordinary reward rules |
| [06 — DevOps](06-devops-and-containers.mmd) | Containers, private execution, status, and backups |
| [07 — Exercise lifecycle](07-exercise-lifecycle.mmd) | Different admin and generated-exercise paths |
| [08 — Student submission](08-student-submission.mmd) | Request, polling, correction, reward, and trial promotion |
| [09 — Database](09-database.mmd) | Records and links between them |
| [10 — Pages](10-pages.mmd) | Where students and admins navigate |
| [11 — Routes](11-backend-routes.mmd) | Request groups and who handles them |

Arrows mean information or work moving between parts. A dotted arrow marks supporting work. Sequence diagrams read top to bottom. Database lines show how records connect; `PK` means a record's own ID and `FK` means an ID pointing to another record.

See [Database explained](Database_explained.md) for constraints that are not readable in a compact picture. See [Routes](Routes_explained.md) for the complete contract; the route diagram is an overview.
