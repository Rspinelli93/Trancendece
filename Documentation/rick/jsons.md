# JSON formats

# Exercises

## 1. Admin exercise upload

This is the complete exercise uploaded by an admin.

### Format

| Field | Meaning |
| --- | --- |
| `title` | Exercise name |
| `exercise_type` | `function` or `program` |
| `level` | `1`, `2`, or `3` |
| `tags` | Words that help RAG understand the exercise |
| `description` | Instructions shown to the student |
| `starter_code` | Initial code shown in the editor; it can be empty |
| `hints` | Optional text or function names shown in the frontend to help the student |
| `reference_solution` | Correct code used only to validate the exercise |
| `forbidden_functions` | Functions the student cannot use |
| `tests` | Tests that the reference solution and student code must pass |
| `compiler_code` | Test program containing `/* STUDENT_CODE */`; empty for complete-program exercises |
| `input` | Text sent to the program through standard input; it can be empty |
| `expected_output` | Exact output expected from this test |

### Example

**When:** An admin submits a new exercise.

**Sent from → to:** Admin page → main backend service.

```json
{
  "title": "Create ft_strlen",
  "exercise_type": "function",
  "level": 1,
  "tags": ["strings", "loops", "strlen"],
  "description": "Create a function that returns the length of a string.",
  "starter_code": "int ft_strlen(char *str)\n{\n\n}",
  "hints": ["Use a loop", "Stop at the null character"],
  "reference_solution": "int ft_strlen(char *str) { int i = 0; while (str[i]) i++; return i; }",
  "forbidden_functions": ["strlen"],
  "tests": [
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"hola\")); }",
      "input": "",
      "expected_output": "4\n"
    },
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"\")); }",
      "input": "",
      "expected_output": "0\n"
    }
  ]
}
```

### Workflow

- **When:** An admin uploads a new exercise.
- **Communication:** Admin page → main backend service.
- **Use:** The main backend checks the format, creates the exercise ID, and prepares the validation request shown in step 2.
- **Result:** The upload continues to the code-checking service. Nothing is stored yet.
- **Discarded:** `reference_solution` is discarded after validation.
- **Hint:** The backend generates the exercise ID before testing so temporary tester responses and logs can identify the upload. A failed upload is not stored and its ID is never reused. The `hints` field is only learning help shown in the frontend. It is not used by RAG or the tester.

## 2. Exercise validation request

The main backend creates this request to test the admin's reference solution.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | ID of the exercise being tested |
| `exercise_title` | Exercise name included for readable logs |
| `exercise_type` | `function` or `program` |
| `code` | The reference solution |
| `forbidden_functions` | Functions that cannot be used |
| `tests` | Compiler code, input, and expected output for every test |

### Example

**When:** The admin exercise format is valid and an exercise ID has been created.

**Sent from → to:** Main backend service → code-checking service.

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "exercise_type": "function",
  "code": "int ft_strlen(char *str) { /* code */ }",
  "forbidden_functions": ["strlen"],
  "tests": [
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"hola\")); }",
      "input": "",
      "expected_output": "4\n"
    }
  ]
}
```

### Workflow

- **When:** Validating an admin upload.
- **Communication:** Main backend service → code-checking service.
- **Use:** The code-checking service checks forbidden functions, compiles the reference solution, runs every test, and compares the outputs.
- **Stored:** No. This request is temporary.
- **Hint:** The reference solution is placed in `code` only for this validation request.

## 3. Exercise validation result

This tells the main backend whether the reference solution passed every test.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | ID of the tested exercise |
| `exercise_title` | Name of the tested exercise |
| `success` | `true` only when every check passes |
| `error` | Simple compiler or test error; empty after success |

### Example

**When:** The code-checking service finishes every test.

**Sent from → to:** Code-checking service → main backend service.

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "success": false,
  "error": "Test 2 returned the wrong output."
}
```

### Workflow

- **When:** After the code-checking service finishes validating the reference solution.
- **Communication:** Code-checking service → main backend service.
- **Use:** A failure rejects the upload. A success continues to step 4.
- **Stored:** No. The complete response is temporary.
- **Hint:** The ID and title make temporary logs easier to understand. Private expected outputs must not be included in the error shown to the student.

## 4. Validated exercise sent to the AI/RAG service

The reference solution has passed. The main backend now sends the exercise data needed for vector creation and storage.

### Format

The format contains the generated ID and all exercise fields except the discarded reference solution.

### Example

**When:** The exercise validation result has `success: true`.

**Sent from → to:** Main backend service → AI/RAG service.

