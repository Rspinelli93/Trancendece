# Option 4 — Differences from Option 3

Option 4 keeps the same main idea: a C learning platform with accounts, exercises, progress, a compiler, levels, badges, and a leaderboard.

The main change is how exercises are chosen and how the AI is used.

The main reason for this change is to avoid the problem Garance mentioned: if the LLM keeps generating exercises from existing examples, it may create duplicates or slightly different versions of the same exercise. Option 4 avoids this by making the AI search and reuse a controlled library instead of generating more exercises.

## Option 3

In Option 3, the student chooses a topic and level.

If the platform does not have a suitable exercise, the RAG finds similar examples and gives them to the LLM. The LLM then creates a new exercise. The new exercise must pass the compiler and tests before it can be given to a student.

This creates several problems:

- The LLM may generate exercises that are too similar to existing ones.
- Generated exercises require extra validation and trial states.
- The exercise library may slowly fill with repeated content.
- The RAG is mainly being used to help generate content, which does not clearly match the complete RAG module in the subject.

## Option 4

In Option 4, exercises are prepared and validated before students can receive them. The LLM does not create exercises.

The student:

1. chooses their level;
2. writes what they want to learn in a text box;
3. receives an existing exercise that matches the request.

The student no longer chooses an exercise type or topic from a list. The request can be written naturally, for example:

> I understand pointers, but I want to learn how a function can change the original pointer.

The system then:

1. checks the student's level;
2. searches the validated exercise library for the closest matches;
3. gives the best matches to the LLM;
4. asks the LLM to select one of those exercises and explain why it is suitable;
5. returns no match if the library has nothing suitable.

The LLM can only choose an exercise returned by the search. It cannot invent an exercise or use an ID that does not exist.

## What changes

| Option 3 | Option 4 |
| --- | --- |
| The student chooses a topic and level. | The student chooses a level and explains what they want to learn. |
| The LLM generates new exercises. | The LLM selects an existing exercise. |
| RAG finds examples for exercise generation. | RAG finds exercises that match the student's request. |
| Generated exercises need validation and a trial stage. | Exercises are already validated before they can be recommended. |
| New exercises may repeat existing content. | The system only searches a controlled exercise library. |
| Students do not communicate with the AI. | Students communicate with the AI through one simple request box. |

## What stays the same

- The platform teaches C.
- Students create an account and save their progress.
- Admins add exercises using JSON files or forms.
- Exercises must pass validation before becoming available.
- Students write and submit C code.
- The compiler checks student submissions.
- Broken exercises can be reported or disabled.
- Levels, badges, progress, and leaderboards remain available.
- There are no sockets or real-time games.

## Why Option 4 is clearer

The RAG now has one clear purpose: find the right exercise inside the existing library.

The LLM also has a limited role: choose from the retrieved exercises and write a short explanation. It does not create learning content or decide whether an exercise is technically valid.

This is easier to control because every exercise already exists, has been checked, and has a valid ID. It also fits the complete RAG module more clearly: the student asks for something, the system retrieves relevant information, and the LLM generates an answer based on that information.

The subject lists complete RAG as a 2-point major module. To support that module, the final system must use a large exercise dataset, retrieve useful context, and generate a relevant answer for the student.
