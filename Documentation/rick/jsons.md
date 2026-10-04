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
- **Communication:** Admin page → backend → tester.
- **Use:** The tester replaces `/* STUDENT_CODE */` with `reference_solution` and runs every test.
- **Result:** If the tests and vector creation pass, the validated exercise is stored. Otherwise, the upload fails.
- **Discarded:** `reference_solution` is discarded after validation.
- **Hint:** The backend generates the exercise ID before testing so temporary tester responses and logs can identify the upload. A failed upload is not stored and its ID is never reused. The `hints` field is only learning help shown in the frontend. It is not used by RAG or the tester.

## 2. Request sent to the tester

The backend creates this request for both exercise validation and student submissions.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | ID of the exercise being tested |
| `exercise_title` | Exercise name included for readable logs |
| `exercise_type` | `function` or `program` |
| `code` | The reference solution or the student's code |
| `forbidden_functions` | Functions that cannot be used |
| `tests` | Compiler code, input, and expected output for every test |

### Example

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

- **When:** Validating an admin upload or correcting a student submission.
- **Communication:** Backend → tester.
- **Use:** The tester checks forbidden functions, compiles the code, runs every test, and compares the outputs.
- **Stored:** No. This request is temporary.
- **Hint:** The admin flow uses the reference solution as `code`. The student flow uses the submitted code.

## 3. Tester response

This tells the backend whether all tests passed.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | ID of the tested exercise |
| `exercise_title` | Name of the tested exercise |
| `success` | `true` only when every check passes |
| `error` | Simple compiler or test error; empty after success |

### Example

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "success": false,
  "error": "Test 2 returned the wrong output."
}
```

### Workflow

- **When:** After the tester finishes.
- **Communication:** Tester → backend.
- **Use:** The backend accepts or rejects an upload, or shows the result to the student.
- **Stored:** Only `success` is stored for a student attempt. The complete response is temporary.
- **Hint:** The ID and title make temporary logs easier to understand. Private expected outputs must not be included in the error shown to the student.

## 4. Validated exercise stored in the database

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
- **Communication:** Backend → database.
- **Use:** The backend displays the public fields, the tester uses the private tests, and RAG uses the embedding.
- **Stored:** Yes.
- **Hint:** The frontend receives `hints`. `tests`, forbidden checks, expected outputs, and the embedding are never sent to the student page.

## 5. Student submission

The student sends the exercise ID, exercise title, and their code.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | Exercise being answered |
| `exercise_title` | Exercise name included for readable logs |
| `code` | Student's C code |

### Example

```json
{
  "exercise_id": "exercise-123",
  "exercise_title": "Create ft_strlen",
  "code": "int ft_strlen(char *str) { int i = 0; while (str[i]) i++; return i; }"
}
```

### Workflow

- **When:** The student presses Submit.
- **Communication:** Student page → backend.
- **Use:** The backend finds the exercise, creates the tester request, and sends it to the tester.
- **Stored:** The code is discarded after testing. Only the attempt result is stored.
- **Hint:** `user_id` is taken from the login session. The backend checks the exercise ID and uses the title stored in the database before creating logs or tester requests.

## 6. Exercise attempt stored in the database

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

## 7. Student exercise report

The student reports a problem with an exercise.

### Format

| Field | Meaning |
| --- | --- |
| `exercise_id` | Exercise being reported |
| `report` | Message with a maximum of 100 characters |

### Example

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

## 8. Reports shown to the admin

The backend groups report rows by user when displaying them.

### Format

| Field | Meaning |
| --- | --- |
| `user_id` | User who reported the exercise |
| `username` | Current username loaded from the users table |
| `reports` | All messages sent by that user for this exercise |

### Example

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
- **Uppercase differences:** `Rick` and `rick` count as the same username. Emails follow the same rule.
- **Profile changes:** A new username or email is accepted only when it is still unique.
- **Disabled user:** Block login but keep attempts, reports, score, MMR, and badges.
- **Admin:** There is only one admin. It is created during database setup and cannot be disabled through the website. Avatar, score, MMR, and badges are empty for this account.
- **GitHub password:** GitHub users do not receive a local password or password-change option.
- **Badges:** Store only earned badge IDs. Adding a new available badge does not require updating every user.
- **Avatar:** Students choose from predefined avatars. Avatar upload is outside the current scope.