```json
{
  "id": "exercise-123",
  "title": "Create ft_strlen",
  "exercise_type": "function",
  "level": 1,
  "tags": ["strings", "loops", "strlen"],
  "description": "Create a function that returns the length of a string.",
  "starter_code": "int ft_strlen(char *str)\n{\n\n}",
  "hints": ["Use a loop", "Stop at the null character"],
  "forbidden_functions": ["strlen"],
  "tests": [
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"hola\")); }",
      "input": "",
      "expected_output": "4\n"
    }
  ]
}
```

### Workflow

- **Use:** The AI/RAG service checks the JSON, creates the embedding, adds `status: enabled`, and prepares the database row.
- **Stored:** Not yet. Storage happens in step 5.
- **Discarded:** The reference solution is not sent because its validation work is finished.

## 5. Validated exercise stored in the database

This is created only after the reference solution passes every test and the vector is created.

### Format

| Field | Meaning |
| --- | --- |
| `id` | Automatically generated, unique, and never reused |
| `title` | Exercise name |
| `exercise_type` | `function` or `program` |
| `level` | `1`, `2`, or `3` |
| `tags` | Internal words used by RAG |
| `description` | Student instructions |
| `starter_code` | Initial editor content; it can be empty |
| `hints` | Optional help displayed to the student |
| `forbidden_functions` | Functions that cannot be used |
| `tests` | Private compiler code, input, and expected outputs |
| `status` | `enabled` or `disabled` |
| `embedding` | Vector used by RAG to find the exercise |

### Example

**When:** The reference solution and vector creation have both succeeded.

**Sent from → to:** AI/RAG service → PostgreSQL.

```json
{
  "id": "exercise-123",
  "title": "Create ft_strlen",
  "exercise_type": "function",
  "level": 1,
  "tags": ["strings", "loops", "strlen"],
  "description": "Create a function that returns the length of a string.",
  "starter_code": "int ft_strlen(char *str)\n{\n\n}",
  "hints": ["Use a loop", "Stop at the null character"],
  "forbidden_functions": ["strlen"],
  "tests": [
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"hola\")); }",
      "input": "",
      "expected_output": "4\n"
    }
  ],
  "status": "enabled",
  "embedding": [0.12, -0.08, 0.31]
}
```

### Workflow

- **When:** After upload validation and vector creation succeed.
- **Communication:** AI/RAG service → database.
- **Use:** The AI/RAG service returns public fields, provides private tests to the main backend, and uses the embedding for RAG.
- **Stored:** Yes.
- **Hint:** The frontend receives `hints`. `tests`, forbidden checks, expected outputs, and the embedding are never sent to the student page.

## 6. Exercise storage result

The AI/RAG service tells the main backend whether vector creation and database storage succeeded.

### Format

| Field | Meaning |
| --- | --- |
| `success` | Whether the exercise was stored |
| `exercise_id` | Exercise ID |
| `exercise_title` | Exercise name for readable logs |
| `error` | Safe error message; empty after success |

### Example

**When:** The AI/RAG service finishes vector creation and storage.

**Sent from → to:** AI/RAG service → main backend service.

```json
{
  "success": true,
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "error": null
}
```

### Workflow

- **Use:** The main backend shows the final upload result to the admin.
- **Stored:** No. This response is temporary.
- **Hint:** If vector creation or storage fails, `success` is `false` and the exercise is not stored.

## 7. Student submission

The student sends the exercise ID and their code. The main backend does not trust an exercise title from the frontend.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | Exercise being answered |
| `code` | Student's C code |

### Example

**When:** A student presses Submit.

**Sent from → to:** Student frontend → main backend service.

```json
{
  "exercise_id": "exercise-123",
  "code": "int ft_strlen(char *str) { int i = 0; while (str[i]) i++; return i; }"
}
```

### Workflow

- **When:** The student presses Submit.
- **Communication:** Student page → backend.
- **Use:** The main backend gets `user_id` from the login session and requests the trusted exercise data shown in step 8.
- **Stored:** Not yet. The code stays temporary.
- **Hint:** The exercise title and private tests must come from the AI/RAG service, not from the frontend.

## 8. Request for private exercise data

The main backend asks for the data needed to test the submission.

### Example

**When:** The main backend accepts the student submission format.

**Sent from → to:** Main backend service → AI/RAG service.

```json
{
  "exercise_id": "exercise-123"
}
```

### Workflow

- **Use:** Find the enabled exercise and its private tests.
- **Stored:** No.

## 9. Private exercise data returned

The AI/RAG service returns the trusted testing information.

### Example

