# Exercise Generation, Validation and Correction Logic

## 1. General idea

The system uses the LLM to create coding exercises, but the LLM does not decide whether a player’s answer is correct.

The responsibilities are separated:

* Person 5 uses the LLM to generate exercises.
* Person 4 validates exercises and corrects player submissions.
* Person 3 stores approved exercises in the database.
* Person 2 uses the exercises during matches.
* Person 1 displays the exercises and results to the players.

The basic logic is:

```text
LLM generates an exercise
        ↓
Person 4 validates it
        ↓
Person 3 saves it
        ↓
Person 2 uses it in a match
        ↓
Person 4 corrects player submissions
```

## 2. Restricting the exercises

The LLM should not be allowed to generate any kind of exercise without restrictions. Person 4 cannot automatically validate completely unpredictable exercise formats.

For the first version, the LLM should generate C function exercises such as:

* `ft_strlen`
* `ft_strcpy`
* `ft_atoi`
* `ft_isalpha`
* `ft_toupper`

Every exercise must follow the same JSON structure.

## 3. What the LLM generates

Person 5 asks the LLM to generate a complete exercise package containing:

* Title
* Description
* Difficulty
* Required function name
* Function prototype
* Starter code
* Reference solution
* Public tests
* Hidden tests
* Expected results
* Time limit
* Memory limit

Example:

```json
{
  "judgeType": "FUNCTION",
  "title": "ft_strlen",
  "description": "Write a function that returns the length of a string.",
  "functionName": "ft_strlen",
  "prototype": "int ft_strlen(const char *str);",
  "starterCode": "int ft_strlen(const char *str) {\n}",
  "referenceSolution": "...",
  "publicTests": [],
  "hiddenTests": [],
  "timeLimitMs": 1000,
  "memoryLimitMb": 64
}
```

Person 5 first checks that the generated JSON has the correct structure. This confirms that all required fields exist, but it does not prove that the exercise actually works.

## 4. Person 4’s role

Person 4 is the **C Runner, Exercise Validator and Submission Judge**.

Person 4 is more than a JSON parser. The parser only checks the format. Person 4 checks the real behaviour of the exercise by compiling and executing code.

A simple comparison is:

> Person 5 writes the exam. Person 4 tests the exam and later corrects the players’ answers.

Person 4 should expose an internal validation route such as:

```http
POST /internal/v1/exercises/validate
```

Person 5 sends the generated exercise package to this route.

## 5. How an exercise is validated

Person 4 performs the following checks.

### Structure check

Confirm that the exercise contains:

* A valid function name
* A valid prototype
* A reference solution
* Public tests
* Hidden tests
* Valid execution limits

### Compilation check

Compile the reference solution using strict compiler options:

```bash
gcc -std=c11 -Wall -Wextra -Werror
```

The exercise is rejected if the reference solution does not compile or produces warnings.

Person 4 can also use sanitizers to detect invalid memory access and undefined behaviour.

### Reference solution check

Run the reference solution against every public and hidden test.

The reference solution must pass every test. If it fails even one test, the exercise is rejected.

### Edge-case check

Person 4 should add standard edge cases instead of trusting only the tests created by the LLM.

For `ft_strlen`, the tests could include:

```text
""                → 0
"a"               → 1
"hello"           → 5
"hello world"     → 11
"     "           → 5
A very long string → correct length
```

### Wrong-solution check

Person 4 should test deliberately incorrect solutions.

For example:

* A function that always returns zero
* A function that returns the length plus one
* A function that stops at a space
* A function that only works with short strings
* A function with an infinite loop

The hidden tests must reject these incorrect solutions. If an incorrect solution passes, the exercise needs better tests.

### Performance and security check

Person 4 verifies that:

* The reference solution respects the time limit.
* Infinite loops are stopped.
* Memory usage is limited.
* Excessive output is stopped.
* The code cannot access the network.
* The code cannot access private server files.
* The code runs inside an isolated environment.

### Repeatability check

The same exercise should be executed several times.

It must produce the same result every time. Exercises that depend on random values, external files or uninitialized memory should be rejected.

## 6. Exercise approval

The exercise follows a series of states:

```text
DRAFT
  ↓
VALIDATING
  ↓
APPROVED or REJECTED
  ↓
ACTIVE
```

