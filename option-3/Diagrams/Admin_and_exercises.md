# Exercises and the admin page

**Julien and William build the flow. Eliott helps with the page.** Rick helps with RAG eligibility, and Garance helps with long-running jobs.

## The page

Start with a simple list of exercise names and IDs. Search by ID or name, filter by topic, sort the list, and move between result pages. A small status label shows whether an exercise is active, trial, or disabled.

Click an exercise to see its JSON, ratings, and report count. The actions are **Edit** and **Disable**. Disable asks “Are you sure?” and removes the exercise from new assignments and RAG searches. We keep old results for student history.

Topics come from our fixed list. User management, role editing, topic editing, and a separate reports page are outside this first version.

## Upload one or many

Paste JSON, upload one file, or select several `.json` files. A pasted JSON array can also contain a batch.

1. Check the files and required fields.
2. Compile each reference solution and run its tests.
3. Show progress, such as “Checking 7 of 20”.
4. Show a passed list and a failed list, with clear errors.
5. Let us download failed exercises with `validation_errors` added.
6. **Import passed exercises** saves only the passed items we confirm.
7. **Discard failed exercises** removes failed items from the temporary batch.

Before confirmation, files and results live in temporary job storage, not the permanent exercise library. A failed item never becomes an exercise record. Judge0 may hold its own execution records temporarily; those follow a cleanup policy.

The page polls progress. It stops when the batch finishes and offers a retry if the job expires or the service restarts. Repeating the import request must not create duplicates.

## Editing

The JSON editor creates a candidate version. Validate it, view the result, then confirm the change. If validation fails, the previous version stays untouched.

A confirmed edit creates a new version and resets the visible votes and reports. Old submissions and feedback stay attached to the old version. New assignments use the new version. An existing student attempt keeps its original version unless that version is disabled.

An admin-confirmed, validated edit follows the admin publication path and can enter RAG immediately. Its history still records whether the original content came from the LLM.

## Communication and routes

React → Express admin routes → temporary batch → worker → Judge0 → validation results → confirmation → PostgreSQL → RAG index.

Pages: `/admin/exercises`, `/admin/exercises/new`, `/admin/exercises/:exerciseId`.

Routes use `/api/v1/admin/exercises` and `/api/v1/admin/imports`. The [route guide](Routes_explained.md) covers validation, progress, errors, import, editing, and disable actions.

Express checks the admin session on every request. JSON cannot assign its own “passed” status, grant access, or change the compiler's safety settings. Existing IDs go through the edit flow rather than being silently overwritten by an upload.

## What we should demonstrate

Upload a mixed batch, download useful errors, and import only the successful files. Edit an active exercise with broken code and show that its old version remains usable. A normal student must be refused every admin action.

Search needs filters, sorting, and pagination for its 1-point module (subject p.13). JSON upload alone is not the file-management or import/export module.

[System diagram](02-admin-and-exercises.mmd)