**When:** The exercise exists and is enabled.

**Sent from → to:** AI/RAG service → main backend service.

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "exercise_type": "function",
  "forbidden_functions": ["strlen"],
  "tests": [
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"hola\")); }",
      "input": "",
      "expected_output": "4\n"
    }
  ]
}
```

### Workflow

- **Use:** The main backend combines this trusted data with the temporary student code.
- **Stored:** No. This response is temporary.
- **Private:** This JSON never goes to the frontend.

## 10. Student code sent to the code-checking service

The main backend creates the complete checking request.

### Example

**When:** The private exercise data has been returned.

**Sent from → to:** Main backend service → code-checking service.

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "exercise_type": "function",
  "code": "int ft_strlen(char *str) { int i = 0; while (str[i]) i++; return i; }",
  "forbidden_functions": ["strlen"],
  "tests": [
    {
      "compiler_code": "#include <stdio.h>\n/* STUDENT_CODE */\nint main(void) { printf(\"%d\\n\", ft_strlen(\"hola\")); }",
      "input": "",
      "expected_output": "4\n"
    }
  ]
}
```

### Workflow

- **Use:** Check forbidden functions, compile the student code, run every test, and compare the output.
- **Stored:** No. The code and tests are temporary.

## 11. Student submission result

The code-checking service returns the result before anything is saved as an attempt.

### Example

**When:** The code-checking service finishes the submission tests.

