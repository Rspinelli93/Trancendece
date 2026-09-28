# The exercise JSON

One file describes one exercise. Use the same format for admin uploads and LLM generation. A batch is several files or an array of exercise objects.

## What belongs inside

| Field | Meaning |
| --- | --- |
| `schema_version` | Which file format this uses |
| `slug`, `title` | Stable name and readable title |
| `topic`, `level` | One allowed topic and difficulty level |
| `language` | `c` for the first version |
| `description` | Instructions and edge-case behaviour |
| `function_signature` | The function the student must write |
| `starter_code` | What initially appears in the editor |
| `test_template` | One of our approved testing programs |
| `examples` | Cases students can see |
| `hidden_tests` | Private input and expected-result cases |
| `reference_solution` | A solution used to validate the exercise |
| `limits` | Requested time and memory limits, capped by our backend |
| `requirements` | Allowed functions and other exercise rules |

The backend assigns IDs, version numbers, source, status, ratings, and RAG eligibility. JSON cannot mark itself approved. Requirements that need extra checks must be implemented in the test template; writing “do not use strlen” in a description does not enforce it.

## Small format example

This illustrates a string-length exercise. The `c_string_to_int_v1` template calls the function with each input and returns an integer for our backend to compare.

```json
{
  "schema_version": 1,
  "slug": "count-characters",
  "title": "Count the characters",
  "topic": "strings",
  "level": 1,
  "language": "c",
  "description": "Return the number of characters before the terminating null byte. Input is a non-null C string. Do not change it.",
  "function_signature": "int count_chars(const char *text);",
  "starter_code": "int count_chars(const char *text) {\n    /* Your code */\n}\n",
  "test_template": "c_string_to_int_v1",
  "examples": [
    {"input": "hello", "expected": 5},
    {"input": "", "expected": 0}
  ],
  "hidden_tests": [
    {"input": "a b", "expected": 3},
    {"input": "42!", "expected": 3}
  ],
  "reference_solution": "int count_chars(const char *text) { int n = 0; while (text[n]) n++; return n; }",
  "limits": {"cpu_seconds": 2, "memory_mb": 64},
  "requirements": []
}
```

This is a format illustration, not our complete test coverage. Memory-management and linked-list tasks need their own approved templates, including allocation ownership and cleanup checks.

The student response contains only the public fields. Hidden tests and reference solutions never appear in the browser's exercise JSON. We compare typed results exactly unless an exercise explicitly defines another rule.

## Error download

Keep the original exercise fields and append `validation_errors` to that same object:

```json
"validation_errors": [
  {
    "type": "compilation_error",
    "stage": "compile",
    "message": "The reference solution could not compile.",
    "details": "exercise.c:4: error: expected ';' before return"
  }
]
```

For a batch, download an array of failed exercise objects with their own errors. On re-upload, the backend ignores the old error field and runs checks again. If a file is not valid JSON, return its filename, original text, and parse error in a small wrapper instead.

Error categories include invalid format, compilation error, failed test, timeout, memory limit, crash, and service error. Memory error/leak categories require the extra checking setup described in [Compiler and correction](Compiler_and_correction.md).

Admin details can identify private failing tests. Students receive the same simple categories with private test information removed. A sanitizer result is reported as a leak only when the checker actually detects one.
