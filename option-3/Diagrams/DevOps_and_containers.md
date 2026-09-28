# DevOps and containers

**Garance leads. Julien pairs on Judge0. William helps with data and recovery.**

Our aim is a clean checkout that starts with one documented command. A container is a packaged service with the tools it needs.

## What runs

| Part | Purpose |
| --- | --- |
| Nginx | Serve React's built pages and forward HTTPS requests |
| Express API | Handle accounts and ordinary application requests |
| Background worker | Run generation, correction, indexing, and ML jobs |
| PostgreSQL with pgvector | Store application data and RAG search records |
| Judge0 service group | Compile and execute C separately from our application |

The API and worker share one codebase. Python recommendation scripts run with the worker initially. The LLM and embedding model are accessed through the chosen provider, unless we later choose local hosting.

Judge0 brings its own services and storage requirements; it is not just one compiler library. Include its API, workers, queue/storage dependencies, and required host settings in the Compose setup. Do not promise that this architecture has only three containers. Pin a supported, patched release and test its requirements on our actual machine.

## Job handling

Long actions return an ID immediately. React polls a status route and shows progress. Polling stops on success, failure, or expiry.

Keep accepted submissions and generation jobs in PostgreSQL. Workers claim a job so two workers do not award the same result. On restart, retry unfinished jobs safely or mark them retryable.

Admin imports are different: candidate JSON and validation results remain in a bounded temporary folder until confirmation. Keep batch ownership and progress there too. Clean up discarded and expired batches. If that temporary data is lost, ask the admin to upload again; do not claim it was imported.

## Safe execution

The browser cannot reach Judge0 directly. Only the correction worker can submit jobs. Run generated and student code with no application credentials or network access, and set time, memory, process, file, and output limits.

The compiler needs to work on the chosen host before the team builds around it. Check a valid C function, a loop that never ends, large output, a crash, and any planned sanitizer setup. Restrict any runner privileges to the runner environment.

## Startup and recovery

Provide `.env.example`, ignore real secrets, apply database migrations, seed our fixed topics and admin accounts, and document the single startup command. Admin access is assigned during setup, with no user-management panel.

Add `/health` and a simple `/status` page. Show a small public summary rather than database addresses, keys, or raw logs. If generation is unavailable, existing exercises should still be usable. If correction is unavailable, explain that submissions are waiting or can be retried.

Back up application data, eligible exercise material, and the information needed to rebuild the RAG index. Keep a protected copy outside the database volume. Automate backups and practise restoring them into a clean environment. Logs should contain job IDs and useful errors, not passwords, private solutions, or student code dumps.

Containers, HTTPS, secrets, and clean setup support mandatory requirements (subject pp.8–9). Health checks, a status page, automatic backups, and recovery procedures together support the proposed 1-point DevOps module (p.19).

[System diagram](06-devops-and-containers.mmd)
