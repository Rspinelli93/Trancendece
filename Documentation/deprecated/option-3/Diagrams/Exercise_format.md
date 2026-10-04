# The exercise JSON

Each exercise is described in one JSON file. Admin uploads and LLM-generated exercises use the same format.

We can upload one file, several files, or a JSON array containing several exercises.

## What belongs inside

| Field | Meaning |
| --- | --- |
| `name` | Exercise title |
| `topic` | One of our chosen topics |
| `level` | Exercise difficulty |
| `description` | Instructions, function to write, and examples |
| `starter_code` | Code initially shown to the student |
| `reference_solution` | A working answer used to validate the exercise |
| `compiler_code` | A C program that tests the solution and prints results |
| `expected_output` | What the testing program should print |

The backend assigns the exercise ID and status. It also sets time and memory limits for running code.

## Example

```json
{
  "name": "Count the characters",
  "topic": "strings",
  "level": 1,
  "description": "Write int count_chars(const char *text). Return the number of characters in the string, without counting the final null byte. The input is never NULL. Do not modify it. For example, hello returns 5 and an empty string returns 0.",
  "starter_code": "int count_chars(const char *text)\n{\n    /* Write your code here */\n}\n",
  "reference_solution": "int count_chars(const char *text)\n{\n    int count = 0;\n    while (text[count])\n        count++;\n    return count;\n}\n",
  "compiler_code": "#include <stdio.h>\n\n{{SOLUTION}}\n\nint main(void)\n{\n    printf(\"%d\\n\", count_chars(\"hello\"));\n    printf(\"%d\\n\", count_chars(\"\"));\n    printf(\"%d\\n\", count_chars(\"a b\"));\n    return 0;\n}\n",
  "expected_output": "5\n0\n3\n"
}
```

Inside a JSON string, `\n` means a new line.

## How the code runs

`compiler_code` contains a placeholder called `{{SOLUTION}}`. Our backend replaces it with either the reference solution or the student's code.

The resulting program looks like this:

```c
#include <stdio.h>

/* Reference solution or student's function goes here */

int main(void)
{
    printf("%d\n", count_chars("hello"));
    printf("%d\n", count_chars(""));
    printf("%d\n", count_chars("a b"));
    return 0;
}
```

Judge0 compiles and runs the program. Our backend compares its output with `expected_output`.

The program must finish successfully and produce the expected results to pass.

## Before an exercise is published

1. Check that the JSON contains the required fields.
2. Insert the reference solution into `compiler_code`.
3. Send the completed program to Judge0.
4. Compare its output with `expected_output`.

If any check fails, the exercise is rejected. The admin sees the reason and can discard it.

For a batch upload, show the passed and failed exercises separately. Only passed exercises confirmed by the admin are saved.

Admin exercises can then enter the RAG. LLM-generated exercises remain trials until a student also submits a passing solution.

## When a student submits

1. Insert the student's code into the same `compiler_code`.
2. Compile and run it through Judge0.
3. Compare the output with the same `expected_output`.
4. Save the result and award progress if the student passes.

Students receive a simple result:

- Passed.
- Compilation error.
- Wrong output.
- Time limit reached.
- Memory limit reached.
- Program crashed.

If our correction service fails, show a service error and allow a retry. It does not count as a student mistake.

## What students can see

Students see the exercise name, topic, level, description, and starter code.

The reference solution, testing program, and expected test output stay on the server.

## Broken exercises

If an exercise turns out to be incorrect or unclear, students can report it. An admin can disable it so students and the RAG stop receiving it.

We do not need a separate repair workflow or errors added to the exercise JSON. A corrected replacement can be uploaded and validated again.

A passing test does not guarantee that an exercise is perfect, so ratings and reports remain useful.

## Memory checks

Time and memory limits protect the platform while code runs.

Detecting a **memory leak** is a separate check. Correct output alone cannot tell us whether the program released its allocated memory. We only add memory-leak results if we configure and test a tool that detects them.