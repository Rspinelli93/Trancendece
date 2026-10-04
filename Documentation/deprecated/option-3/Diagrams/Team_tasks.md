# Our work

We divide ownership by system and pair where the parts meet. These are starting responsibilities; we can move tasks as the work develops.

| Person | Main responsibility | Shared work |
| --- | --- | --- |
| Rick | LLM generation, RAG retrieval, exercise reuse | Julien on compiler validation; Eliott on ML and training data |
| William | Accounts, sessions, OAuth, database, API routes | Julien on public/admin exercise API; Eliott on progress |
| Eliott | Student pages, shared design, recommendations | Rick on model training; William on saved activity |
| Garance | Containers, HTTPS, Judge0 setup, jobs, health and backups | Julien on safe execution; William on restore checks |
| Julien | Compiler integration, code checking, and exercises | Rick on generated compiler code; William on imports; Eliott on results |

Eliott does not have to build every screen alone. William can take account forms, Julien the JSON upload/results page, and Garance the status page, using Eliott's shared components. Rick also builds the generation-job handling and status integration. Everyone contributes application code as well as their specialist work.

## First useful results

1. William + Eliott: register, log in, and open a dashboard.
2. Garance + Julien: insert a solution into `compiler_code`, run it through Judge0, and compare its output.
3. Julien + William: upload a batch, show checks, and confirm only passed files.
4. Eliott + Julien: open an assigned exercise, submit code, and see the result.
5. William + Eliott: save first completion and topic progress once.
6. Rick + Julien: retrieve examples, generate a valid trial, and add it to RAG after a student passes.
7. Eliott + Rick: start with rule-based suggestions, then train and evaluate personalized recommendations.
8. Garance + William: show health status and restore an automatic backup.

After the core path works, finish voting/reports, badges, public API documentation, search, and evaluation demonstrations. Build the shared design pieces as pages are added.

## Check together

Test simultaneous students, duplicate clicks, runner downtime, invalid batches, stale edits, hidden-answer exposure, disabled exercises, and a clean setup. Each system should be tried by someone who did not write it.

We still need to assign Product Owner, Project Manager, and Technical Lead roles within the five of us. These describe coordination responsibilities, not separate extra people. Record real contributions and module owners in the final root README.

Subject: team roles pp.4–6, shared contributions p.8, and README pp.27–29.