An exercise becomes `APPROVED` only when all automatic validations pass.

However, the LLM could generate a description, solution and tests that agree with each other but are all logically wrong. Person 4 can prove that the package works technically, but cannot always prove that the exercise’s meaning is correct.

For that reason, an approved exercise should receive a quick human review before becoming `ACTIVE`.

This review can be done through a CLI command. An admin page is not necessary.

```bash
npm run exercises:review
npm run exercises:approve -- exercise-123
```

## 7. Saving approved exercises

Person 3 saves approved exercises in PostgreSQL.

The `exercises` table stores information such as:

```text
id
title
description
difficulty
function_name
prototype
starter_code
reference_solution
time_limit_ms
memory_limit_mb
status
version
created_at
```

A separate `test_cases` table stores:

```text
id
exercise_id
visibility
input
expected_output
position
```

The `visibility` field identifies whether a test is:

* `PUBLIC`
* `HIDDEN`

The reference solution and hidden tests are private. They must never be sent to the frontend.

## 8. Loading exercises during a match

When Person 2 creates a match, the game engine asks Person 3 for active exercises.

The frontend receives only:

* Exercise title
* Description
* Function prototype
* Starter code
* Public examples

The following information stays on the server:

* Reference solution
* Hidden tests
* Hidden expected results

## 9. Correcting a player submission

When the player presses **Run code**, the submission is tested only with public tests. This allows the player to see basic errors while developing the solution.

When the player presses **Send answer**, Person 2 sends the official submission to Person 4.

A possible route is:

```http
POST /internal/v1/executions
```

The request contains:

```json
{
  "exerciseId": "exercise-123",
  "sourceCode": "int ft_strlen(const char *str) { ... }",
  "mode": "OFFICIAL"
}
```

Person 4 then:

1. Creates an isolated environment.
2. Compiles the player’s code.
3. Runs the hidden tests.
4. Applies time and memory limits.
5. Returns an official verdict.

Possible verdicts include:

```text
ACCEPTED
WRONG_ANSWER
COMPILE_ERROR
RUNTIME_ERROR
TIME_LIMIT
MEMORY_LIMIT
```

Person 4 only returns the result. Person 2 uses that result to update:

* Player lives
* Current challenge
* Score
* Match progress
* Winner

## 10. The LLM’s role in corrections

The LLM can help explain an error, but it should not decide the official result.

The correction flow is:

```text
Person 4 produces the official verdict
        ↓
Person 5 sends safe information to the LLM
        ↓
The LLM generates a simple explanation
```

The LLM can receive:

* Exercise description
* Player code
* Compiler error
* Official verdict
* Public-test information

It should not receive or reveal hidden-test answers.

For competitive matches, LLM explanations should normally be shown after the player completes the challenge or after the match ends. Otherwise, the LLM could provide too much assistance during the competition.

## 11. Final division of responsibilities

### Person 1 — Frontend

* Sends Run Code and Send Answer actions.
* Displays verdicts and optional LLM feedback.

### Person 2 — Game engine

* Sends official submissions to Person 4.

### Person 3 — Backend and database

* Saves approved exercises.
* Stores public and hidden tests.
* Returns active exercises to the game engine.
* Protects private exercise information.

### Person 4 — Runner and validator

* Validates generated exercises.
* Compiles reference solutions.
* Tests edge cases.
* Rejects weak or broken exercises.
* Executes player code safely.
* Produces the official verdict.

### Person 5 — LLM and infrastructure

* Generates exercise JSON.
* Checks the JSON structure.
* Sends generated exercises for validation.
* Uses the LLM to explain player errors.
* Manages the infrastructure required by the generator and runner.

---

# Summary

	The LLM creates a possible exercise, but its output is never trusted automatically.
---
	Person 4 validates the exercise through real compilation and execution. Only exercises that compile, pass all tests, reject incorrect solutions and respect security limits can be approved.
---
	Person 3 stores the approved exercise. Person 2 loads it during a match, and Person 4 later uses the saved hidden tests to correct player submissions.
---
	The official result always comes from repeatable compilation and tests. The LLM is used for content generation and helpful explanations, not for deciding scores or winners.