**Sent from → to:** Code-checking service → main backend service.

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "success": true,
  "error": null
}
```

### Workflow

- **Use:** Show a safe result to the student and prepare the attempt record.
- **Stored:** Only the attempt fields shown in step 12 are stored.
- **Hint:** Student code, private tests, and the complete compiler response are discarded.

## 12. Exercise attempt stored in the database

One record represents one submitted attempt.

### Format

| Field | Meaning |
| --- | --- |
| `user_id` | Student who submitted |
| `exercise_id` | Exercise that was submitted |
| `success` | Whether every test passed |
| `attempt_number` | First, second, third attempt, and so on |
| `time_taken` | Time spent before submission; the exact measuring method is still undecided |

### Example

**When:** The code-checking service returns the submission result.

**Sent from → to:** Main backend service → PostgreSQL.

```json
{
  "user_id": "user-1",
  "exercise_id": "exercise-123",
  "success": true,
  "attempt_number": 2,
  "time_taken": 185
}
```

### Workflow

- **When:** After the tester returns a result for a student submission.
- **Communication:** Backend → database.
- **Use:** Later scoring, MMR, badges, and learning progress can use these results.
- **Stored:** Yes.
- **Hint:** Student code, compiler errors, and dates are not stored.

## 13. Student exercise report

The student reports a problem with an exercise.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | Exercise being reported |
| `report` | Message with a maximum of 100 characters |

### Example

**When:** A student presses Report exercise.

**Sent from → to:** Student frontend → main backend service. The main backend then stores it in PostgreSQL.

```json
{
  "exercise_id": "exercise-123",
  "report": "The empty-string test appears to be incorrect."
}
```

### Workflow

- **When:** A student presses Report exercise.
- **Communication:** Student page → backend → database.
- **Use:** The admin can read reports and disable the exercise.
- **Stored:** One database row per report with `exercise_id`, `user_id`, and `report`.
- **Hint:** The backend obtains `user_id` from the login session. It does not store the username in the report.

## 14. Reports shown to the admin

The backend groups report rows by user when displaying them.

### Format

| Field | Meaning |
| --- | --- |
| `user_id` | User who reported the exercise |
| `username` | Current username loaded from the users table |
| `reports` | All messages sent by that user for this exercise |

### Example

**When:** An admin opens the reports for one exercise.

**Sent from → to:** Main backend service → admin frontend.

```json
[
  {
    "user_id": "user-1",
    "username": "a",
    "reports": ["First report", "Second report"]
  },
  {
    "user_id": "user-2",
    "username": "b",
    "reports": ["Another report"]
  }
]
```

### Workflow

- **When:** An admin opens the reports for an exercise.
- **Communication:** Database → backend → admin page.
- **Use:** The admin reads the reports and can disable the exercise.
- **Stored:** This grouped JSON is not stored. It is built from individual report rows.
- **Hint:** Loading the username from the users table keeps it correct if the user changes their name.

## 15. Learning request sent to the AI/RAG service

The main backend sends the student's level and request after checking the login and form.

### Format

| Field | Meaning |
| --- | --- |
| `level` | Selected level: `1`, `2`, or `3` |
| `query` | What the student wants to learn |

### Example

**When:** A logged-in student sends a learning request.

**Sent from → to:** Main backend service → AI/RAG service.

```json
{
  "level": 2,
  "query": "I want to practise changing pointers inside functions."
}
```

### Workflow

- **Communication:** Main backend service → AI/RAG service.
- **Use:** Create the request vector, search enabled exercises, and ask the LLM to choose from valid matches.
- **Stored:** No.

## 16. Exercise match or no match

A match returns one existing exercise ID:

**When:** RAG finds valid candidates and the LLM chooses one.

**Sent from → to:** AI/RAG service → main backend service.

```json
{
  "matched": true,
  "exercise_id": "exercise-123",
  "exercise_title": "Change a pointer from a function",
  "reason": "This exercise practises changing a pointer through a function."
}
```

If no result is close enough:

**When:** The search finishes correctly but finds no suitable exercise.

**Sent from → to:** AI/RAG service → main backend service.

```json
{
  "matched": false,
  "exercise_id": null,
  "reason": "No suitable exercise was found for your request."
}
```

### Workflow

- **Communication:** AI/RAG service → main backend service → frontend.
- **Stored:** No.
- **Hint:** A no-match response means the search worked but found nothing suitable.

## 17. AI/RAG service error

A technical failure returns a safe error:

**When:** PostgreSQL, the vector model, or the LLM fails.

**Sent from → to:** AI/RAG service → main backend service.

```json
{
  "success": false,
  "error_code": "SERVICE_UNAVAILABLE",
  "message": "The exercise service is temporarily unavailable.",
  "request_id": "request-123"
}
```

### Workflow

- **When:** PostgreSQL, the vector model, or the LLM fails.
- **Communication:** AI/RAG service → main backend service → frontend.
- **Stored:** The response is not stored. The request ID and technical error go to the logs.
- **Hint:** A technical failure must not be returned as “no exercise found.”

---

# Users

## 1. Local registration

A student creates an account with a username, email, password, and predefined avatar.

### Format

| Field | Meaning |
| --- | --- |
| `username` | Unique name used for login and display |
| `email` | Unique email used for login |
| `password` | Plain password used only during registration |
| `avatar` | ID of one predefined avatar |

### Example

**When:** A student submits the local registration form.

**Sent from → to:** Registration frontend → main backend service.

```json
{
  "username": "rick",
  "email": "rick@example.com",
  "password": "plain-password",
  "avatar": "avatar-3"
}
```

### Workflow

- **When:** A student creates a local account.
- **Communication:** Registration page → backend → database.
- **Use:** The backend checks the fields, hashes the password, and creates the user.
- **Stored:** The username, email, password hash, and avatar ID are stored. The plain password is discarded.
- **Hint:** Username and email comparisons ignore uppercase differences.

## 2. Local login

A local user can log in with either their username or email.

### Format

| Field | Meaning |
| --- | --- |
| `login` | Username or email |
| `password` | Local account password |

### Example

**When:** A local user submits the login form.

**Sent from → to:** Login frontend → main backend service.

```json
{
  "login": "rick",
  "password": "plain-password"
}
```

### Workflow

- **When:** A local user logs in.
- **Communication:** Login page → backend → database.
- **Use:** The backend finds the enabled user and checks the password hash.
- **Stored:** The request is not stored.
- **Hint:** GitHub accounts cannot use this login because they have no local password.

## 3. GitHub OAuth account

GitHub verifies the person and returns their GitHub identity to the backend.

### Format

| Field | Meaning |
| --- | --- |
| `github_id` | Unique account ID returned by GitHub |
| `username` | Unique username for our platform |
| `email` | Unique email returned and verified through GitHub |
| `avatar` | One predefined avatar chosen for our platform |

### Example

**When:** GitHub verifies a first login and the new account is ready to be stored.

**Sent from → to:** Main backend service → PostgreSQL.

```json
{
  "github_id": "github-928374",
  "username": "rick",
  "email": "rick@example.com",
  "avatar": "avatar-3"
}
```

### Workflow

- **When:** A student logs in with GitHub for the first time.
- **Communication:** Browser → GitHub → backend → database.
- **Use:** The backend trusts the identity only after completing the GitHub OAuth flow.
- **Stored:** `github_id`, username, email, and avatar are stored. GitHub access data used during login is not kept unnecessarily.
- **Hint:** A GitHub user has no local password. `password_hash` stays empty.

## 4. User stored in the database

One record represents one local or GitHub account.

### Format

| Field | Meaning |
| --- | --- |
| `id` | Automatically generated, unique, and never reused |
| `username` | Unique username |
| `email` | Unique email |
| `password_hash` | Hashed password for local users; empty for GitHub users |
| `github_id` | Unique GitHub ID for OAuth users; empty for local users |
| `role` | `student` or `admin` |
| `status` | `enabled` or `disabled` |
| `avatar` | Predefined avatar ID for students; empty for the admin |
| `total_score` | Starts at `0` for students; empty for the admin |
| `mmr` | Starts at `0` for students; empty for the admin |
| `badges` | List of earned badge IDs for students; empty for the admin |

### Local-user example

**When:** A local registration or accepted profile update is saved.

**Sent from → to:** Main backend service → PostgreSQL.

```json
{
  "id": "user-1",
  "username": "rick",
  "email": "rick@example.com",
  "password_hash": "hashed-password",
  "github_id": null,
  "role": "student",
  "status": "enabled",
  "avatar": "avatar-3",
  "total_score": 0,
  "mmr": 0,
  "badges": ["first-success"]
}
```

### GitHub-user example

**When:** A first GitHub login is accepted and saved.

**Sent from → to:** Main backend service → PostgreSQL.

```json
{
  "id": "user-2",
  "username": "julien",
  "email": "julien@example.com",
  "password_hash": null,
  "github_id": "github-638493",
  "role": "student",
  "status": "enabled",
  "avatar": "avatar-1",
  "total_score": 0,
  "mmr": 0,
  "badges": []
}
```

### Workflow

- **When:** After local registration, first GitHub login, or a profile update.
- **Communication:** Backend → database.
- **Use:** Login, profiles, attempts, reports, scoring, MMR, and badges refer to this user ID.
- **Stored:** Yes.
- **Hint:** A user has either `password_hash` or `github_id`, not both. The only admin is created during database setup.

## 5. Profile update

Users can change their username, email, or predefined avatar.

### Format

All fields are optional. Only the fields being changed are sent.

| Field | Meaning |
| --- | --- |
| `username` | New unique username |
| `email` | New unique email |
| `avatar` | New predefined avatar ID; students only |

### Example

**When:** A user saves changes to their profile.

**Sent from → to:** Profile frontend → main backend service.

```json
{
  "username": "new-rick",
  "avatar": "avatar-5"
}
```

### Workflow

- **When:** A user updates their profile.
- **Communication:** Profile page → backend → database.
- **Use:** The backend checks uniqueness and allowed avatar IDs before updating the account.
- **Stored:** Accepted changes replace the previous values.
- **Hint:** The user ID and role come from the login session and cannot be changed through this JSON.

## 6. User returned to the frontend

Private login information is removed before sending a user to the frontend.

### Format

| Field | Meaning |
| --- | --- |
| `id` | User ID |
| `username` | Display name |
| `role` | `student` or `admin` |
| `avatar` | Predefined avatar ID; empty for the admin |
| `total_score` | Student's score; empty for the admin |
| `mmr` | Student's MMR; empty for the admin |
| `badges` | Student's earned badge IDs; empty for the admin |

### Example

**When:** Login succeeds or a user opens a profile.

**Sent from → to:** Main backend service → frontend.

```json
{
  "id": "user-1",
  "username": "rick",
  "role": "student",
  "avatar": "avatar-3",
  "total_score": 120,
  "mmr": 42,
  "badges": ["first-success", "ten-exercises"]
}
```

### Workflow

- **When:** After login or when opening a profile.
- **Communication:** Database → backend → frontend.
- **Use:** The frontend displays the account without receiving private authentication fields.
- **Stored:** This response is not stored separately.
- **Hint:** `password_hash` and `github_id` are never returned to the frontend.

## User edge cases

- **Known GitHub ID:** If `github_id` already exists, log in to that account.
- **Username already used:** A matching username alone does not prove it is the same person. A new GitHub user must choose another username.
- **GitHub email already used by a local account:** Reject the GitHub registration. Accounts are not joined automatically.
- **Uppercase differences:** `Alex` and `alex` count as the same username. Emails follow the same rule.
- **Profile changes:** A new username or email is accepted only when it is still unique.
- **Disabled user:** Block login but keep attempts, reports, score, MMR, and badges.
- **Admin:** There is only one admin. It is created during database setup and cannot be disabled through the website. Avatar, score, MMR, and badges are empty for this account.
- **GitHub password:** GitHub users do not receive a local password or password-change option.
- **Badges:** Store only earned badge IDs. Adding a new available badge does not require updating every user.
- **Avatar:** Students choose from predefined avatars. Avatar upload is outside the current scope.
