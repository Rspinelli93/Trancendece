# Compiler integration, correction system and exercises

**Julien leads. Garance handles the isolated runner. Rick helps with generated exercises.**

Judge0 runs C code for us. Our job is to prepare the exercise tests, send the right files, interpret results, and protect the student's progress from system errors.

## What is checked

Compiling checks whether code can become a program. Running tests checks whether it behaves as expected. Both must succeed.

The working proposal is function exercises first: the student implements a named function, and our test program calls it. Full programs can come later if we choose them. Function-only scope still needs the team's final agreement.

We use trusted test templates written by us. The JSON selects a template and supplies input/output cases. It cannot provide arbitrary shell commands or choose unrestricted compiler flags.

## Submission flow

1. Confirm the student owns the assignment and its exercise version is usable.
2. Save the submitted code with a request ID.
3. Put it into the chosen test template and submit to Judge0.
4. Run public examples and private tests within limits.
5. Interpret the execution results on our backend.
6. Save the final result and any first-completion reward once.
7. Return a safe result to the page; update recommendations later.

Judge0 has an HTTP API for submission creation and result lookup. Our worker keeps its tokens private and polls for completion. We configure a C runtime, isolated execution, and time/memory limits. [Judge0 API](https://ce.judge0.com/)

## Results students understand

| Result | Meaning |
| --- | --- |
| Passed | All required checks passed |
| Compilation error | The C code could not compile |
| Test failed | A result did not match what the exercise expected |
| Timeout | The program did not finish within the limit |
| Memory limit | The program used too much allowed memory |
| Memory error | A checker detected invalid memory use |
| Memory leak | A checker detected allocated memory that was not released |
| Program crash | Execution stopped unexpectedly |
| Service error | Our correction service failed; this is not a student failure |

Memory leaks are not detected just by compiling. We need a tested sanitizer setup or another memory checker inside the runner. AddressSanitizer can detect memory errors, with leak checking depending on the platform. Sanitizers also need different resource settings. Garance and Julien must verify this before promising `memory_leak` results. [Clang reference](https://clang.llvm.org/docs/AddressSanitizer.html)

Use the same categories for admins and students. Admin downloads include reference-code diagnostics; students see their own useful diagnostics without hidden inputs, expected hidden answers, private test source, or server paths. A failed hidden test can say “An edge case failed”.

## Fair correction

We control the harness and compare outputs outside the submitted program. Printing “passed” cannot award points. The runner has no application secrets or access to our database. Network, file, process, time, and output limits apply.

Keep test expectations outside the student's executable where practical, send cases separately, and never return the test bundle to the browser. Generated code is untrusted too.

Retries with the same request ID return the original submission. Runner failures can retry safely without awarding twice. Confirmed broken exercises do not count toward failed-attempt recommendations; previously earned levels are not removed.

Main routes: `POST /api/v1/assignments/:assignmentId/submissions` and `GET /api/v1/submissions/:submissionId`. See [all routes](Routes_explained.md).

Demonstrate correct code, wrong output, a compile error, an infinite loop, a crash, and a runner outage. Memory-leak demonstration is required before enabling that result category.

[System diagram](04-compiler-and-correction.mmd)
